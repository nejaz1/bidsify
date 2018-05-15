"""
Base class for BIDS
"""
import pandas as pd
import os
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
        
    # load subject file into pandas dataframe
    def loadSubjFile(self):
        # assumes that file is in root folder of destination directory
        f               = os.path.join(self.destDir,self.subjFile)       
        if os.path.isfile(f):
            self.subjData   = pd.read_csv(f, sep='\t')
        else:
            print('subject file not found in dest directory')
        
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

    # list of columns (in order) defines the subject and session names to be used as 
    # directories names in raw data 
    def set_raw_format(self, subj, ses):
        self.rawFormat['subj'] = subj
        self.rawFormat['ses']  = ses
    
    # list of columns (in order) defines the subject and session names to be used as 
    # directories names in bids        
    def set_bids_format(self, subj, ses):
        self.bidsFormat['subj'] = subj
        self.bidsFormat['ses']  = ses
        
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

    # run conversion of raw data into bids format
    # function loops over all subjects in the subject file and sessions
    def convert(self):
        # loop over all subjects
        rows, cols = self.subjData.shape
        
        for i in range(rows):
            # make directories for subj/ses
            self.makeDir(i)

            # get subject and sess dir names for i-th row
            #[subj, ses] = self.get_bids_dir_names(i)
            
            
            
            
            
            
    
                