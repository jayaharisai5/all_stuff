import pandas as pd 


def read_csv():
    df = pd.read_csv('healthcare-dataset-stroke-data.csv')
    return df

def handling_null_values():
    df = read_csv()
    shape = df.shape
    columns = df.columns 
    length = len(columns)
    null = df.isnull().sum()
    adition_null = df.isnull().sum().sum()
    null_array=[]
    for u in null:
        print(u)
        null_array.append(u)
    return(columns, null_array, length, adition_null, shape)

def replace(option):
    df = read_csv()
    if option == 1:
        column_means = df.mean()
        df.fillna(column_means, inplace=True)
    elif option == 2:
        column_median = df.median()
        df.fillna(column_median, inplace=True)

def remove(option):
    df = read_csv()
    if option ==1:
        df.dropna(inplace=True)
    return df

