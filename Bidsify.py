"""
Base class to provide BIDS conversion functionality

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""
import pandas as pd
from BidsRuleIDs import Dir as DR, File as FR, Special as SP
from BidsNaming import BidsifyNaming
import BidsFileIO as fio
import numpy as np
import pdb


class Bidsify:    
    # constructor
    def __init__(self):
        self.namer = BidsifyNaming()
        
        # create list of rules
        self.rules      = list()
        
    # bids namer needs these file paths
    def set_directories(self, source, dest):
        self.namer.set_directories(source,dest)        
        
    # bids namer needs the data in the subject file
    def set_subject_file(self, subject_file):
        self.namer.set_subject_file(subject_file)        
                    
    # list of columns defines the subject and session names to be used as 
    # directories names in raw data 
    def set_raw_format(self, subj, ses):
        self.namer.set_raw_format(subj,ses)
    
    # list of columns defines the subject and session names to be used as 
    # directories names in bids        
    def set_bids_format(self, subj, ses):
        self.namer.set_bids_format(subj,ses)
        
    # save participant info as tsv in dest directory
    def save_participants_file(self):
        # adding participants identifier to file
        df = self.namer.get_subject_data()
        
        rows, col = df.shape
        p = list()
        for i in range(rows):
            p.append(self.namer.tags.tSubj + self.namer.get_bids_subj_name(i))

        df[self.namer.tags.tParticipantID] = p
        
        # saving file in bids root directory
        f = self.namer.get_participants_file_name()
        fio.saveToTSV(f,df)
                
    # make required directories for data in i-th row
    def make_ses_dirs(self,i):
        dpath   = self.namer.get_bids_ses_dir(i)
        fio.make_directory(dpath)
                
    # add rule
    def add_rule(self, dtype, file_names, order, opt):    
        r                   = dict()
        r['dtype']          = dtype
        r['file_names']     = file_names
        r['order']          = order
        r['opt']            = opt
        self.rules.append(r)
        
    # apply all available rules to given row data
    def apply_rule(self, row, rules_to_run):        
        for j in rules_to_run:
            r = self.rules[j]
                
            # get all options associated with rule
            dtype       = r['dtype']
            file_names  = r['file_names']
            order       = r['order']
            opt         = r['opt']            

            print(str(dtype))
            print("row " + str(row+1) + ': ', end='')
                                
            # parse over rules            
            if dtype in FR:                
                # read raw & bids converted files
                raw     = self.namer.get_raw_file_path_from_rule(row, r)
                
                if (raw is None):
                    print("skipping")
                    continue
                                
                if dtype is FR.BEH:     # this is a behavioural rule, send to toTSV
                    # STEP 1 :load raw behavioural file, convert to tsv and save
                    data    = fio.readBehavioural(raw,opt[SP.INCL])
                    outf    = self.namer.get_bids_file_path_from_dtype(row, dtype, opt)
                    
                    #   PRIOR TO SAVING
                    #       - need to check if any renaming or math needs to be done
                    if SP.COL_OP in opt.keys():
                        op = opt[SP.COL_OP] # operations to perform
                        x = data    # data to perform op on: get ptr to pandas, this will propogate to data as well                        
                        # loop over operations
                        for sp in range(len(op)):
                            exec(op[sp])                            

                    fio.saveToTSV(outf,data)
                    
                    # STEP 2 :(optional)write json file to disk
                    if FR.BEH_JSON in opt.keys():
                        data    = opt[FR.BEH_JSON]
                        outf    = self.namer.get_bids_file_path_from_dtype(row, FR.BEH_JSON, opt)
                        fio.saveToJSON(outf,data)                    

                elif dtype in [FR.T1, FR.DWI]:     # this is an anatomical image, just rename/copy
                    bids    = self.namer.get_bids_file_path_from_dtype(row, dtype, opt)
                    fio.copyfile(raw,bids)  
                    
                elif dtype in [FR.FUNC_TASK]:       # this is a list of functional images, might contain wildcard
                    # do i need to search for files?
                    indx = self.namer.is_wildcard(file_names)
                    if not(indx==[]):
                        file_list   = self.namer.search_files_from_wildcard(raw)
                        tokens      = raw.split('*')
                        runno       = self.namer.tokenize_run_no(file_list,tokens)
                        print("Copying in order: {}".format(runno))
                        runopt = opt.copy()
                        
                        for i in range(len(runno)):
                            runopt[SP.RUN_NO] = runno[i]
                            bidsf   = self.namer.get_bids_file_path_from_dtype(row,dtype,runopt)
                            rawf    = file_list[i]  
                            fio.copyfile(rawf,bidsf)  
                            
                            # STEP 2 :(optional)write json file to disk
                            if FR.FUNC_JSON in opt.keys():                            
                                data    = opt[FR.FUNC_JSON]
                                outf    = self.namer.get_bids_file_path_from_dtype(row, FR.FUNC_JSON, runopt)
                                fio.saveToJSON(outf,data)                    
                    else:
                        print('UNDEFINED CONTROL SEQ: in dtype FR.FUNC_TASK')



                print('')
            else:
                print('rule is invalid')
                

    # run conversion of raw data into bids format
    # function loops over all subjects in the subject file and sessions
    def run_all_rules(self):
        # loop over all subjects
        rows = self.namer.get_participant_rows()
        
        # loop over all rules user has defined
        rules_to_run = range(len(self.rules))

        for i in range(rows):
            # make directories for subj/ses
            #self.makeDir(i)

            # apply rules to this row data
            self.apply_rule(i, rules_to_run)                
            
            # get subject and sess dir names for i-th row
            #[subj, ses] = self.get_bids_dir_names(i)
            
    # run a subset of rules given by indices
    def run_rules(self, rules_to_run):
        # loop over all subjects
        rows = self.namer.get_participant_rows()
        
        for i in range(rows):
            # make directories for subj/ses
            #self.makeDir(i)

            # apply rules to this row data
            self.apply_rule(i, rules_to_run)                
            
            # get subject and sess dir names for i-th row
            #[subj, ses] = self.get_bids_dir_names(i)
            
            

                