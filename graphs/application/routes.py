from application import app 
from flask import render_template, Flask, redirect, request, url_for
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import io
matplotlib.use('agg')
from flask import Flask, send_file,render_template

df = pd.read_csv('dataset.csv')

@app.route("/")
def index():
    categ = []
    numer = []
    for col in df.columns:
        if df[col].dtypes == object:
            categ.append(col)
        else:
            numer.append(col)
    empty_list = []
    for i in categ:
        fig,ax = plt.subplots(1,1, figsize=(5,4))
        sns_plot = sns.countplot(x=df[i][1:])
        image = io.BytesIO()
        sns_plot.figure.savefig(image, format = 'png')
        image.seek(0)
        empty_list.append(send_file(image,mimetype = 'image/png' ))
        #b.append(empty_list)
    print(tuple(empty_list))

    return "hello"