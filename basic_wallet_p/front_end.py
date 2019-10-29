from flask import Flask, render_template, request
import hashlib
import requests
import sys
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'debug'
DB.init_app(app)

@app.route('/')
def getter():
   return render_template('basic.html')

@app.route('/', methods=['POST'])
def my_form_post():
    new_id = request.form['enter_id']
    #print(type(new_id))
    with open("dan_horsley.txt", "w") as f:
        f.writelines(new_id)
    my_query = DB.session.query(func.sum(trdb.amt)).filter_by(recipient = new_id).first()[0] #(trdb.recipient == "12345")
    all_transactions = trdb.query.filter_by(recipient = new_id).all()
    print(type(all_transactions), all_transactions)
    #for item in trdb.
    # return f'''total mined coins for id {new_id}  is {my_query}.  
    #             complete history of transactions is : {all_transactions}'''

    return render_template('render.html', newid = new_id, total_amt = my_query, allt = all_transactions)

if __name__ == '__main__':
    app.run(host='172.23.121.54', port=5000)