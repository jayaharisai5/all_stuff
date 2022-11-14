from application import app 
from flask import render_template, Flask, redirect, request, url_for
from werkzeug.utils import secure_filename
import pandas as pd

from cleaning import read_csv, handling_null_values, replace, remove




df = pd.read_csv('healthcare-dataset-stroke-data.csv')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        file_name = f.filename
        message = "Sucessfull"
        condition = True
        return render_template("index.html", message=message, file_name=file_name, condition=condition)

@app.route('/cleaning', methods = ['GET', 'POST'])
def cleaning():
    print(df)
    columns, null_array, length, adition_null, shape = handling_null_values()
    if adition_null == 0:
        disable = 'disabled'
        condition = True
    else:
        disable = "none"
        condition = False

    if request.method == 'POST':
        if request.form.get('action1') == 'REPLACE':
            print('replace')
            replace = True
            return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            replace=replace, shape=shape)
        elif  request.form.get('action2') == 'REMOVE':
            print('remove')
            remove = True
            return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            remove=remove, shape=shape)
        elif request.form.get('action3') == 'REPLACE_HERE':
            print('Replacing')
            option = request.form["option"]
            option = int(option)
            print(type(option))
            if option == 1:
                print('Replace null/Nan values with mean')
                message = 'Replace null/Nan values with mean'
                column_means = df.mean()
                df.fillna(column_means, inplace=True)
                after_shape = df.shape
                duplicates = True
                return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            option=option, message=message, shape=shape, after_shape=after_shape, column_means=column_means, duplicates=duplicates)
            elif option == 2:
                print('Replace null/Nan values with median')
                message = 'Replace null/Nan values with median'
                column_median = df.median()
                df.fillna(column_median, inplace=True)
                after_shape = df.shape
                duplicates = True
                return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            option=option, message=message, shape=shape, after_shape=after_shape, column_median=column_median, duplicates=duplicates)
            else:
                message = "There is no option you have selected"
            return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            option=option, message=message, shape=shape)
        elif request.form.get('action4') == 'REMOVE_HERE':
            print('Replacing')
            option = request.form["option"]
            option = int(option)
            print(type(option))
            if option == 1:
                print('Drop All Rows with any Null/NaN/NaT Values')
                message = 'Drop All Rows with any Null/NaN/NaT Values'
                df.dropna(inplace=True)
                after_shape = df.shape
                duplicates = True
            elif option == 2:
                print('Drop All Columns with Any Missing Value')
                message = 'Drop All Columns with Any Missing Value'
                df.dropna(axis=1, inplace=True)
                after_shape = df.shape
                duplicates = True
            elif option == 3:
                print('Dropping rows or columns only when all values are null')
                message = 'Dropping rows or columns only when all values are null'
                df.dropna(axis=0, how='all', inplace=True)
                after_shape = df.shape
                duplicates = True
            else:
                message = "There is no option you have selected"
            return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
            option=option, message=message, shape=shape, after_shape=after_shape, duplicates=duplicates)
        
    return render_template("cleaning.html", columns=columns, null_array=null_array, length=length, adition_null=adition_null,
    disable=disable, condition=condition, shape=shape)

@app.route('/duplicate', methods = ['GET', 'POST'])
def duplicate():
    duplicate = df.duplicated().sum().sum()
    if duplicate == 0:
        condition = True
        con = False
        message = 'There are no duplicates'
        return render_template("duplicates.html", condition=condition, message=message, con=con)
    else:
        con = True
        if request.method == 'POST':
            if request.form.get('action4') == 'DUPLICATE_HERE':
                print("Hello")
                option = request.form["option"]
                option = int(option)
                print(option)
                if option == 1:
                    df.drop_duplicates(inplace=True)
                    duplicates_after = df.duplicated().sum().sum()
                else:
                    print("No action")
            return render_template("duplicates.html", duplicates_after=duplicates_after)
        return render_template("duplicates.html", con=con)
    return render_template("duplicates.html")

@app.route('/outliers')
def outliers():
    return render_template('outliers.html')

@app.route('/labelencoding')
def labelencoding():
    message = "Start with label encoding "
    categorical = df.select_dtypes(exclude='number')
    return render_template('labelencoding.html', message=message)


@app.route('/sampling')
def sampling():
    return render_template('sampling.html')

@app.route('/traintestsplit')
def traintestsplit():
    return render_template('train_test_split.html')