# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
RedfishODataService API Definitions.

Defines REST API behaviors for RedfishODataService.
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

# The Redfish OData service document is stored in the fish object
# dictionary. The key '/redfish/v1/odata' should only be defined
# when a valid odata service document is present. It can be defined
# here (see below) or by loading fishem from a mockup or a fish file.
# Mockups and fish files loaded into fishem can overwrite any
# initial object defined here.
#
# An initial odata document can be defined like this:
# fish['/redfish/v1/odata'] = {
#         << JSON odata service document contents>>
# }

class RedfishODataService(Resource):
    """Defines API behaviors for the Redfish OData Service
    document.

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
        # TODO: Generate an OData service document on demand, if possible
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
    # Register the URIs that this API module responds to
    rest_api.add_resource(RedfishODataService,
        '/redfish/v1/odata',
        '/redfish/v1/odata/')

    return
    # End of activate()
