import json
import os

import altair as alt
import numpy as np
import pandas as pd

df = pd.read_csv('AB_NYC_2019.csv')

def null_count(df):
    #Calculating null values
    # We are dropping  Columns which have more than 30% of null value
    # Replacing null value with mean in case of int and float
    # If null value persist for other cases we are dropping those rows

    nulls_count = {col: df[col].isnull().sum() for col in df.columns}
    print(nulls_count)

    is_null_count_out_of_range = {col: df[col].isnull().sum() / df.shape[0] * 100 > 30 for col in df.columns}

    for k, v in is_null_count_out_of_range.items():
        if v:
             df.drop(k, axis=1, inplace=True)
        else:
         if isinstance(df[k][0], (np.int64, np.float64)):
            df[k].fillna(df[k].mean(), inplace=True)
         else:
            drop_list = df[df[k].isnull()].index.tolist()
            df.drop(drop_list, axis=0, inplace=True)

    nulls_count = {col: df[col].isnull().sum() for col in df.columns}
    print(nulls_count)
    return df

def unique_value_list(df1):
    #Finding all the unique values to in each column

    uniques = {col: df1[col].unique().tolist() for col in df1.columns}
    return uniques

def new_folder():
    # Directory
    directory = "Altair_Plots/Bar_Graph"

    # Parent Directory path
    parent_dir = "../"
    print(parent_dir)
    # Path
    path = os.path.join(parent_dir, directory)
    print(path)

    try:
       os.mkdir(path)
    except OSError as error:
       print(error)
    return  path

def write_unique_value_list(path, uniques):
    # Writing the above created dictionary to a text file

    with open(path + '/Unique_values.txt', 'w') as json_file:
       json.dump(uniques, json_file)

def dtypes_conversion(uniques):
    #Converting columns to categorical having less than or equal to 10
    #unique values in a column

    for k,v in uniques.items():
     if len(pd.Index(v)) <=10:
         df[k]=df[k].astype('category')

    cat_col=df.select_dtypes(include=['category']).columns.tolist()
    num_col=df.select_dtypes(include=['int64','float64']).columns.tolist()

    types = df.dtypes[df.dtypes == 'object']
    for i, j in types.items():
        try:
            df[i] = pd.to_datetime(df[i])
            df[i + '_year'] = pd.DatetimeIndex(df[i]).year
            df[i + '_month'] = pd.DatetimeIndex(df[i]).month
            cat_col.append(i + '_year')
            cat_col.append(i + '_month')
        except:
            pass
    print(df.dtypes)
    return cat_col,num_col

def bar_JSON_generator(path,cat_col,num_col):
    # Generating JSON using altair methods

    for i in range(len(cat_col)):
     for j in range(len(num_col)):
        chart=alt.Chart(df).mark_bar().encode(
            x=cat_col[i],
            y=num_col[j])
        chart.save(path+'/Bar_'+str(cat_col[i])+" Vs "+str(num_col[j])+"_"+"plot.json")
           #print(cat_col[i],num_col[j])
    print("Bar Graph JSON generated in ""Altair_Plots"" folder for the combinations")

def stackedBar_JSON_generator(path,cat_col):
    # Generating JSON using altair methods

    for i in range(len(cat_col)-1):
        chart=alt.Chart(df).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
            ).encode(x=cat_col[i], y='count():Q', color=cat_col[i+1])
        chart.save(path+'/StackedBar_'+str(cat_col[i])+" Vs "+str(cat_col[i+1])+"_"+"plot.json")
    print("Stacked Bar Graph JSON generated in ""Altair_Plots"" folder for the combinations")


if __name__ == "__main__":
    df1 = null_count(df)

    uniques = unique_value_list(df1)

    path = new_folder()

    write_unique_value_list(path, uniques)

    cat_col, num_col = dtypes_conversion(uniques)

 #   bar_JSON_generator(path, cat_col, num_col)

    stackedBar_JSON_generator(path, cat_col)