import scipy.io as sio
import pandas as pd
import os


# print header names in a mat file 
def printMatHeader(filename):
    d   = sio.loadmat(filename)

    # list of fields to remove from dictionary
    igField = ['__header__','__version__','__globals__']

    for key, value in d.items():
        if key not in igField:
            print(key)

# load and return data in a mat file 
def readMatData(filename):
    d   = sio.loadmat(filename)

    # list of fields to remove from dictionary
    igField = ['__header__','__version__','__globals__']

    for i in range(len(igField)):
        d.pop(igField[i])
            
    return d

# only return data matching given column names
def includeData(data, inclCols):
    d = dict()
    
    for i in range(len(inclCols)):
        d[inclCols[i]] = data[inclCols[i]]
    return d
    
# convert internall dictionary to into a pandas dataframe 
# exclude the columns with given names  
def toDataframe(data, inclCols):
    d  = includeData(data,inclCols)
    df = pd.DataFrame()
    
    for key, value in d.items():
        df[key] = d[key][:,0]
        
    return df
        
# read data from csv
def read(fname, inclCols):
    # check file extension
    filename, ext = os.path.splitext(fname)
    
    df = None
    
    if ext == '.mat':
        d   = readMatData(fname)
        df  = toDataframe(d, inclCols)
    elif ext == '.dat':    
        print('.dat behavioural file reading capability not added yet')
    else:
        print('unrecognized file type')
        
    return df

# save data frame to file
# use tab delimitation, file extension is tsv
# makes directory if it does not exist in file path
def saveToTSV(filename, df):
    d = os.path.dirname(filename)
    
    if not os.path.isdir(d):
        os.makedirs(d)

    df.to_csv(filename, sep='\t', index=False, na_rep='nan')
