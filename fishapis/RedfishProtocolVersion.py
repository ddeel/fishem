# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
RedfishProtocolVersion API Definitions.

Defines REST API behaviors for RedfishProtocolVersion.
Allows initial data for instances of this API object to be set.

Based upone Singleton template version 0.9.0
"""

# Standard library module imports
# None

# Third party module imports
from flask_restful import Resource      # REST operations
from flask import request               # JSON input from REST

# Local module imports
from fish_data import fish              # Fish data
import fishem_httpcodes as HTTP         # HTTP status codes

# Constants
# None

# Capabilities Restricions from unversioned schema
# (These items are read-only within the classes below)
#
# None

# The Redfish protocol version is stored in the fish object
# dictionary. It is defined here:
fish['/redfish'] = {
    'v1': '/redfish/v1/'
    }

class RedfishProtocolVersion(Resource):
    """Defines API behaviors for the Redfish protocol version.

    Defined: GET.

    flask_restful provides default support for HEAD and OPTIONS.
    It also provides a 405 (Method Not Allowed) response for any
    RESTful service requests that are not defined.
    """

    def __init__(self):
        """Handles class setup. Called by flask_restful prior to
        each and every REST operation handled by this class."""
        # End of __init__()

    def get(self):
        """Defines GET behavior. Called by flask_restful."""
        # Handle GET request
        inst_key = request.path
        # fish keys do not have trailing slashes
        if inst_key.endswith('/'):
            inst_key += '/'
            inst_key = inst_key.replace('//', '')
        # Ensure object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Return the requested object
        return fish[inst_key], HTTP.OK
        # End of get()

# Activate the API module
def activate(rest_api):
    """Registers URIs for this API module with flask_restful."""

    # Register the URIs that this API module responds to
    rest_api.add_resource(RedfishProtocolVersion,
        '/redfish',
        '/redfish/')

    return
    # End of activate()
