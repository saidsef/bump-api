#!/usr/bin/env python

import os
import logging
import tempfile
from subprocess import check_output, STDOUT
from json import dumps, loads
from flask import Flask, request, jsonify

PORT  = os.environ.get("PORT")
app   = Flask(__name__)

logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def version_path():
    tmpdir = tempfile.mkdtemp()
    file_name = 'VERSION'
    file_path = os.path.join(tmpdir, file_name)
    return file_path

def version_inc(path, msg):
    return check_output("bump --filename {} {}".format(path, msg), stderr=STDOUT, shell=True)

def version_update(path, v):
    with open(path, 'w') as fh:
        fh.write(v)

def version_out(path):
    with open(path, 'r') as fh:
        version = fh.readline()
    return version

@app.route('/api/v1/version', methods=['GET', 'POST'])
def version():
    if request.method == 'POST':
        j = loads(request.get_data())
        current_version = j['current_version']
        commit_message  = j['commit_message']
        file_path = version_path()
        version_update(file_path, current_version)

        for m in commit_message.split(" "):
            version_inc(file_path, m)

        new_version = version_out(file_path)
        out = { "new_version": new_version }
        return dumps(out)
    else:
        return dumps({'message': 'healthy'})

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=PORT)
