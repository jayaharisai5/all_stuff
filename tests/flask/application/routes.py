from application import app 
from flask import render_template, Flask, redirect, request, url_for
from create_ini import create_ini
import configparser
import boto3
config_reader = configparser.ConfigParser()
config_reader.read('account.ini')
config_reader.read('bucket.ini')
config_reader.read('key.ini')
config_reader.read('sql.ini')
config_writer = configparser.ConfigParser()

import pandas as pd
import numpy as np 
import mysql.connector as sql 

tabless = []
try:
    db_connection = sql.connect(

        host = config_reader["sql"]['localhost'], 
        database = config_reader["sql"]['database_name'], 
        user = config_reader["sql"]['user'], 
        password=config_reader["sql"]['password'])
    db_cursor = db_connection.cursor()
    tables = pd.read_sql_query(sql = "SHOW TABLES FROM CSV", con = db_connection)
    #print(tables.Tables_in_csv)
    for i in tables.Tables_in_csv:
        #print(i)
        tabless.append(i)
    #print(tables[1])
    
except:
    print("error")

print(tabless)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/connect", methods =["GET", "POST"])
def connect():
    if request.method == "POST":
        if request.form.get('action1') == 'Click here':
            print('Connect to s3')
            s3 = True
            db = False
            upload = False
            return render_template('connect.html', s3=s3, db=db, upload=upload)
        elif request.form.get('action2') == 'Click here':
            database_option = request.form['database_option']
            print("Connect to database: " + database_option)
            s3 = False
            db = True
            upload = False
            if database_option == "mysql":
                mysql = True 
                snowflake = False
            elif database_option == "snowflake":
                mysql = False 
                snowflake = True
            return render_template('connect.html', s3=s3, db=db, upload=upload, database_option=database_option, mysql=mysql, snowflake=snowflake)
        elif request.form.get('action7') == 'Submit':
            print("mysql")
            localhost = request.form.get('localhost')
            database_name = request.form.get('database_name')
            user = request.form.get('user')
            password = request.form.get('password')

            config_writer['sql'] = {}
            config_writer['sql']['localhost'] = localhost
            config_writer['sql']['database_name'] = database_name
            config_writer['sql']['user'] = user
            config_writer['sql']['password'] = password
            with open('sql.ini', 'w') as configfile:
                config_writer.write(configfile)
            print(localhost, database_name, user, password)

            databasee = True
            return render_template('connect.html', tabless = tabless, databasee=databasee)
        elif request.form.get('action8') == 'Submit':
            print("snowflake")
            return render_template('connect.html')
        elif request.form.get('action9') == 'Select table':
            table_option = request.form['table_option']
            print(table_option)
            query = 'select * from ' + table_option ;
            df = pd.read_sql(sql=query, con=db_connection)
            print(df)
            databasee = True
            return render_template('connect.html', databasee=databasee, tabless = tabless)
        elif request.form.get('action3') == 'Click here':
            print('Upload your file')
            s3 = False
            db = False
            upload = True
            return render_template('connect.html', s3=s3, db=db, upload=upload)
        elif request.form.get('action4') == 'Submit':
            bucket_key = True
            aws_access_key_id = request.form.get("aws_access_key_id")
            aws_secret_access_key = request.form.get("aws_secret_access_key")
            region_name = request.form.get("region_name")

            create_ini(aws_access_key_id, aws_secret_access_key, region_name)
            try:
                s3 = boto3.resource(
                    's3',
                    aws_access_key_id= config_reader["Account"]['aws_access_key_id'],
                    aws_secret_access_key=config_reader["Account"]['aws_secret_access_key'],
                    region_name=config_reader["Account"]['region_name']
                    )
                bucket_name = []
                bucket_length = len(bucket_name)
                for bucket in s3.buckets.all():
                    bucket_name.append(bucket.name)
                print(bucket_name)
                return render_template('connect.html', bucket_key=bucket_key, bucket_name=bucket_name)
            except:
                print("Error")
            return render_template('connect.html', bucket_key=bucket_key)
        elif request.form.get('action5') == 'Check objects':
            bucket_option = request.form['bucket_option']
            try:
                s3 = boto3.resource(
                    's3',
                    aws_access_key_id= config_reader["Account"]['aws_access_key_id'],
                    aws_secret_access_key=config_reader["Account"]['aws_secret_access_key'],
                    region_name=config_reader["Account"]['region_name']
                    )
                bucket_name = []
                bucket_length = len(bucket_name)
                for bucket in s3.buckets.all():
                    bucket_name.append(bucket.name)
                print(bucket_name)

                objects = []
                for obj in s3.Bucket(bucket_option).objects.all():
                    print(obj.key)
                    objects.append(obj.key)
                return render_template('connect.html', bucket_key=bucket_key, key=key, bucket_name=bucket_name,
            objects=objects)
            except:
                print("Error")
            
            #print(bucket_option)
            
            bucket_key = True
            key = True
            config_writer['Account'] = {}
            config_writer['Account']['bucket'] = bucket_option
            with open('bucket.ini', 'w') as configfile:
                config_writer.write(configfile)
            return render_template('connect.html', bucket_key=bucket_key, key=key, bucket_name=bucket_name,
            objects=objects)
        elif request.form.get('action6') == 'Submit':
            try:
                s3 = boto3.resource(
                    's3',
                    aws_access_key_id= config_reader["Account"]['aws_access_key_id'],
                    aws_secret_access_key=config_reader["Account"]['aws_secret_access_key'],
                    region_name=config_reader["Account"]['region_name']
                    )
                bucket_name = []
                bucket_length = len(bucket_name)
                for bucket in s3.buckets.all():
                    bucket_name.append(bucket.name)
                print(bucket_name)
                sucess = True
                return render_template('connect.html', bucket_key=bucket_key, bucket_name=bucket_name, sucess=sucess)
            except:
                print("Error")
            key_option = request.form['key_value']
            print(key_option)
            bucket_key = True
            key = True
            config_writer['Account'] = {}
            config_writer['Account']['key'] = key_option
            with open('key.ini', 'w') as configfile:
                config_writer.write(configfile)
            sucess = True
            return render_template('connect.html', bucket_key=bucket_key, key=key, bucket_name=bucket_name, sucess=sucess)
        else:
            print("Error")
    return render_template('connect.html')

@app.route("/data")
def data():
    return render_template('data.html')