from functools import wraps
from http import client
from flask import Flask, redirect, render_template, session
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "b\xdc\xa0\x14\x7f6\xeb)\x97U\xb9S2\\\xdf\xa8\x15"

#Databases

cluster = MongoClient("mongodb+srv://DEMODOGS:DEMODOGS@demodogs-apad.4aejn.mongodb.net/?retryWrites=true&w=majority")
db = cluster["APAD"]
users = db["user_table"]
resource = db["resource_table"]
transactions = db["transaction_table"]
projects = db["project_table"]

# client = pymongo.MongoClient(app)
# db = client.users_table

# Login required functions (decorators)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

#Routes import
from user import routes


@app.route('/')
def home():
    return render_template('home.html')
    
# @app.route('/dashboard/')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

#commented above function - for your review @Dhruv P.

@app.route("/dashboard/", methods = ['GET'])
@login_required
def hardware():
    try:
        hardware = resource.find_one({})
        return render_template('dashboard.html', hardware = hardware)
    except Exception as e:
        return print({'error' : str(e)})


@app.route("/project/",methods = ['GET'])
def project():
    return render_template('project.html')

if __name__ == '__main__':
    app.run(debug=True)