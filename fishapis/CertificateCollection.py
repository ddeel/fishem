# Copyright (c) 2021-2022 by Don Deel. All rights reserved.

"""
CertificateCollection API Definitions.

Defines REST API behaviors for CertificateCollection.
Allows initial data for instances of this API object to be set.

Based upon fishem collection template version 0.9.1
"""

# Standard library module imports
# None

# Third party module imports
from flask_restful import Resource      # REST operations
from flask import request               # JSON and URI input from REST
from flask import make_response         # Allow header handling

# Local module imports
from fish_data import fish              # Fish data
import fishem_httpcodes as HTTP         # HTTP status codes

# Constants
# None

# Capabilities Restricions from unversioned schema
# (These items are read-only within the classes below)
res_cap_insertable = True
res_cap_updatable = False
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
# fish files or mockups are loaded into fishem.


class CertificateCollection(Resource):
    """Defines API behaviors for CertificateCollection.

    Defined: GET, POST.

    flask_restful provides default support for HEAD and OPTIONS.
    It also provides a 405 (Method Not Allowed) response for any
    RESTful service requests that are not defined.
    """

    def __init__(self):
        """Handles class setup. Called by flask_restful prior to
        each and every REST operation handled by this class."""
        # End of __init__()

    def get(
            self,
            ManagerAccountId = "",
            ExternalAccountProviderId = "",
            ManagerId = "",
            ComputerSystemId = "",
            ResourceBlockId = "",
            DatabaseId = "",
            EventDestinationId = "",
            MemoryId = "",
            ChassisId = "",
            ProcessorId = "",
            StorageId = "",
            StorageControllerId = "",
            FabricId = "",
            SwitchId = "",
            DriveId = "",
            NetworkAdapterId = "",
            VirtualMediaId = ""
            ):
        """Defines GET behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        #
        # Handle GET request
        coll_key = request.path
        # fish keys do not have trailing slashes
        if coll_key.endswith('/'):
            coll_key += '/'
            coll_key = coll_key.replace('//', '')
        # Ensure object is in the fish object dictionary
        if coll_key not in fish:
            return 'Object not found', HTTP.NOT_FOUND
        # Return the requested object
        return fish[coll_key], HTTP.OK
        # End of get()

    def post(
            self,
            ManagerAccountId = "",
            ExternalAccountProviderId = "",
            ManagerId = "",
            ComputerSystemId = "",
            ResourceBlockId = "",
            DatabaseId = "",
            EventDestinationId = "",
            MemoryId = "",
            ChassisId = "",
            ProcessorId = "",
            StorageId = "",
            StorageControllerId = "",
            FabricId = "",
            SwitchId = "",
            DriveId = "",
            NetworkAdapterId = "",
            VirtualMediaId = ""
            ):
        """Defines POST behavior. Called by flask_restful."""
        # When not empty, arguments hold values from the URI
        # TODO: Add privilege check
        # TODO: Add ETag support
        #
        # Handle Resource Capability restriction
        if not res_cap_insertable:
            resp = make_response('', HTTP.METHOD_NOT_ALLOWED)
            resp.headers.extend({'Allow': allow_http_verbs})
            return resp
        #
        # Handle POST request
        coll_key = request.path
        # fish keys do not have trailing slashes
        if coll_key.endswith('/'):
            coll_key += '/'
            coll_key = coll_key.replace('//', '')
        # Get JSON input, with minimal JSON checking
        json_input = request.get_json(force = True, silent = True)
        if json_input == None:
            return 'Bad JSON input', HTTP.BAD_REQUEST
        # Ensure Id is in the new object
        if 'Id' not in json_input:
            return 'Id not in input', HTTP.BAD_REQUEST
        inst_key = coll_key + '/' + json_input['Id']
        # Ensure @odata.id (if present) is in sync with Id
        if '@odata.id' in json_input:
            # Remove any trailing '/' from @odata.id
            odata_id = json_input['@odata.id']
            if odata_id.endswith('/'):
                odata_id =+ '/'
                odata_id = odata_id.replace('//', '')
            # Check if @odata.id is in sync with Id
            if odata_id != inst_key:
                return '@odata.id out of sync with Id', HTTP.BAD_REQUEST
        else:
            # set @odata.id to be in sync with Id
            json_input['@odata.id'] = inst_key
        # TODO: Add more checking of JSON input
        # Check if object is already in the fish object dictionary
        if inst_key in fish:
            return 'Object already exists', HTTP.BAD_REQUEST
        # Add new object to fish
        fish[inst_key] = json_input
        # Add new link to collection Members
        fish[coll_key]['Members'].append(
            {'@odata.id': inst_key})
        # Re-evaluate collection Members count
        fish[coll_key]['Members@odata.count'] = \
            len(fish[coll_key]['Members'])
        return json_input, HTTP.CREATED
        # End of post()


# Activate this API module
def activate(rest_api):
    """Registers URIs for this API module with flask_restful."""

    # Register the URIs that this API module responds to:
    rest_api.add_resource(
        CertificateCollection,
        '/redfish/v1/AccountService/Accounts/<string:ManagerAccountId>/Certificates',
        '/redfish/v1/AccountService/Accounts/<string:ManagerAccountId>/Certificates/',
        '/redfish/v1/AccountService/ActiveDirectory/Certificates',
        '/redfish/v1/AccountService/ActiveDirectory/Certificates/',
        '/redfish/v1/AccountService/LDAP/Certificates',
        '/redfish/v1/AccountService/LDAP/Certificates/',
        '/redfish/v1/AccountService/ExternalAccountProviders/<string:ExternalAccountProviderId>/Certificates',
        '/redfish/v1/AccountService/ExternalAccountProviders/<string:ExternalAccountProviderId>/Certificates/',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/Accounts/<string:ManagerAccountId>/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/Accounts/<string:ManagerAccountId>/Certificates/',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/ActiveDirectory/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/ActiveDirectory/Certificates/',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/LDAP/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/LDAP/Certificates/',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/ExternalAccountProviders/<string:ExternalAccountProviderId>/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/RemoteAccountService/ExternalAccountProviders/<string:ExternalAccountProviderId>/Certificates/',
        '/redfish/v1/Managers/<string:ManagerId>/NetworkProtocol/HTTPS/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/NetworkProtocol/HTTPS/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Boot/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Boot/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Boot/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Boot/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Boot/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Boot/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/SecureBoot/SecureBootDatabases/<string:DatabaseId>/Certificates/',
        '/redfish/v1/EventService/Subscriptions/<string:EventDestinationId>/Certificates',
        '/redfish/v1/EventService/Subscriptions/<string:EventDestinationId>/Certificates/',
        '/redfish/v1/EventService/Subscriptions/<string:EventDestinationId>/ClientCertificates',
        '/redfish/v1/EventService/Subscriptions/<string:EventDestinationId>/ClientCertificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/Chassis/<string:ChassisId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/Chassis/<string:ChassisId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Memory/<string:MemoryId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Processors/<string:ProcessorId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Processors/<string:ProcessorId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Processors/<string:ProcessorId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Processors/<string:ProcessorId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Processors/<string:ProcessorId>/Certificates/',
        '/redfish/v1/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/StorageControllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Controllers/<string:StorageControllerId>/Certificates/',
        '/redfish/v1/Fabrics/<string:FabricId>/Switches/<string:SwitchId>/Certificates',
        '/redfish/v1/Fabrics/<string:FabricId>/Switches/<string:SwitchId>/Certificates/',
        '/redfish/v1/Chassis/<string:ChassisId>/Certificates',
        '/redfish/v1/Chassis/<string:ChassisId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/Chassis/<string:ChassisId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/Chassis/<string:ChassisId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/Storage/<string:StorageId>/Drives/<string:DriveId>/Certificates/',
        '/redfish/v1/Chassis/<string:ChassisId>/NetworkAdapters/<string:NetworkAdapterId>/Certificates',
        '/redfish/v1/Chassis/<string:ChassisId>/NetworkAdapters/<string:NetworkAdapterId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/Certificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/VirtualMedia/<string:VirtualMediaId>/ClientCertificates/',
        '/redfish/v1/UpdateService/RemoteServerCertificates',
        '/redfish/v1/UpdateService/RemoteServerCertificates/',
        '/redfish/v1/UpdateService/ClientCertificates',
        '/redfish/v1/UpdateService/ClientCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/Certificates',
        '/redfish/v1/Managers/<string:ManagerId>/Certificates/',
        '/redfish/v1/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates',
        '/redfish/v1/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates/',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates',
        '/redfish/v1/CompositionService/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates/',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates',
        '/redfish/v1/ResourceBlocks/<string:ResourceBlockId>/Systems/<string:ComputerSystemId>/KeyManagement/KMIPCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/SPDM/TrustedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/SPDM/TrustedCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/SPDM/RevokedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/SPDM/RevokedCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Client/TrustedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Client/TrustedCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Client/RevokedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Client/RevokedCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Server/TrustedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Server/TrustedCertificates/',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Server/RevokedCertificates',
        '/redfish/v1/Managers/<string:ManagerId>/SecurityPolicy/TLS/Server/RevokedCertificates/'
        )

    return
    # End of activate()
