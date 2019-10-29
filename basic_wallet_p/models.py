from flask_sqlalchemy import SQLAlchemy
from time import time
#from blockchain import DB

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users that we pull and analyse tweets for"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    coins_mined = DB.Column(DB.String(15), nullable = False)
    newest_tweet_id=DB.Column(DB.BigInteger)
  
    def __repr__(self):
        return '<User {}>'.format(self.name)

class Chain_DB(DB.Model):
    """maintains the list of blocks in the form
    block = {'index' : len(self.chain) + 1,'time' : time(), 'current_transactions': self.current_transactions, 
                 'proof' : proof, 'previous_hash' : previous_hash}"""
    index = DB.Column(DB.BigInteger, primary_key=True)
    time = DB.Column(DB.Float)
    cur_tran = DB.Column(DB.Text)
    proof = DB.Column(DB.BigInteger)
    prev_hash = DB.Column(DB.Text)
  
    # def __repr__(self):
    #     return '<User {}>'.format(self.name)

class trdb(DB.Model):
    """maintains the list of transactions in the form
    nt = {'sender' : sender, 'recipient' : recipient,
                 'amount' : amount, 'index' : self.chain[-1]['index']}"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    sender = DB.Column(DB.Text)
    recipient = DB.Column(DB.Text)
    amt = DB.Column(DB.Integer)
    index = DB.Column(DB.BigInteger)

    def __init__(self, sender, recipient, amt, index):
        self.id=time()
        self.sender = sender
        self.recipient = recipient
        self.amt = amt
        self.index = index
    
    def __repr__(self):
         return '<sender {}, recipient {}, amount {}, index {}>'.format(self.sender,
                                                                        self.recipient,
                                                                        self.amt,
                                                                        self.index)
  
