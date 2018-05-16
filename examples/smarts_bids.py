"""
Script to bidsify smarts data

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""
from Bidsify import Bidsify
from RuleIds import Dir as DR, File as FR, Special as SP

# program entry point
if __name__ == "__main__":
    # setting up source and destination directories
    source_dir   = '/Volumes/MotorControl/bids/smarts_raw/fmri'
    dest_dir     = '/Volumes/MotorControl/bids/smarts_bids/'

    # subject file contains information to be bidsified
    # this files needs to be in the root destination folder
    subj_file    = 'subject_list.txt'
    
    # create bidsify object to perform converstion
    bd = Bidsify(subj_file, source_dir, dest_dir)
    
    # create file directory naming formats for raw and bids data
    bd.set_raw_format(subj=['Centre','_','ID'], ses=['Week'])
    bd.set_bids_format(subj=['Centre','ID'], ses=['Week'])    

    # save participants information
    bd.saveParticipantsFile()
    
    # create rules
    #   - rule 0: session specific participant info

    #   - rule 1: convert behavioural data
    #   TODO:
    #       - rename fields
    #       - figure out, and get duration in dataset (onset in secs, duration in secs)
    #       - option to do math on columns
    dtype       = FR.BEH
    file_names  = [FR.SUBJECT, '_', FR.SESSION, '_IN2.mat']  
    dir_names   = {DR.BEHAVIOUR: 'behavioral'}
    order       = [DR.BEHAVIOUR, DR.SUBJECT, DR.SESSION]           
    opt         = {SP.INCL: ['BN','TN','startTR','startTime','hand', 'digit','points']}
    bd.add_rule(dtype,file_names,dir_names,order,opt)
    
   #   - rule 2: convert anatomicals
   
   #   - rule 3: DWI
   
   #   - rule 4: fieldmaps

   #   - rule 4: functionals
   
   #   - rule 5: resting state data
   
   
    # execute all the rules
    bd.convert()
    