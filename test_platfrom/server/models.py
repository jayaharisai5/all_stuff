from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()
#This function will automatically create the ids for the new user
def get_uuid():
    return uuid4().hex
#Creating the new model for the register with table name 'mla_users'
class User(db.Model):
    __tablename__ = 'mla_users'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid) #new user unique id
    mla_username = db.Column(db.String(345), unique=True, nullable=False)   #new user username ' it should be unique'
    mla_f_name = db.Column(db.Text, nullable=False)     #new user firstname
    mla_l_name = db.Column(db.Text, nullable=False)     #new user last name
    mla_user_organization = db.Column(db.Text, nullable=False)  #new user organization name
    mla_user_organization_email = db.Column(db.String(345), unique=True, nullable=False)    #new user organization email 'it should be unique'
    mla_user_mobile_number = db.Column(db.String(345), unique=True, nullable=False)     #new user mobile number 'it should be unique'
    mla_user_password = db.Column(db.String(1000))      #new user password  
    mla_user_comform_password = db.Column(db.String(1000))      #new user conform password
