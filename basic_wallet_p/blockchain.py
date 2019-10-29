# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4
import requests

from flask import Flask, jsonify, request
from models import *
import os.path




class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):


        block = {'index' : len(self.chain) + 1,'time' : time(), 'current_transactions': self.current_transactions, 
                 'proof' : proof, 'previous_hash' : previous_hash}
    

        self.current_transactions = []
        self.chain.append(block)

        
        return block

    def hash(self,block):

        block = json.dumps(block, sort_keys = True).encode()
        my_hash = hashlib.sha224(block).hexdigest()

        return my_hash

    @property
    def last_block(self):
        return self.chain[-1]
    

    @staticmethod
    def valid_proof(block_string, proof):
 
        new_string = (block_string + str(proof)).encode()
        hash_try = hashlib.sha256(new_string).hexdigest()
        
        return hash_try[:3] == '000'

    def new_transaction(self,sender, recipient, amount):
        # :param sender: <str> Address of the Recipient
        # :param recipient: <str> Address of the Recipient
        # :param amount: <int> Amount
        # :return: <int> The index of the `block` that will hold this transaction
        nt = {'sender' : sender, 'recipient' : recipient,
                 'amount' : amount, 'index' : self.chain[-1]['index']}

        self.current_transactions.append(nt)
        new_DB_tran = trdb(sender = nt['sender'],
                                        recipient = nt['recipient'],
                                        amt = nt['amount'],
                                        index = nt['index'])
        DB.session.add(new_DB_tran)
        DB.session.commit()
        return nt

# Instantiate our Node
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'debug'
#DB = SQLAlchemy(app)
DB.init_app(app)


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():#request): 
    # Modify the `mine` endpoint to create a reward via a `new_transaction`
    # for mining a block:

    #The sender is "0" to signify that this node created a new coin
    #The recipient is the id of the miner
    #The amount is 1 coin as a reward for mining the next block
    data = request.get_json()
    if 'proof' in data.keys() and 'id' in data.keys():
        lastblockstring = json.dumps(blockchain.chain[-1], sort_keys = True)
        
        if blockchain.valid_proof(lastblockstring, int(data['proof'])):
            prevhash = blockchain.hash(blockchain.chain[-1])
            blockchain.new_block(int(data['proof']),prevhash)
            response = {'message' : 'New Block Forged'}
            reward = blockchain.new_transaction('0',request.remote_addr,'1')
            node = 'http://127.0.0.1:5000'
            requests.post(url=node + "/transactions/new", json=reward)
            response_id = 200
        else:
            response = {'message' : 'incorrect proof'}
            response_id = 400
    else:
        response = {'message' : 'proof or id not included'}
        response_id = 400

    return jsonify(response), response_id

@app.route('/last_block', methods=['GET'])
def last():
    response = blockchain.last_block

    return jsonify(response), 200

@app.route('/create_DB')
def cdb():
    DB.drop_all()
    DB.create_all()

    return 'DB reset'

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length' :len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_t():
    sender = request.remote_addr
    # check that 'sender', 'recipient', and 'amount' are present
    #  return a 400 error using `jsonify(response)` with a 'message'
    # upon success, return a 'message' indicating index of the block
    # containing the transaction
    data = request.get_json()
    if 'sender' in data.keys() and 'recipient' in data.keys() and 'amount' in data.keys():
        index = str(blockchain.chain[-1]['index'])
        return jsonify({'message' : index}),200
    else:
        return jsonify({'message' : 'missing json'}),400


# Run the program on port 5000
if __name__ == '__main__':
    app.run()
    #from models import trdb #host='0.0.0.0', port=5000)

