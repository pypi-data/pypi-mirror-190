import os
from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
import requests
import json
import datetime
import time
import uuid
import random
from kraken_image_processing import kraken_image_processing as k   


# Initalize app
test_mode = False


# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/', methods=['GET'])
def main_get():

    if 1==0:
        url = 'https://krakenimageprocessing.tactik8.repl.co/api'
        files = {'file': open('test3.jpg', 'rb')}
    
        params = {'@type':'schema:imageObject', '@id': 'some_id'}
        #data = json.dumps(record, default = str)
    
        r = requests.post(url, params=params, files=files)
        #print(json.dumps(r.json(), indent=4))

    if 1==1:
        url = 'https://krakenimageprocessing.tactik8.repl.co/api'
        
    
        params = {'@type':'schema:imageObject', '@id': 'some_id'}
        #data = json.dumps(record, default = str)
        headers = {'content-type': 'applicaiton/json'}
        r = requests.post(url, headers=headers, params=params)
        #print(json.dumps(r.json(), indent=4))


    
    return Response('ok')


@app.route('/api', methods=['GET'])
def api_get():
    """Process get data
    """

    return Response('ok')


@app.route('/api', methods=['POST'])
def api_post():
    """Process get data
    """
    print('Post')
    file = None
    try:
        file = request.files['file'].read()
    except:
        a=1
        
    record = {
        '@type': request.values.get('@type'),
        '@id': request.values.get('@id'),
        'schema:contentUrl': 'https://suburbanmen.com/wp-content/uploads/2023/01/suburban-men-instagram-crush-jessie-cushing-20230125-122.jpg'
        }

    records = k.process(record, file)
    
    return jsonify(records)

   





def run_api():
    app.run(host='0.0.0.0', debug=False)

