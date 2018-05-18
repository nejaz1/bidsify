"""
Script to bidsify smarts data

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""
from Bidsify import Bidsify
from BidsRuleIDs import Dir as DR, File as FR, Special as SP

# program entry point
if __name__ == "__main__":
    # create bidsify object to perform converstion
    bd = Bidsify()
    
    # setting up source and destination directories + subject file
    bd.set_directories(source='/Volumes/MotorControl/bids/smarts_raw/fmri',dest='/Volumes/MotorControl/bids/smarts_bids/')
    bd.set_subject_file('subject_list_copy.txt')
    
    # set formats to correctly convert folders/names
    bd.set_raw_format(subj=['Centre','_','ID'], ses=['Week'])
    bd.set_bids_format(subj=['Centre','ID'], ses=['Week'])    

    # save participants information
    bd.save_participants_file()
    
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
    opt                 = dict()
    opt[SP.INCL]        = ['BN','TN','startTR','startTime','hand', 'digit','points']
    opt[FR.BEH_JSON]    = {'RepetitionTime': 2.7, 'Instruction': 'Press instructed finger, keeping all other fingers stable'} 
    
    bd.add_rule(dtype,file_names,dir_names,order,opt)
    
    #   - rule 2: convert anatomicals
    dtype       = FR.T1
    file_names  = [FR.SUBJECT, '_', [FR.COLUMN, 'RefT1'], '_T1.nii']  
    dir_names   = {DR.ANATOMICAL: 'anatomicals'}
    order       = [DR.ANATOMICAL, DR.SUBJECT, [DR.COLUMN, 'RefT1']]
    opt         = []
    
    bd.add_rule(dtype,file_names,dir_names,order,opt)

   
    #   - rule 3: DWI
    dtype       = FR.DWI
    file_names  = ['DTI_map.nii']  
    dir_names   = {DR.ANATOMICAL: 'anatomicals'}
    order       = [DR.ANATOMICAL, DR.SUBJECT, [DR.COLUMN, 'RefT1']]
    opt         = []
    
    bd.add_rule(dtype,file_names,dir_names,order,opt)

   
   #   - rule 4: fieldmaps

   #   - rule 4: functionals
   
   #   - rule 5: resting state data


   # execute all the rules
   bd.run_all_rules()
    