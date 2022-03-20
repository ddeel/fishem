# Copyright (c) 2021-2022 by Don Deel. All rights reserved.

"""
Shared data for fishem and its modules.

All Redfish and Swordfish objects are shared as JSON objects in a
dictionary named "fish". Redfish resource path names are used as
keys to access objects in this dictionary, and these objects can
contain nested elements. Examples are shown here:

Key (path)                          Value (object)
--------------------------------    --------------------------------
/redfish                            Protocol version object
/redfish/v1                         ServiceRoot
/redfish/v1/<R>                     Resource Collection
/redfish/v1/<R>/<Id1>               Resource Singleton Id1
/redfish/v1/<R>/<Id1>/<SR>          SubResource Collection
/redfish/v1/<R>/<Id1>/<SR>/<Id2>    SubResource Singleton Id2
/redfish/v1/odata                   OData Service Document
/redfish/v1/$metadata               Metadata Document

<R> = Resource
<SR> = SubResource
<Id1> = Identifier
<Id2> = Identifier

Note:   The keys for objects in this dictionary, including
        the ServiceRoot key, do NOT have trailing slashes.

fishem configuration setup information is shared in a dictionary
named "fishem_config".
"""

# fish data dictionary
fish = {}

# fishem configuration dictionary (set by fishem.py)
fishem_config = {}
