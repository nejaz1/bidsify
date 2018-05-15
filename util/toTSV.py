import scipy.io as sio
import pandas as pd


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

# exclude data with given column names
def excludeData(data, exclCols):
    d = data.copy()
    
    for i in range(len(exclCols)):
        d.pop(exclCols[i])
            
    return d
    
# convert internall dictionary to into a pandas dataframe 
# exclude the columns with given names  
def toDataframe(data, exclCols):
    d  = excludeData(data,exclCols)
    df = pd.DataFrame()
    
    for key, value in d.items():
        df[key] = d[key][:,0]
        
    return df
        

# save data frame to file
# use tab delimitation, file extension is tsv
def saveToTSV(filename, df):
    df.to_csv(filename, sep='\t', index=False)
