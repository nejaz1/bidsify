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
    #   - rule 1: convert behavioural data
    dtype           = FR.BEH
    order           = ['behavioral', DR.SUBJECT, DR.SESSION]            
    file_names      = [FR.SUBJECT, '_', FR.SESSION, '_IN2.mat']  
    opt                 = dict()
    opt[SP.NAME]        = 'smarts'    
    opt[SP.INCL]        = ['BN','TN','startTR','startTime','hand', 'digit','points']
    opt[SP.COL_OP]      = ["x['onset'] = (x['startTR']*2000 + x['startTime'])/1000",
                           "x['duration'] = 4*2"]
    opt[FR.BEH_JSON]    = {'RepetitionTime': 2, 'Instruction': 'Press instructed finger, keeping all other fingers stable'} 
    
    bd.add_rule(dtype,file_names,order,opt)
    
    #   - rule 2: convert anatomicals
    dtype       = FR.T1
    order       = ['anatomicals', DR.SUBJECT, [DR.COLUMN, 'RefT1']]    
    file_names  = [FR.SUBJECT, '_', [FR.COLUMN, 'RefT1'], '_T1.nii']  
    opt         = []
    
    bd.add_rule(dtype,file_names,order,opt)

   
    #   - rule 3: DWI
    dtype       = FR.DWI
    order       = ['anatomicals', DR.SUBJECT, [DR.COLUMN, 'RefT1']]
    file_names  = ['DTI_map.nii']      
    opt         = []
    
    bd.add_rule(dtype,file_names,order,opt)


    # - rule 4: functionals
    dtype       = FR.FUNC_TASK
    order       = ['imagingdata', DR.SUBJECT, DR.SESSION]    
    file_names  = ['ra', FR.SUBJECT, '_', FR.SESSION, '_', 'MF', SP.RUN_NO, '.nii']  
    opt         = dict()
    opt[SP.NAME]        = 'smarts'    
    opt[FR.FUNC_JSON]   = {'RepetitionTime': 2, 'TaskName': 'smarts'}     

    bd.add_rule(dtype,file_names,order,opt)   
    
#      - rule 5: resting state data
#

    # execute all the rules
    bd.run_all_rules()
    