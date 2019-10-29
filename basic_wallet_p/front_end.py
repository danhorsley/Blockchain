from flask import Flask, render_template, request
import hashlib
import requests
import sys
import json
from flask_sqlalchemy import SQLAlchemy
from miner import *

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['ENV'] = 'debug'
# db = SQLAlchemy(app)
#db.create_all()

@app.route('/')
def getter():
   return render_template('basic.html')

@app.route('/', methods=['POST'])
def my_form_post():
    new_id = request.form['enter_id']
    return f'total mined coins is {new_id}'

if __name__ == '__main__':
    app.run()