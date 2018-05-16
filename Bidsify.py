"""
Base class to provide BIDS conversion functionality

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""
import pandas as pd
import os
from RuleIDs import Dir as DR, File as FR, Special as SP
import toTSV
import pdb

class Bidsify:
    subjFile        = None
    subjData        = None        

    sourceDir       = None
    destDir         = None   
    

    # constructor
    def __init__(self, subj_file, source_dir, dest_dir):
        self.subjFile   = subj_file
        self.sourceDir  = source_dir
        self.destDir    = dest_dir        
        self.loadSubjFile()
        
        # setting up new and old naming formats for conversion
        self.rawFormat  = dict()
        self.bidsFormat  = dict()

        # create list of rules
        self.rules      = list()
        
    # load subject file into pandas dataframe
    def loadSubjFile(self):
        # assumes that file is in root folder of destination directory
        f               = os.path.join(self.sourceDir,self.subjFile)       
        if os.path.isfile(f):
            self.subjData   = pd.read_csv(f, sep='\t')
        else:
            print('subject file not found in raw directory')

    # save subject file as tsv
    def saveParticipantsFile(self):
        # adding participants identifier to file
        df = self.subjData.copy()
        
        rows, col = df.shape
        p = list()
        for i in range(rows):
            p.append('sub-' + self.makeDirName(i,self.bidsFormat['subj']))

        df['participants-id'] = p
        
        # saving file in bids root directory
        f = os.path.join(self.destDir,'participants.tsv')
        toTSV.saveToTSV(f,df)
                
    # print data stored in each row i for dataframe
    # depending on experiment design, row could be a single subject, or a session for a subject
    def printRow(self, i):
        print(self.subjData.loc[i,:])

    # construct directory name for i-th row using provided columns
    # FOR INTERNAL USE ONLY
    def makeDirName(self,i,cols):
        # depending on experiment design, row could be a single subject, or a session for a subject
        s = str()
        for c in cols:
            if c in self.subjData.columns:
                s += str(self.subjData.loc[i,c]).strip()
            else:
                s += c
        return s
    
    # make required directories for data in i-th row
    def makeDir(self,i):
        # get subject and sess dir names for i-th row
        [subj, ses] = self.get_bids_dir_names(i)
        
        # make full path
        d = os.path.join(self.destDir,subj,ses)
        
        if not os.path.isdir(d):
            os.makedirs(d)

    # list of columns defines the subject and session names to be used as 
    # directories names in raw data 
    def set_raw_format(self, subj, ses):
        self.rawFormat['subj']      = subj
        self.rawFormat['ses']       = ses
    
    # list of columns defines the subject and session names to be used as 
    # directories names in bids        
    def set_bids_format(self, subj, ses):
        self.bidsFormat['subj']     = subj
        self.bidsFormat['ses']      = ses
        
    # list of columns (in order) defines the subject and session names to be used as 
    # directories names in bids        
    def get_bids_dir_names(self, i):
        subj    = 'sub-' + self.makeDirName(i,self.bidsFormat['subj'])        
        ses     = 'ses-' + self.makeDirName(i,self.bidsFormat['ses'])
        return [subj, ses]                

    # list of columns (in order) defines the subject and session names to be used as 
    # directories names in bids        
    def get_raw_dir_names(self, i):
        subj    = self.makeDirName(i,self.rawFormat['subj'])        
        ses     = self.makeDirName(i,self.rawFormat['ses'])
        return [subj, ses]                

    def make_raw_dir_path(self, row, rule):
        # get source base path
        [subj, ses] = self.get_raw_dir_names(row)
        
        # starts building order from raw source directory
        s = self.sourceDir
        
        # loop over order in 'order' variable
        for j in range(len(rule['order'])):
            # check if this is not subj,sess directory
            if rule['order'][j] not in [DR.SUBJECT, DR.SESSION]:   
                s = os.path.join(s,rule['dir_names'][rule['order'][j]])
            elif rule['order'][j] is DR.SUBJECT:
                s = os.path.join(s,subj)
            elif rule['order'][j] is DR.SESSION:
                s = os.path.join(s,ses)                

        return s
    
    def make_raw_file_name(self, row, rule):
        # get source base path
        [subj, ses] = self.get_raw_dir_names(row)

        # starts building file name from empty
        s = str()
        
        # ordering of elements in the file name
        fname = rule['file_names']
        
        # loop over order in 'fname' variable
        for j in range(len(fname)):
            if fname[j] is FR.SUBJECT:
                s += subj
            elif fname[j] is FR.SESSION:
                s += ses
            else:
                s += fname[j]

        return s    

    # make directory path for specific data type in bids
    def make_bids_dir_path(self, row, dtype):
        # get dest base path
        [subj, ses] = self.get_bids_dir_names(row)
        
        # starts building order from raw source directory
        s = self.destDir
        
        if dtype in [FR.BEH, FR.FUNC_TASK, FR.FUNC_REST]:
            s = os.path.join(s,subj,ses,'func')
        else:
            print('undefined data type')
            s = None
            
        return s

    # make file paths for specific data type in bids        
    def make_bids_file_name(self, row, dtype):
        # get dest base path
        [subj, ses] = self.get_bids_dir_names(row)

        # starts building file name from empty
        s = str()
        
        if dtype is FR.BEH:
            s += subj + '_' + ses + '_task-events.tsv' 
        else:
            print('undefined data type')
            s = ''
            
        return s        
   
    
    # add rule
    def add_rule(self, dtype, file_names, dir_names, order, opt):    
        r                   = dict()
        r['dtype']          = dtype
        r['file_names']     = file_names
        r['dir_names']      = dir_names
        r['order']          = order
        r['opt']            = opt
        self.rules.append(r)

    # apply all available rules to given row data
    def apply_rule(self, row):        
        # loop over all rules user has defined
        N = len(self.rules)

        for j in range(N):
            r = self.rules[j]
                
            # get all options associated with rule
            dtype       = r['dtype']
            file_names  = r['file_names']
            dir_names   = r['dir_names']            
            order       = r['order']
            opt         = r['opt']                        

            # parse over rules            
            if dtype in FR:
                # get directory path
                d   = self.make_raw_dir_path(row,r)
                
                if dtype is FR.BEH:     # this is a behavioural rule, send to toTSV
                    # get behavioural file
                    f       = self.make_raw_file_name(row,r)
                    f       = os.path.join(d,f)
                    data    = toTSV.read(f,opt[SP.INCL])
                    
                    # write to destination
                    destDir     = self.make_bids_dir_path(row, dtype)
                    destFile    = self.make_bids_file_name(row, dtype)
                    outf        = os.path.join(destDir,destFile)
                    toTSV.saveToTSV(outf,data)                    
            else:
                print('rule is invalid')
                

    # run conversion of raw data into bids format
    # function loops over all subjects in the subject file and sessions
    def convert(self):
        # loop over all subjects
        rows, cols = self.subjData.shape
        
        for i in range(rows):
            # make directories for subj/ses
            # self.makeDir(i)

            # apply rules to this row data
            self.apply_rule(i)                
            
            # get subject and sess dir names for i-th row
            #[subj, ses] = self.get_bids_dir_names(i)
            
            
            
            
            
            
    
                