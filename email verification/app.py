from flask import Flask, request, url_for
from flask_mail import Mail, Message 
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os 


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bjusten420@gmail.com'
app.config['MAIL_PASSWORD'] = '4821_neWpassword55'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

s = URLSafeTimedSerializer('Thisisasecret!')

mail = Mail(app)

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == "GET":
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    email = request.form['email']
    token = s.dumps(email, salt='email-conform')
    
    msg= Message('Conform Email', sender='bjusten420@gmail.com', recipients=[email])
    link = url_for('conform_email', token=token, externam=True)

    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)


    return '<div>Your email: {}</div><div>Token: {}</div>'.format(email, token)


#route that handle token
@app.route('/conform_email/<token>')
def conform_email(token):
    try:
        email = s.loads(token, salt='email-conform', max_age=20)
    except SignatureExpired:
        return '<p>Token expired</p>'
    return 'The token works!'

if __name__ == '__main__':
    app.run(debug=True)