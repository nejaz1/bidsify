"""
Enumerated data types useful for data conversion

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""

class BidsTags:
    tSubj             = 'sub-'
    tSes              = 'ses-'
    tParticipantID    = 'participants-id'   
    tFunc             = 'func'
    tFuncEvents       = 'task-{}_events'
    tFuncRun          = 'task-{}_run-{}_bold'    
    tAnat             = 'anat'    
    tDWI              = 'dwi'        
    
    
    fParticipantID    = 'participants.tsv'

    def __init__(self):
        """ purposely left empty """