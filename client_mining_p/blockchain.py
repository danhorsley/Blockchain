# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {'index' : len(self.chain) + 1,'time' : time(), 'current_transactions': self.current_transactions, 
                 'proof' : proof, 'previous_hash' : previous_hash}
    

        # Reset the current list of transactions
        # Append the chain to the block
        # Return the new block
        self.current_transactions = []
        self.chain.append(block)
        #self.new_block = block
        
        return block

    def hash(self,block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        block = json.dumps(block, sort_keys = True).encode()
        my_hash = hashlib.sha224(block).hexdigest()
       
        
        
        return my_hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     stringify = json.dumps(block, sort_keys = True)
    #     proof_guess = 0
    #     while self.valid_proof(stringify, proof_guess) is False:
    #       proof_guess += 1
          
    #     return proof_guess

          
          

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        new_string = (block_string + str(proof)).encode()
        hash_try = hashlib.sha256(new_string).hexdigest()
        
        return hash_try[:3] == '000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine(request):
    # * Modify the `mine` endpoint to instead receive and validate or 
    # reject a new proof sent by a client.
    # It should accept a POST
    # Use `data = request.get_json()` to pull the data out of the POST
    # Note that `request` and `requests` both exist in this project
    # Check that 'proof', and 'id' are present
    # return a 400 error using `jsonify(response)` with a 'message'
    data = request.get_json()
    if 'proof' in data.keys() and 'id' in data.keys():
        lastblock = blockchain.chain[-1]
        if blockchain.valid_proof(lastblock, data['proof']):
            response = 'validated'
            response_id = 200
        else:
            response = 'incorrect proof'
            response_id = 400
    else:
        response = 'proof or id not included'
        response_id = 400

    return jsonify(response), response_id

@app.route('/last_block', methods=['GET'])
def last():
    response = blockchain.last_block()

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length' :len(blockchain.chain)
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run()#host='0.0.0.0', port=5000)
