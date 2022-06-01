import logging
import json
import re

from flask import Blueprint, jsonify, request, current_app as app
from flask import Flask

appy = Flask(__name__)
log = logging.getLogger(__name__)

build_api = Blueprint('build_api', __name__)

@build_api.route('/builds', methods=['POST'])
def builds():
    if not request.content_type == 'application/json':
        message = 'invalid request: Content-Type must be application/json'
        log.error(message)
        return jsonify({'error': message} ), 400

    # ensure valid json
    try:
        req_data = json.loads(request.data)
    except ValueError:
        return jsonify({'error': 'invalid json'}), 400

    jobs =  req_data.get('jobs')
    if not jobs:
        return jsonify({'error': 'invalid payload: expects key: jobs'}), 400

    build_base = jobs.get('Build base AMI')
    if not build_base:
        return jsonify({'error': 'invalid payload: expects key: Build base AMI'}), 400

    latest = {
        'build_date': 0,
        'ami_id': '',
        'commit_hash': ''
    }

    build_list = build_base.get('Builds')
    for build in build_list:

        # ensure all keys are present
        if not all (k in build for k in ['result', 'output', 'build_date']):
            log.warn('No result or output or build_date in list item')
            continue

        # Get only successful builds
        if build.get('result') != 'SUCCESS':
            log.debug('result is not SUCCESS. Skipping')
            continue

        build_date = build.get('build_date')

        # only update if build_date is more recent
        if not build_date > latest.get('build_date'):
            continue

        b_output = parse_output((build.get('output')))
        if b_output:
            latest['ami_id'] = b_output.get('ami_id')
            latest['commit_hash'] = b_output.get('commit_hash')
            latest['build_date'] = build_date
        else:
            log.debug('build does not have proper output format')

    if latest.get('build_date') == 0:
        return jsonify({'error': 'No latest build found'})
    else:
        return jsonify({'latest': latest})

def parse_output(build_output):
    """
    parse_output expects a string of format:
    base-ami us-west-2 ami-XXXXXXXX <hash>
    returns a dict with ami_id and commit_hash
    """
    regex_statement = 'base-ami us-west-2 (ami-[a-zA-Z0-9]*) ([a-zA-Z0-9]*)$'
    r = re.match(regex_statement, build_output)
    if r:
        ami_id = r.group(1)
        commit_hash = r.group(2)

        return {
            'ami_id': ami_id,
            'commit_hash': commit_hash,
        }
    else:
        return None

appy.run(debug=True)