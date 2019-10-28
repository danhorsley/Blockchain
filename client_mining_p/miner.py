import hashlib
import requests

import sys
import json

# *Client Mining*
# Create a client application that will:
# * Get the last block from the server
# * Run the `proof_of_work` function until a valid proof is found, validating or rejecting each attempt.  Use a copy of `valid_proof` to assist.
# * Print messages indicating that this has started and finished.
# * Modify it to generate proofs with *6* leading zeroes.
# * Print a message indicating the success or failure response from the server
# * Add any coins granted to a simple integer total, and print the amount of coins the client has earned
# * Continue mining until the app is interrupted.
# * Change the name in `my_id.txt` to your name
# * (Stretch) Handle non-json responses sent by the server in the event of an error, without crashing the miner
# * Stretch: Add a timer to keep track of how long it takes to find a proof


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    def proof_of_work(block):
 
        stringify = json.dumps(block, sort_keys = True)
        proof_guess = 0
        while valid_proof(stringify, proof_guess) is False:
            proof_guess += 1
            
        return proof_guess


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
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

        return hash_try[:6] == '000000'


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
