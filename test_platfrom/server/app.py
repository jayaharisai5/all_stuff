from flask import Flask, request, abort, jsonify, session
from flask_bcrypt import Bcrypt
import bcrypt
from config import ApplicationConfig
#impeortinfg the model.py file from that file we are importing models that we are created
from models import db, User
from flask_cors import CORS, cross_origin
from itertools import chain  #converting the 2d list to 1d list 
import boto3 #to do something in aws
import pandas as pd #for manipulation

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app) #it is a password hashing function to hash the password 
CORS(app, supports_credentials=True)  # here we are using cors to fetch the data from the front end
db.init_app(app) #initilizating the application
#db.create_all()

with app.app_context():
    db.create_all() #creating the tables


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error":"Unauthorized"})
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'id': user.id,
        'mla_username': user.mla_username
    })

#Creating a register form API
@app.route('/mla_register', methods=['POST', 'GET'])
def register_user():
    mla_username = request.json['mla_username']     #new user name that we want to display
    mla_f_name = request.json['mla_f_name']     #user firstname
    mla_l_name = request.json['mla_l_name']     #User Lastname
    mla_user_organization = request.json['mla_user_organization']       #user organization
    mla_user_organization_email = request.json['mla_user_organization_email']   #user organization email
    mla_user_mobile_number = request.json['mla_user_mobile_number']     #his mobile number
    mla_user_password = request.json['mla_user_password']       #password   
    mla_user_comform_password = request.json['mla_user_comform_password']       #COnform password
    #Here we are checking weather the user is present in the past
    mla_new_user_exist = User.query.filter_by(mla_username=mla_username).first() is not None 
    #if he is exested mla_new_user_exist will be true
    if mla_new_user_exist:
        abort(409)
        return jsonify({'User already exists'})
    #print("------------------------" + mla_user_password)
    #Checking the password and conform password is same or not 
    if mla_user_password == mla_user_comform_password:
        print("Password Matched")   
        hashed_password = bcrypt.generate_password_hash(mla_user_password)  #if the passwords are mached then we will create a hashes to the password for protection
        mla_new_user = User(mla_username=mla_username, mla_f_name=mla_f_name, mla_l_name=mla_l_name, 
                        mla_user_organization=mla_user_organization, mla_user_organization_email=mla_user_organization_email,
                        mla_user_mobile_number=mla_user_mobile_number, mla_user_password=hashed_password, mla_user_comform_password=hashed_password)
        db.session.add(mla_new_user) #adding to the data base
        db.session.commit() #Commiting to the data base
    else:
        print("Password not matched")  # if the password dontnot matches there will shown this error
    
    #finally it will return these details
    return jsonify({
        'id': mla_new_user.id,
        'mla_f_name': mla_new_user.mla_f_name,
        'mla_l_name': mla_new_user.mla_l_name,
        'mla_user_organization': mla_new_user.mla_user_organization,
        'mla_user_organization_email': mla_new_user.mla_user_organization_email
    })

#Function and route for the user login
@app.route("/mla_login",  methods=['POST'])
def login_user():
    mla_username = request.json['mla_username']  #asking exesting username
    mla_user_password = request.json['mla_user_password'] #password

    user  = User.query.filter_by(mla_username=mla_username).first()  #filtering based on the uername
    #if the user is not present then we will shoe the error
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    #if the user is present but password is wrong we will throw the error
    if not bcrypt.check_password_hash(user.mla_user_password, mla_user_password):
        return jsonify({"error": "Unauthorized"}), 401
    #Session is noting but after login sucessfull we need to kee the user session until he want to logout
    session["user_id"] = user.id
    #sucessull login we will return these details
    return jsonify({
        'id': user.id,
        'mla_username': user.mla_username
        
    })

def Merge(dict1, dict2):
    return(dict2.update(dict1))


@app.route("/data_retrevel", methods = ["POST", "GET"])
def data_retrevel():
    aws_access_key_id = request.json['aws_access_key_id']  #from user we are getting the aws access id
    aws_secret_access_key = request.json['aws_secret_access_key']  #from user we are getting the aws access key
    region_name = request.json['region_name'] #user region name
    bucket_name = request.json['bucket_name'] #usetr bucket name
    #connecting to s3
    
    s3 = boto3.resource(
                    's3',
                    aws_access_key_id= aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                    )
    #session["s3"] =s3
    session["aws_access_key_id"] = aws_access_key_id
    session["aws_secret_access_key"] = aws_secret_access_key
    session["region_name"] = region_name
    session["bucket_name"] = bucket_name
    
    print("error")
    objects = []
    #session["s3"] = s3

    for obj in s3.Bucket(bucket_name).objects.all():
                    print(obj.key)
                    objects.append(obj.key)
    

    return jsonify(objects)

@app.route("/user", methods = ["POST", "GET"])
def data():
    object = request.json['object']
    aws_access_key_id = request.json['aws_access_key_id']  #from user we are getting the aws access id
    aws_secret_access_key = request.json['aws_secret_access_key']  #from user we are getting the aws access key
    region_name = request.json['region_name'] #user region name
    bucket_name = request.json['bucket_name'] #usetr bucket name

    s3 = boto3.resource(
                    's3',
                    aws_access_key_id= aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                    )
    obj = s3.Bucket(bucket_name).Object(object).get()
    foo = pd.read_csv(obj['Body'], index_col=0)

    print(foo)
    #session["foo"] = foo

    print(object)

            
    return jsonify('Sucessful')


@app.route("/read_data", methods = ["POST", "GET"])
def read_data():
    object = request.json['object']
    aws_access_key_id = request.json['aws_access_key_id']  #from user we are getting the aws access id
    aws_secret_access_key = request.json['aws_secret_access_key']  #from user we are getting the aws access key
    region_name = request.json['region_name'] #user region name
    bucket_name = request.json['bucket_name'] #usetr bucket name

    s3 = boto3.resource(
                    's3',
                    aws_access_key_id= aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                    )
    obj = s3.Bucket(bucket_name).Object(object).get()
    foo = pd.read_csv(obj['Body'], index_col=0)
    print(foo.head())

    return jsonify("hello")
    
if __name__ == "__main__":
    app.run(debug=True)