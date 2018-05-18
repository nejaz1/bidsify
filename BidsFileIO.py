import scipy.io as sio
import pandas as pd
import os
import json
import shutil as sh

# load delimited text file into a pandas dataframe
def loadDelimToPandas(file_name, delim):
    if os.path.isfile(file_name):
        df = pd.read_csv(file_name, sep=delim)
    else:
        print('loadDelimToPandas::file not found')
        df = None
    return df

# make directory defined in the path
# creates subjdirectories along the way
def make_directory(dir_path):    
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

# check if the file_name sits in a valid directory, if not create it        
def validate_directory(file_name):
    d = os.path.dirname(file_name)    
    if not os.path.isdir(d):
        os.makedirs(d)

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
def readBehavioural(fname, inclCols):
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
    validate_directory(filename)
    df.to_csv(filename, sep='\t', index=False, na_rep='nan')
    
# save json text to file
def saveToJSON(filename, json_text):
    validate_directory(filename)    
    with open(filename, 'w') as f:
        json.dump(json_text, f)
    f.close()
    
# load json file into dictionary
def loadFromJSON(filename):
    validate_directory(filename)
    with open(filename, 'r') as f:
        ds = json.load(f)
    f.close()    
    return ds


# copy src file to destination
def copyfile(src, dest):
    validate_directory(dest)
    
    if not os.path.isfile(src):
        print('BidsFileIO::missing file::' + src)
    else:
        sh.copyfile(src,dest)
