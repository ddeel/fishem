# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
HostInterface API Definitions.

Defines REST API behaviors for HostInterface.
Allows initial data for instances of this API object to be set.
Supports the handling of Actions defined for this API object.

Based upon fishem singleton template version 0.9.0
"""

# Standard library module imports
# None

# Third party module imports
from flask_restful import Resource      # REST operations
from flask import request               # JSON input from REST
from flask import make_response         # Allow header handling

# Local module imports
from fish_data import fish              # Fish data
import fishem_httpcodes as HTTP         # HTTP status codes

# Constants
# None

# Capabilities Restricions from unversioned schema
# (These items are read-only within the classes below)
res_cap_insertable = False
res_cap_updatable = True
res_cap_deletable = False

# Generate Allow HTTP Verbs string from Capabilities Restrictions
allow_http_verbs = 'GET'
if res_cap_insertable: allow_http_verbs += ', POST'
if res_cap_updatable:  allow_http_verbs += ', PUT, PATCH'
if res_cap_deletable:  allow_http_verbs += ', DELETE'

# Initial data for instances of this object at specific URIs
# can optionally be defined here with assignment statements:
#   fish[<instancd URI>] = {<initial instance data>}
# Note that this initial instance data may be overwritten when
# mocksups or fish files are loaded into fishem.


class HostInterface(Resource):
    """Defines API behaviors for HostInterface instances.

    Defined: GET, PUT, PATCH, DELETE.

    flask_restful provides default support for HEAD and OPTIONS.
    It also provides a default 405 (Method Not Allowed) response
    for any RESTful service requests that are not defined.
    """

    def __init__(self):
        """Handles class setup. Called by flask_restful prior to
        each and every REST operation handled by this class."""
        # End of __init__()

    def get(
            self,
            ManagerId = "",
            HostInterfaceId = ""
            ):
        """Defines GET behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        #
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

    def put(
            self,
            ManagerId = "",
            HostInterfaceId = ""
            ):
        """Defines PUT behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        #
        # Handle Resource Capability restriction
        if not res_cap_updatable:
            resp = make_response('', HTTP.METHOD_NOT_ALLOWED)
            resp.headers.extend({'Allow': allow_http_verbs})
            return resp
        #
        # Handle PUT request
        inst_key = request.path
        # fish keys do not have trailing slashes
        if inst_key.endswith('/'):
            inst_key += '/'
            inst_key = inst_key.replace('//', '')
        # Ensure object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Get JSON input, with minimal JSON checking
        json_input = request.get_json(force = True, silent = True)
        if json_input == None:
            return 'Bad JSON input', HTTP.BAD_REQUEST
        # Ensure @odata.id is in the new object
        if '@odata.id' not in json_input:
            return '@odata.id not in input', HTTP.BAD_REQUEST
        # Ensure @odata.id is not being changed
        if fish[inst_key]['@odata.id'] != json_input['@odata.id']:
            return 'Bad @odata.id input', HTTP.BAD_REQUEST
        # TODO: Add more checking of JSON input
        # Replace the old object with the new object
        fish[inst_key] = json_input
        # Return a copy of the new object
        return fish[inst_key], HTTP.OK
        # End of put()

    def patch(
            self,
            ManagerId = "",
            HostInterfaceId = ""
            ):
        """Defines PATCH behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        #
        # Handle Resource Capability restriction
        if not res_cap_updatable:
            resp = make_response('', HTTP.METHOD_NOT_ALLOWED)
            resp.headers.extend({'Allow': allow_http_verbs})
            return resp
        #
        # Handle PATCH request
        inst_key = request.path
        # fish keys do not have trailing slashes
        if inst_key.endswith('/'):
            inst_key += '/'
            inst_key = inst_key.replace('//', '')
        # Ensure object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Get JSON input, with minimal JSON checking
        json_input = request.get_json(force = True, silent = True)
        if json_input == None:
            return 'Bad JSON input', HTTP.BAD_REQUEST
        # Ensure @odata.id is not a PATCH target
        if '@odata.id' in json_input:
            return 'Attempted to PATCH @odata.id', HTTP.BAD_REQUEST
        # TODO: Add more checking of JSON input
        # Update patch_key items in the object
        for patch_key, patch_value in json_input.items():
            # TODO: Add Writeability check for each patch_key item
            fish[inst_key][patch_key] = patch_value
        # Return a copy of the updated object
        return fish[inst_key], HTTP.OK
        # End of patch()

    def post(
            self,
            ManagerId = "",
            HostInterfaceId = ""
            ):
        """Defines POST behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        #
        # Handle POST request
        # POST is not allowed as a CRUD operation on a singleton
        # resource (except for Actions, which are handled in a
        # separate class), but is defined here so a proper Allow
        # header will be returned if a POST request is received.
        resp = make_response('', HTTP.METHOD_NOT_ALLOWED)
        resp.headers.extend({'Allow': allow_http_verbs})
        return resp
        # End of post()

    def delete(
            self,
            ManagerId = "",
            HostInterfaceId = ""
            ):
        """Defines DELETE behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        # TODO: Check for (and handle?) @Redfish.OperationApplyTime
        #
        # Handle Resource Capability restriction
        if not res_cap_deletable:
            resp = make_response('', HTTP.METHOD_NOT_ALLOWED)
            resp.headers.extend({'Allow': allow_http_verbs})
            return resp
        #
        # Handle DELETE request
        inst_key = request.path
        # fish keys do not have trailing slashes
        if inst_key.endswith('/'):
            inst_key += '/'
            inst_key = inst_key.replace('//', '')
        # Ensure the object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Find the coll_key (assumes object is a collection member)
        inst_key_parts = inst_key.split('/')
        coll_member_id = inst_key_parts[len(inst_key_parts) - 1]
        coll_key = inst_key + '//'
        coll_key = coll_key.replace('/' + coll_member_id + '//', '')
        # Ensure the collection is in the fish object dictionary
        if coll_key not in fish:
            return 'Collection not found', HTTP.NOT_FOUND
        # Ensure the object is in the Collection's Members
        if {'@odata.id': inst_key} not in fish[coll_key]['Members']:
            return 'Object not in Collection', HTTP.NOT_FOUND
        # Get a copy of the object
        deleted_object = fish[inst_key]
        # Delete the object and its subordinate resources
        del_keys = []
        for fish_key in fish:
            if fish_key.startswith(inst_key):
                del_keys.append(fish_key)
        for del_key in del_keys:
                del fish[del_key]
        # Remove link from Collection Members
        fish[coll_key]['Members'].remove(
            {'@odata.id': inst_key})
        # Re-evaluate collection Members count
        fish[coll_key]['Members@odata.count'] = \
            len(fish[coll_key]['Members'])
        # Return a copy of the deleted object
        return deleted_object, HTTP.OK
        # End of delete()


