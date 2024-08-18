from model import encode,decrypt
import numpy
from numpy import asarray
from PIL import Image,ImageOps
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template,send_file
from werkzeug.utils import secure_filename
import sqlite3


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("intro.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("intro.html")
    else:
        return render_template("signup.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
       
        if file.filename == '':
            return render_template('index.html', error='No image uploaded!')
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],'download.jpg'))
            if request.form['go']=='encrypt':
                return redirect(url_for('image'))
            return redirect(url_for('decode1'))
        else:
            return render_template('index.html', error='Please upload an image file')
    
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        image1 = Image.open(UPLOAD_FOLDER+'download.jpg')
        msg=request.form['msg']
        x=encode(image1, msg)
        x.convert('RGB').save(UPLOAD_FOLDER+'new1.png')
        return send_file(UPLOAD_FOLDER+'new1.png', as_attachment=True)
    return render_template('encode.html')


@app.route('/decode')
def decode1():
    image1 = Image.open(UPLOAD_FOLDER+'download.jpg')
    msg1= decrypt(image1)
    return render_template('decode.html',msg=msg1)

if __name__ == '__main__':
   app.run(debug = True)

