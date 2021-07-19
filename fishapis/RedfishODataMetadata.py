# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
RedfishODataMetadata API Definitions.

Defines REST API behaviors for RedfishODataMetadata.
Allows initial data for instances of this API object to be set.

Based upone Singleton template version 0.9.0
"""

# Standard library module imports
# None

# Third party module imports
from flask_restful import Resource      # REST operations
from flask import request               # JSON input from REST
from flask import make_response         # XML response handling
import xmltodict                        # XML response handling

# Local module imports
from fish_data import fish              # Fish data
import fishem_httpcodes as HTTP         # HTTP status codes

# Constants
# None

# Capabilities Restricions from unversioned schema
# (These items are read-only within the classes below)
#
# None

# The Redfish $metadata document is stored in the fish object
# dictionary, using xmltodict to encode and decode the XML.
# The key '/redfish/v1/$metadata' should only be defined when a
# valid $metadata document is present. It can be defined here
# (see below) or by loading fishem from a mockup or a fish file.
# Mockups and fish files loaded into fishem can overwrite any
# initial object defined here.
#
# An initial $metadata document can be defined like this:
# fish['/redfish/v1/$metadata'] = {
#     <<JSON-encoded XML $metadata document contents>>
# }

class RedfishODataMetadata(Resource):
    """Defines API behaviors for the Redfish OData $metadata
    document.

    Defined: GET.

    flask_restful provides default support for HEAD and OPTIONS.
    It also provides a 405 (Method Not Allowed) response for any
    RESTful service requests that are not defined.
    """

    def __init__(
            self,
            **resource_class_kwargs
            ):
        """Handles class setup. Called by flask_restful prior to
        each and every REST operation handled by this class."""
        global api
        api = resource_class_kwargs['api']
        # End of __init__()

    def get(
            self
            ):
        """Defines GET behavior. Called by flask_restful."""
        # TODO: Generate an OData $metadata document on demand          # Note
        # Handle GET request
        inst_key = request.path
        # fish keys do not have trailing slashes
        if inst_key.endswith('/'):
            inst_key += '/'
            inst_key = inst_key.replace('//', '')
        # Ensure object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Ensure the request has a good Accept Header
        good_accept_header_values_for_xml = \
            ['application/xml', '*/*', 'application/*']
        good_accept_header = False
        for value in good_accept_header_values_for_xml:
            if value in api.mediatypes():
                good_accept_header = True
        if not good_accept_header:
            return 'XML not allowed by Accept Headers', \
                    HTTP.NOT_ACCEPTABLE
        # Return object with Content-Type set to 'application/xml'
        resp = make_response(xmltodict.unparse(fish[inst_key], \
            pretty=True), HTTP.OK)
        resp.headers.remove('Content-Type')     # Remove default
        resp.headers.remove('Content-Length')   # Remove default
        resp.headers.extend({'Content-Type': 'application/xml'})
        return resp
        # End of get()

# Activate this API module
def activate(rest_api):
    """Registers URIs for this API module with flask_restful."""

    # Register the URIs that this API module responds to
    rest_api.add_resource(
        RedfishODataMetadata,
        '/redfish/v1/$metadata',
        '/redfish/v1/$metadata/',
        resource_class_kwargs={'api': rest_api}
        )

    return
    # End of activate()