class HostInterfaceActions(Resource):
    """Defines API behaviors for HostInterface Actions.

    Defined: POST.

    flask_restful provides default support for HEAD and OPTIONS.
    It also provides a 405 (Method Not Allowed) response for any
    RESTful service requests that are not defined.

    This class is only needed for Resource Singletons that support
    Actions or OEM Actions.

    Note: This class is included for all Singleton objects, even
    when there are no Actions currently defined for the object.
    This is to allow new Actions and OEM Actions to be created
    for experimental purposes.
    """

    def __init__(self):
        """Handles class setup. Called by flask_restful prior to
        each and every REST operation handled by this class."""
        # End of __init__()

    def post(
            self,
            ManagerId = "",
            HostInterfaceId = "",
            UriAction = "",
            UriOemAction = ""
            ):
        """Defines POST behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support (?)
        #
        # Handle POST request
        action_uri_parts = request.path.split('/Actions/')
        if len(action_uri_parts) != 2:
            return 'Bad input', HTTP.BAD_REQUEST
        inst_key = action_uri_parts[0]
        action_name = action_uri_parts[1]
        # Action names do not have trailing slashes
        if action_name.endswith('/'):
            action_name += '/'
            action_name = action_name.replace('//', '')
        # Ensure object is in the fish object dictionary
        if inst_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Scan for the requested Action with an elif chain that
        # follows the initial 'if' statement below; OEM Actions
        # will have action_name = 'Oem/<Oem>.<ActionName>'
        if action_name == '':
            return 'Unknown Action for ' + inst_key, HTTP.BAD_REQUEST
        else:
            # Did not find a defined Action or OEM Action
            return 'Unknown Action for ' + inst_key, HTTP.BAD_REQUEST
        # End of post()


# Activate this API module
def activate(rest_api):
    """Registers URIs for this API module with flask_restful."""

    # Register the URIs this API module responds to:
    rest_api.add_resource(
        HostInterface,
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>',
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>/'
        )

    # Register the Action URIs this API module responds to:
    rest_api.add_resource(
        HostInterfaceActions,
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>/Actions/<string:UriAction>',
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>/Actions/Oem/<string:UriOemAction>',
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>/Actions/<string:UriAction>/',
        '/redfish/v1/Managers/<string:ManagerId>/HostInterfaces/<string:HostInterfaceId>/Actions/Oem/<string:UriOemAction>/'
        )

    return
    # End of activate()
