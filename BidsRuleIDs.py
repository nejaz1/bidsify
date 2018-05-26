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
    FUNC_JSON   = 5        
    T1          = 6
    DWI         = 7    
    FUNC_TASK   = 8
    FUNC_REST   = 9    
    MASK        = 10

class Special(Enum):
    EMPTY       = 0
    INCL        = 1
    EXCL        = 2
    NAME        = 3   
    COL_OP      = 4            
    RUN_NO      = 5  

    
