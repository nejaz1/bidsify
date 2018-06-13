"""
Enumerated data types useful for data conversion

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""

from enum import Enum

class Dir(Enum):
    COLUMN          = 0
    SUBJECT         = 1
    SESSION         = 2
             
class File(Enum):
    COLUMN      = 0
    SUBJECT     = 1
    SESSION     = 2
    BEH         = 3
    BEH_JSON    = 4   
    BEH_RAW     = 5
    BEH_MVC     = 6
    FUNC_JSON   = 7        
    T1          = 8
    DWI         = 9    
    FUNC_TASK   = 10
    FUNC_REST   = 11    
    FUNC_MOV    = 12
    MASK        = 13
    SURF        = 14

class Special(Enum):
    EMPTY       = 0
    INCL        = 1
    EXCL        = 2
    NAME        = 3   
    COL_OP      = 4            
    RUN_NO      = 5  

    
