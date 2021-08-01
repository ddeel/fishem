# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
Initialize and launch REST operations for fishem.
"""

# Standard library module imports
import json                     # JSON handling
import importlib                # API module imports
import os                       # CLI and file I/O handling

# Third party module imports
from flask import Flask, make_response  # REST operations
from flask_restful import Api           # REST operations

# Local module imports
# Note: API modules are programmatically imported in startup()


# Function: startup()

def startup(config):
    """Sets up Flask and Flask-RESTful, registers all fish URIs,
    and starts REST operations. Called only by fishem.py. Input
    argument 'config' is a dictionary that holds all necessary
    input arguments.
    """

    # Create Flask and Flask-RESTful instances
    flask_app = Flask(config['name'])
    rest_api = Api(flask_app)

    # Make output more readable on browsers without JSON plugins
    @rest_api.representation('application/json')
    def output_json(data, code, headers=None):
        """Set Flask-RESTful indents to 4 for JSON output
        """
        resp = make_response(json.dumps(data, indent=4), code)
        resp.headers.extend(headers or {})
        return resp

    # Set up URIs for all fishem API modules
    mod_count = 0
    for dirpath, dirnames, filenames in os.walk('fishapis'):
        if dirpath == 'fishapis':
            for fn in filenames:
                # Import API module to get access to its functions
                if fn == '__init__.py': continue
                mod_name = 'fishapis.' + fn.replace('.py', '')
                api_mod = importlib.import_module(mod_name)
                # Tell the API module to register its URIs
                api_mod.activate(rest_api)
                # Provide a simple progress indicator
                if mod_count % 5 == 0:
                    print('.', sep='', end='', flush=True)
                mod_count += 1
    print(' (', mod_count, ' API modules)', sep='')
    print('fishem running -----------------------------------------')

    # TODO: Finish adding HTTPS support

    # Launch RESTful operations
    flask_app.run(host='0.0.0.0', port=config['port'])

    # End of startup()
