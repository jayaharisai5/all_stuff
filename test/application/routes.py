from application import app 
from flask import render_template, Flask, redirect, request, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import json 
import plotly 
import plotly.express as px
import pickle
file = []
data = pd.read_csv('healthcare-dataset-stroke-data.csv')

@app.route("/upload")
def index():
    return render_template("index.html")
pickle_in = pickle.load(open("finalised_model.pkl","rb"))

columns = pickle_in.feature_names_in_
col = []
for i in columns:
    print(i)
    col.append(i)




@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        file_name = f.filename
        file.append(file_name)
        print(file[0])
        data_csv = pd.read_csv(file[0])
        print(data_csv)
        message = "Sucessfull"
        condition = True
        return render_template("index.html", message=message, file_name=file_name, condition=condition)


@app.route('/cleaning', methods = ['GET', 'POST'])
def cleaning():
    method = "Handling with null values"
    null = data.isnull().sum()
    analysis = "Analysis"
    print(null)
    columns = data.columns
    null_array=[]
    for u in null:
        print(u)
        null_array.append(u)
    print(columns[1])
    total_null = data.isnull().sum().sum()
    len_col = len(columns)
    if total_null == 0:
        print("TOtal zero")
        condition = 'disabled'
        message = "There are no null values"
        return render_template("cleaning.html", null_array=null_array, columns=columns, len_col=len_col,
        method=method, total_null=total_null, analysis=analysis,  condition=condition)
        
    else:
        if request.method == 'POST':
            if request.form.get('action1') == 'REPLACE':
                #print("HEllo")
                title = 'REPLACE'
                message = 'Start replacing'
                options = True
                return render_template("cleaning.html", title=title, message=message, null_array=null_array, columns=columns, len_col=len_col,
        method=method, total_null=total_null, analysis=analysis, options=options)
            elif  request.form.get('action2') == 'REMOVE':
                #print("HEllllllo")
                title = 'REMOVE'
                message = 'Start removing'
                optionss = True
                return render_template("cleaning.html", title=title, message=message, null_array=null_array, columns=columns, len_col=len_col,
        method=method, total_null=total_null, analysis=analysis, optionss=optionss)
            else:
                pass # unknown  
    

    return render_template("cleaning.html", null_array=null_array, columns=columns, len_col=len_col,
        method=method, total_null=total_null, analysis=analysis)


@app.route('/replace', methods = ['GET', 'POST'])
def replace():
    if request.method == "POST":
        option = request.form["option"]

        option = int(option)
        print(type(option))
        return render_template("duplicates.html")
    else:
        return render_template("cleaning.html")
    return render_template("cleaning.html")

@app.route('/remove', methods = ['GET', 'POST'])
def remove():
    if request.method == "POST":
        option = request.form["option"]
        option = int(option)
        print(type(option))
        if option ==1:
            print("You have selected "+ str(option))
            data.dropna(inplace=True)
            print(data.head())
            print(data.isnull().sum())
        elif option == 2:
            print("You have selected "+ str(option))
        elif option ==3:
            print("You have selected "+ str(option))
        else:
            return render_template("cleaning.html")
        return render_template("duplicates.html")
    else:
        return render_template("cleaning.html")
    return render_template("cleaning.html")

import plotly.express as px


@app.route('/visuavalize', methods = ['GET', 'POST'])
def visuavalize():
    print(col)
    if request.method == "POST":
        #user = request.form["name"]
        '''
        df = pd.DataFrame({
            'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
            'Bananas'],
            'Amount': [4, 1, 2, 2, 4, 5],
            'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
        })'''
        option_one = request.form["option_one"]
        option_two = request.form["option_two"]
        print(option_one, option_two)
        
        fig = px.bar(data, x=option_one, y=option_two, barmode='group')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template("visuavalize.html", col=col, option_one = option_one, option_two=option_two, graphJSON=graphJSON)
    else:
        return render_template("visuavalize.html", col=col)
     
@app.route('/duplicates')
def duplicates():
    return render_template("duplicates.html")