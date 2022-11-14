from dotenv import load_dotenv
import os 

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    #It will just stop the logging the useless messages
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    #echo the sql where ever there is a change in the data base
    SQLALCHEMY_ECHO = True 
    #here we are using sqllite
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"