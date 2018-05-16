"""
Enumerated data types useful for data conversion

Created: 15 May 2018
Eva Berlot & Naveed Ejaz
"""

from enum import Enum

class Dir(Enum):
    MODAL           = 0
    SUBJECT         = 1
    SESSION         = 2
    ANATOMICAL      = 3    
    FIELDMAP        = 4
    DICOM           = 5
    BEHAVIOUR       = 6
    GLM             = 7
    PREPROCESSED    = 8
             
class File(Enum):
    FILE        = 0
    SUBJECT     = 1
    SESSION     = 2
    BEH         = 3
    T1          = 4
    DWI         = 5    
    FUNC_TASK   = 6
    FUNC_REST   = 7    

class Special(Enum):
    EMPTY       = 0
    INCL        = 1
    EXCL        = 2
    
