"""
Base class to provide BIDS conversion functionality

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""
import os
from BidsRuleIDs import Dir as DR, File as FR, Special as SP
import BidsFileIO as fio
from BidsTags import BidsTags
import glob
import pdb

class BidsifyNaming:
    sourceDir       = []
    destDir         = []
    derivDir        = []
    subjFile        = []
    
    rawFormat       = []
    bidsFormat      = []    
    subjData        = []
        
    # constructor
    def __init__(self):
        """ purposely left empty """
        self.rawFormat  = dict()
        self.bidsFormat = dict()
        
        # get list of tags for easy acess
        self.tags    = BidsTags()
        
    # bids namer needs these file paths
    def set_directories(self, source, dest, deriv):
        self.sourceDir  = source
        self.destDir    = dest
        self.derivDir   = deriv
        
    # bids namer needs these file paths
    def set_subject_file(self, subject_file):
        self.subjFile   = subject_file

        # now load the file
        fpath = self.subj_file_name()
        self.subjData = fio.loadDelimToPandas(fpath,'\t')
        
    # returns a copy of the subject data
    def get_subject_data(self):
        return self.subjData.copy()

    # list of columns defines the subject and session names to be used as 
    # directories names in raw data 
    def set_raw_format(self, subj, ses):
        self.rawFormat['subj']      = subj
        self.rawFormat['ses']       = ses

    # list of columns defines the subject and session names to be used as 
    # directories names in raw data 
    def set_bids_format(self, subj, ses):
        self.bidsFormat['subj']     = subj
        self.bidsFormat['ses']      = ses

    # concatenate selected columns for the given row i
    def concat_cols_for_row_i(self,i,cols):
        s = str()
        for c in cols:
            if c in self.subjData.columns:
                s += str(self.subjData.loc[i,c]).strip()
            else:
                s += c
        return s

    # if a tokenizer is present in file name, return its index, otherwise empty
    def is_wildcard(self, fname):
        # do i need to tokenize run no?
        tokIndx = []
        if SP.RUN_NO in fname:
            tokIndx = fname.index(SP.RUN_NO)
            
        return tokIndx

    # construct path for file name from row and provided rule info
    def search_files_from_wildcard(self, fname):
        return glob.glob(fname)
    
    # construct path for file name from row and provided rule info
    def tokenize_run_no(self, file_list, tokens):
        runno_list = list()
        
        for i in range(len(file_list)):
            f = file_list[i]
            runno_list.append(int(f.split(tokens[0])[1].split(tokens[1])[0]))
            
        return runno_list
        
        
    # construct path name from row and provided rule info
    def get_raw_dir_path_from_rule(self, row, rule):
        # get source base path
        subj    = self.get_raw_subj_name(row)
        ses     = self.get_raw_ses_name(row)        
        
        order = rule['order']
        
        # starts building order from raw source directory
        s = self.sourceDir

        # loop over order in 'order' variable
        for j in range(len(order)):
            # check if there element in order is a list
            if type(order[j]) == list:
                cmd = order[j]  # there can only be two columns
                if cmd[0] is DR.COLUMN:
                    srep = self.subjData.loc[row,cmd[1]].strip()
                    s    = os.path.join(s,srep)
            else:
                # check if this is not subj,sess directory
                if order[j] not in [DR.SUBJECT, DR.SESSION]:   
                    #s = os.path.join(s,rule['dir_names'][rule['order'][j]])
                    s = os.path.join(s,rule['order'][j])
                elif order[j] is DR.SUBJECT:
                    s = os.path.join(s,subj)
                elif order[j] is DR.SESSION:
                    s = os.path.join(s,ses)                

        return s

    # construct path for file name from row and provided rule info
    def get_raw_file_name_from_rule(self, row, rule):
        # get source base path
        subj    = self.get_raw_subj_name(row)
        ses     = self.get_raw_ses_name(row)        

        # starts building file name from empty
        s = str()
        
        # ordering of elements in the file name
        fname = rule['file_names']

        # loop over order in 'fname' variable
        for j in range(len(fname)):
            # check if there element in order is a list
            if type(fname[j]) == list:
                cmd = fname[j]  # there can only be two columns
                if cmd[0] is FR.COLUMN:
                    s += self.subjData.loc[row,cmd[1]].strip()
            else:                                        
                if fname[j] is FR.SUBJECT:
                    s += subj
                elif fname[j] is FR.SESSION:
                    s += ses
                elif fname[j] is SP.RUN_NO:
                    s += '*'
                else:
                    s += fname[j]
        
        return s    

    # make directory path for specific data type in bids
    def get_bids_dir_path_from_dtype(self, row, dtype, opt):
        # get dest base path
        subj    = self.get_bids_subj_name(row)
        ses     = self.get_bids_ses_name(row)       

        # starts building order from raw source directory
        s = self.destDir
        
        if dtype in [FR.BEH, FR.BEH_JSON, FR.FUNC_TASK, FR.FUNC_JSON, FR.FUNC_REST]:
            s = os.path.join(s,subj,ses,self.tags.tFunc)
        elif dtype is FR.T1:
            s = os.path.join(s,subj,ses,self.tags.tAnat)            
        elif dtype is FR.DWI:
            s = os.path.join(s,subj,ses,self.tags.tDWI)
        elif dtype is FR.MASK:
            s = self.derivDir
            s = os.path.join(s,self.tags.tMask,subj,ses)        
        elif dtype is FR.BEH_RAW:
            s = self.derivDir
            s = os.path.join(s,self.tags.tBehRaw,subj,ses)
        elif dtype is FR.SURF:
            s = self.derivDir
            s = os.path.join(s,self.tags.tSurface)
        else:
            print('undefined data type')
            s = None
            
        return s

    # make file paths for specific data type in bids        
    def get_bids_file_name_from_dtype(self, row, dtype, opt):        
        # get dest base path
        subj    = self.get_bids_subj_name(row)
        ses     = self.get_bids_ses_name(row)                
        
        # starts building file name from empty
        s = subj + '_' + ses + '_'
        
        if dtype is FR.BEH:         # BEHAVIOUR TSV
            s += (self.tags.tFuncEvents + '.tsv').format(opt[SP.NAME])
        elif dtype is FR.BEH_JSON:  # BEHAVIOUR JSON
            s += (self.tags.tFuncEvents + '.json').format(opt[SP.NAME])
        elif dtype is FR.T1:        # ANATOMICAL T1
            s += 'T1w.nii'            
        elif dtype is FR.DWI:       # ANATOMICAL DWI
            s += 'dwi.nii'    
        elif dtype is FR.FUNC_TASK:     # Functional images
            s += (self.tags.tFuncRun + '.nii').format(opt[SP.NAME],opt[SP.RUN_NO])
        elif dtype is FR.FUNC_JSON:     # Functional json images
            s += (self.tags.tFuncRun + '.json').format(opt[SP.NAME],opt[SP.RUN_NO])   
        elif dtype is FR.BEH_RAW:        # Raw behavioural files
            s += (self.tags.tFuncRun + '.mat').format(opt[SP.NAME],opt[SP.RUN_NO])
        elif dtype is FR.MASK:
            s = opt[SP.NAME]   
        elif dtype is FR.SURF:
            s = 'x'+subj
        else:
            print('undefined data type')
            s = ''
            
        return s        
    
    ###########################################################
    # List of functions that compute names
    
    # bids namer needs these file paths
    def subj_file_name(self):
        return os.path.join(self.sourceDir,self.subjFile)

    # get number of runs in subject file
    def get_participant_rows(self):
        rows, cols = self.subjData.shape
        return rows

    # subject name used for bids for row i
    def get_bids_subj_name(self, i):
        return self.tags.tSubj + self.concat_cols_for_row_i(i,self.bidsFormat['subj'])

    # session name used for bids for row i
    def get_bids_ses_name(self, i):
        return self.tags.tSes + self.concat_cols_for_row_i(i,self.bidsFormat['ses'])
    
    # session name used for bids for row i
    def get_bids_ses_dir(self, i):
        subj    = self.tags.tSubj + self.concat_cols_for_row_i(i,self.bidsFormat['subj'])
        ses     = self.tags.tSes + self.concat_cols_for_row_i(i,self.bidsFormat['ses'])
        
        # make full path to session directory
        return os.path.join(self.destDir,subj,ses)        

    # subject name used for raw data for row i
    def get_raw_subj_name(self, i):
        return self.concat_cols_for_row_i(i,self.rawFormat['subj'])
    
    # session name used for raw data for row i
    def get_raw_ses_name(self, i):
        return self.concat_cols_for_row_i(i,self.rawFormat['ses'])    
    
    # file name/path for participants tsv file
    def get_participants_file_name(self):
        return os.path.join(self.destDir,self.tags.fParticipantID)  
    
    # for data in row i, returh the full path for file specified in rule
    def get_raw_file_path_from_rule(self, i, rule):
        try:
            d   = self.get_raw_dir_path_from_rule(i,rule)
            f   = self.get_raw_file_name_from_rule(i,rule)
            return os.path.join(d,f)
        
        except:
            return None
    
    def get_bids_file_path_from_dtype(self, i, dtype, opt):
        try:
            d   = self.get_bids_dir_path_from_dtype(i, dtype, opt)
            f   = self.get_bids_file_name_from_dtype(i, dtype, opt)        
            return os.path.join(d,f)
        except:
            return None
        
