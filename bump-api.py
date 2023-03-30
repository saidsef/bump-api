#!/usr/bin/env python3

import os
import logging
import tempfile
from json import dumps, loads
from flask import Flask, request, jsonify, Response
from flask_wtf.csrf import CSRFProtect
from subprocess import run, STDOUT, PIPE
from prometheus_flask_exporter import PrometheusMetrics

HOST = os.environ.get("POD_IP", "0.0.0.0")
PORT = os.environ.get("PORT", "7070")
app = Flask(__name__)
csrf = CSRFProtect()

csrf.init_app(app)
PrometheusMetrics(app, group_by='url_rule') # by URL rule

logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def version_path():
    tmpdir = tempfile.mkdtemp()
    file_name = 'VERSION'
    file_path = os.path.join(tmpdir, file_name)
    return file_path

def version_inc(path, msg):
    command = ["bump", "--filename", path, msg]
    result = run(command, stdout=PIPE, stderr=STDOUT)
    return result.stdout.decode().strip()


def version_update(path, v):
    with open(path, 'w') as fh:
        fh.write(v)


def version_out(path):
    with open(path, 'r') as fh:
        version = fh.readline()
    return version


@app.route('/', methods=['GET'])
def index():
  return jsonify(['{} {}'.format(list(rule.methods), rule) for rule in app.url_map.iter_rules() if 'static' not in str(rule)])


@app.route('/api/v1/version', methods=['GET', 'POST'])
def version():
    if request.method == 'POST':
        j = loads(request.get_data())
        current_version = j['current_version']
        commit_message = j['commit_message']
        file_path = version_path()
        version_update(file_path, current_version)

        for m in commit_message.split(" "):
            version_inc(file_path, m)

        new_version = version_out(file_path)
        out = {
            "new_version": new_version
        }
        return Response(dumps(out), 200, mimetype='application/json')
    else:
        return Response(dumps({'message': 'healthy'}), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
