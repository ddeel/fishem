# fishem -- Fish Emulator

fishem is a Redfish/Swordfish emulator that responds to the create,
read, update, delete, and action RESTful API operations defined for
the Redfish protocol. When fishem is started, the initial state of
the emulator is set by an input Redfish/Swordfish mockup or by an
input JSON "fish" file. When fishem is stopped, the final state of
the emulator can be captured as an output mockup and/or as an output
JSON "fish" file.

The mockups used by fishem are normal Redfish/Swordfish mockups. These
mockups are hierarchical folder/directory tree structures where each
node corresponds to a Redfish/Swordfish object, and a JSON file named
*index.json* within each node describes the state elements for the
Redfish/Swordfish object. The top-most node corresponds to the Redfish
root (/redfish/v1).

The JSON "fish" files used by fishem are files that describe the state
information for all of the Redfish/Swordfish objects known to fishem in
a single JSON file. These files are used to allow a stopped fishem run
to be continued in a subsequent fishem run.

An important early step in the development of a Redfish/Swordfish
service implementation is to create a mockup of the intended service.
fishem provides developers with a way to see how these mockups react
to real Redfish protocol API operations. It also supports the
incremental development of mockups, meaning they can be made more
and more complete over time. With a reasonably complete mockup,
fishem can allow a Redfish/Swordfish client implementation to
interact with an emulation of the intended service before the
service implementation actually exists.

fishem accepts any valid Redfish/Swordfish mockup as input. After the
mockup is loaded, fishem responds to the create, read, update, delete,
and action RESTful API operations supported by the Redfish/Swordfish
elements in the mockup.

Note that fishem does not do any checking of input mockups. Other
tools should be used to ensure that mockups are using good JSON and
have correct links between the different objects within the mockup.
fishem does support experimentation, however, so it is possible to
work with mockups that have elements that go beyond what is directly
supported by Redfish/Swordfish schema.

----

## Current Status

### Version: 0.9.1

This version of fishem is based upon schema from the following
public releases of the DMTF Redfish and SNIA Swordfish standards:

- DMTF Redfish Release 2021.4, published January 18, 2022

- SNIA Swordfish v1.2.3, published December 5, 2021

Note: Includes corrections for minor schema errors found in the
Redfish Certificate\_v1.xml and CircuitCollection\_v1.xml schema
files. These corrections have been given to the DMTF to become
part of the next Redfish release.

### Functionality supported includes:

- The ability to set the initial state of the emulator at
  startup by reading in any valid Redfish/Swordfish mockup.
  Input Redfish/Swordfish mockups can include OData metadata
  (/redfish/v1/$metadata) and/or an OData service document
  (/redfish/v1/odata) to set the corresponding initial state
  elements in the emulator.

- The ability to capture the final state of the emulator at
  shutdown by creating an output mockup.

- Basic handling of the allowed GET, PUT, PATCH, POST, and
  DELETE operations for all the URI-accessible Collection
  objects and Singleton objects defined by Redfish/Swordfish
  schema.

- Handling of URIs with and without trailing slashes for
  RESTful API operations.

- Routing of RESTful API operation requests to individual
  API code modules using URIs from Redfish/Swordfish schema.

- API code modules with simplified access to arguments
  derived from the URIs that invoke the API code modules.

- Basic handling of all Singleton object Actions defined by
  Redfish/Swordfish schema, with support for also handling
  OEM Actions. "Basic handling" of Actions means they are
  detected, responded to with HTTP responses, and reported
  to the user console by API code modules.

- Handling of resource capabilities (Insertable, Updatable,
  and Deletable) defined by Redfish/Swordfish schema.

### Functionality not yet complete includes:

- The ability to regenerate basic API code modules from updated
  schema for all the URI-accessible Collection objects and
  Singleton objects defined by Redfish/Swordfish schema.

- Support for HTTPS connections to the RESTful API.

- Support for ETags in RESTful API operations.

- Optional enforcement of schema-defined requirements
  for object properties (Read Only, Mandatory, etc)

----

## Installing fishem

fishem requires Python 3.6 or higher, and running in a virtual
environment is recommended but not required.

fishem is installed with the following steps:

- Copy the fishem project files into a folder/directory.

- Go to the folder/directory where the fishem project files are
  located and install the required Python packages with this
  command:

	**pip install -r requirements.txt**

fishem should now be ready to run in a basic configuration where all
of its input arguments come from the command line that starts fishem.

----

## Starting fishem

fishem runs from the command line and accepts several arguments that
establish inputs, outputs, and various aspects of fishem behavior.
These arguments can come from the command line, from a configuration
file (more about this below), or from a combination of the command
line and the configuration file.

In cases where an argument is present in both the command line and
the configuration file, the command line argument always overrides
the configuration file argument.

To run fishem, go to the folder/directory where *fishem.py* is kept
and enter this command:

**python fishem.py *arguments***

The *arguments* are all optional, and zero or more of them can be
used in any combination in the command that starts fishem. Most of
the arguments support both a long form (begins with "--") and a
short form (begins with "-"):

**--help** or **-h**

Show the fishem help message and immediately exit.

**--version** or **-v** or   **-V**

Show the fishem version and immediately exit.

**--imockup IMOCKUP** or **-im IMOCKUP**

Input mockup IMOCKUP when fishem is started. IMOCKUP must specify
a directory where a Redfish/Swordfish mockup is located. Note that
fishem does not do any checking of the input mockup. It is assumed
that the input mockup provides a valid JSON description of the
Redfish/Swordfish initial state for the emulator.

**--omockup OMOCKUP** or **-om OMOCKUP**

Output mockup OMOCKUP when fishem is stopped. OMOCKUP must specify
the name of a directory where the output mockup is to be stored.
If OMOCKUP already exists, it will be overwritten.

**--ifish IFISH** or **-if IFISH**

Input JSON fish file IFISH when fishem is started. IFISH must
specify the name of a JSON fish file from a previous fishem run.
Note that if an input mockup is also specified, then some of the
state from the input JSON fish file may be overwritten by the
state from the input mockup.

**--ofish OFISH** or **-of OFISH**

Output JSON fish file OFISH when fishem is stopped. OFISH must
specify the name of a file where the output JSON fish file is
to be stored. If OFISH already exists, it will be overwritten.

**--port PORT** or **-p PORT**

Set the port number that fishem will use for the RESTful API.
A default value of 5000 will be used unless this is set to a
different value by the command line or the configuration file.

**--https**

[THIS FUNCTIONALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]

Use HTTPS for the RESTful API. A default value of "False" is
used unless it is set otherwise by the command line or the
configuration file. There is no short form for this argument.

**--fishdoctorEnabled**

[THIS FUNCTIONALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]

Enable fishdoctor for the RESTful API. A default value of "False"
is used unless it is set otherwise by the command line or the
configuration file. There is no short form for this argument.

----

## Configuration file

Most of the fishem command line arguments can also be set by an
optional JSON configuration file named *fishem\_config.json* in
the folder/directory where *fishem.py* is kept. This is a JSON
key-value file, where zero or more of the following supported
entries can be used in any combination:

**"imockup": "IMOCKUP"**

Input mockup IMOCKUP when fishem is started. IMOCKUP must specify
a directory where a Redfish/Swordfish mockup is located. Note that
fishem does not do any checking of the input mockup. It is assumed
that the input mockup provides a valid JSON description of the
Redfish/Swordfish initial state for the emulator.

**"omockup": "OMOCKUP"**

Output mockup OMOCKUP when fishem is stopped. OMOCKUP must specify
the name of a directory where the output mockup is to be stored.
If OMOCKUP already exists, it will be overwritten.

**"ifish": "IFISH"**

Input JSON fish file IFISH when fishem is started. IFISH must
specify the name of a JSON fish file from a previous fishem run.
Note that if an input mockup is also specified, then some of the
state from the input JSON fish file may be overwritten by the
state from the input mockup.

**"ofish": "OFISH"**

Output JSON fish file OFISH when fishem is stopped. OFISH must
specify the name of a file where the output JSON fish file is
to be stored. If OFISH already exists, it will be overwritten.

**"port": "PORT"**

Set the port number that fishem will use for the RESTful API.
A default value of 5000 will be used unless this is set to a
different value by the command line or the configuration file.

**"https": "FLAG"**

[THIS FUNCTIONALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]

Use HTTPS for the RESTful API if FLAG is set to "true". A default
value of "false" will be used unless it is set otherwise by the
command line or the configuration file.

**"fishdoctorEnabled": "FLAG"**

[THIS FUNCTIONALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]

Enable fishdoctor for the RESTful API if FLAG is set to "true".
A default value of "false" is used unless it is set otherwise by
the command line or the configuration file.

### Configuration file notes

The configuration file is optional, but a basic *fishem\_config.json*
configuration file is distributed with fishem. It sets all the input
and output file argument values to null (""), it sets the "port"
argument to 5000, and it sets the "https" and "fishdoctorEnabled"
arguments to "false". These are the same default values that fishem
uses when it cannot find the optional configuration file.

Command line arguments always override configuration file arguments,
so the basic *fishem\_config.json* file effectively only serves as a
ready-to-use template that can be easily customized.

Note: If fishem is started with no arguments set by the command line
and no arguments set by the configuration file, then the emulator will
not have any Redfish/Swordfish state at all, and the RESTful API will
only be able to respond to requests for the Redfish protocol version.

----

## Stopping fishem

Enter Control-C to stop fishem at any time after it is fully started
and ready to handle RESTful API operations. The current state of the
emulator will be saved in a JSON fish file named *lastfish.json* in the
folder/directory where *fishem.py* is kept, and then the current state
of the emulator will also be saved in any form that was requested
(mockup and/or JSON fish file) by the command line that started fishem.

fishem always saves a JSON fish file named *lastfish.json* to ensure
that a developer can access the final state of an emulator run, even
when no output mockup or output JSON fish file was requested when
fishem was started.

If needed, an output mockup can be created from *lastfish.json* by
running fishem. Start fishem with *lastfish.json* as an input JSON
fish file and specify a name for an output mockup. After fishem has
fully started, stop fishem with Control-C (before any RESTful API
operations have caused additional state changes) and the requested
output mockup will be created.

----

## Windows 10 console

fishem uses Flask, which can send output to the Windows 10 console
that includes terminal control character sequences like "^[[37m".
If this is happening, it likely means the Windows 10 console is
not configured to support color, and the following article may be
useful: [Windows console with ANSI colors handling](https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling "Windows console with ANSI colors handling")

----

## Technical Overview

This section provides an overview of the fishem component parts and
briefly explains how they work together to bring Redfish and Swordfish
mockups to life.

fishem is written in Python, and making the source code easy to
understand was given a higher priority than elegance or minimizing
code.


### fishem components

The files and directories in the base fishem directory are as follows.

##### \_\_init\_\_.py

The presence of this file makes the fishem directory a Python package.

##### fish\_data.py

fish\_data.py contains shared data for fishem and its modules. The
shared data is kept in two Python dictionaries, one named "fish" and
one named "fishem\_config".

###### *fish* dictionary

All Redfish and Swordfish objects are kept as JSON objects in a
shared Python dictionary named *fish*. This dictionary contains the
current state of the emulator at all times.

Redfish resource path names are used as keys to access objects in this 
dictionary, and objects within the dictionary can contain nested
elements.

Examples of *fish* dictionary keys are shown here:

- /redfish
  - Protocol version
- /redfish/v1
  - ServiceRoot
- /redfish/v1/<R\>
  - Resource Collection <R\>
- /redfish/v1/<R\>/<Id1\>
  - Resource Singleton <Id1\>
- /redfish/v1/<R\>/<Id1\>/<SR\>
  - SubResource Collection <SR\>
- /redfish/v1/<R\>/<Id1\>/<SR\>/<Id2\>
  - SubResource Singleton <Id2\>
- /redfish/v1/odata
  - OData Service Document
- /redfish/v1/$metadata
  - Metadata Document


The keys for the *fish* dictionary do not have trailing slashes.

The information in the *fish* dictionary can be accessed and set by any
of the fishem modules. It contains the current state of the emulator at
all times. It is referred to as the "fish" when fishem is running,
and as a "fish file" when it is stored as a JSON file.

Only JSON objects are kept in the *fish* dictionary. This includes the
Redfish $metadata document, which is converted from XML to JSON using
the Python package "xmltodict". The "xmltodict" package is also used to
convert JSON back into XML.

###### *fishem\_config* dictionary

fishem configuration information is kept in a shared Python dictionary
named *fishem\_config*. This information is initialized by the
*fishem.py* module, and can be accessed by any of the other fishem
modules.

##### fishem.py

This module contains main(), and is directly invoked by the user to
coordinate the things done by other fishem modules to start and stop
the emulator.

##### fishem\_config.json

This is an optional JSON key-value file that contains values for zero
or more of the supported fishem configuration parameters. It is kept
in the directory where *fishem.py* and *fishem\_configure.py* are kept.

The *fishem\_config.json* file is optional, but a basic version of the
file is distributed with fishem. It sets all the fishem configuration
parameters to the default values used when the optional
*fishem\_config.json* file is not found, so in its distributed form it
is really only a ready-to-use template that can be easily customized.

##### fishem\_configure.py

This module is called by *fishem.py* at startup to establish values for
the fishem configuration parameters that can be set by the user.

##### fishem\_fishfileio.py

This module handles all fish file input and output for fishem.

##### fishem\_httpcodes.py

This module contains numerical definitions for the HTTP status codes
used by fishem.

##### fishem\_mockupio.py

This module handles all mockup input and output for fishem.

##### fishem\_restops.py

This module is called by *fishem.py* at startup to initialize the
RESTful server and launch REST operations for fishem.

##### fishem\_version.py

This module sets the fishem version number.

##### lastfish.json

This is a JSON fish file that describes the state information for all
of the Redfish and Swordfish objects known to fishem when it was most
recently stopped.

fishem always saves a JSON fish file named *lastfish.json* when it is
stopped. This is to ensure that a developer can access the final state
of a fishem run, even when no output mockup or fish file was specified
when fishem was started.

This file can be used to allow a stopped fishem run to be continued in
a subsequent fishem run, by specifying it as an input fish file.

##### LICENSE.txt

This is a text file that contains the BSD 3-Clause License that covers
the fishem source code.

##### README.md

This is a Markdown file that contains the fishem README source.

##### requirements.txt

This is a text file that lists the Python packages needed by fishem.
It is used by the Python "pip" command to set up the environment
necessary for running fishem.

##### fishem/fishapis directory

This is a directory that contains the fishem API modules. It also
contains a \_\_init\_\_.py file to make it a Python package.

There are currently more than 200 API modules in the *fishem/fishapis*
directory.

Each API module implements the REST operations and behaviors defined
for a specific Redfish or Swordfish object. Most of the API modules are
for the collection and singleton objects defined for Redfish and
Swordfish, but there are also a few special-purpose API modules.

API module file names are directly derived from the corresponding
Redfish and Swordfish CSDL schema file names, using the same spellings
and capitalizations. For example, the fishem API module file name
"ServiceRoot.py" is derived from the Redfish CSDL schema file name
"ServiceRoot\_v1.xml".

###### Collection API modules

Collection API modules each have one class with methods that implement
the create, read, update, and delete (CRUD) operations supported by the
corresponding Redfish or Swordfish collection. These methods are called
by Flask-RESTful to handle requested CRUD operations.

For Redfish and Swordfish collections, the supported CRUD operations
are GET and POST.

Flask-RESTful provides a 405 (Method Not Allowed) response for any CRUD
operation requests that are not implemented by an API module. It also
provides default support for handling HEAD and OPTIONS requests.

The name of the class that implements the supported CRUD operations is
the same as the main part of the API module file name. For example,
this class is named *ChassisCollection* in the API module that has the
file name *ChassisCollection.py*.

Collection API modules also define a function called *activate()* that
registers with Flask-RESTful the URIs that the API module responds to.
This function is called by *fishem\_restops.py* as part of the fishem
initialization process.

###### Singleton API modules

Singleton API modules each have two classes.

The first class in a singleton API module has methods that implement
the create, read, update, and delete (CRUD) operations supported by the
corresponding Redfish or Swordfish singleton. These methods are called
by Flask-RESTful to handle requested CRUD operations.

For Redfish and Swordfish singletons, the supported CRUD operations are
GET, PUT, PATCH, and DELETE.

Note: POST is not an allowed CRUD operation for Redfish and Swordfish
singletons, but it is a defined method in the class that handles CRUD
operations. This is to ensure that a proper Allow header can be
returned with a 405 (Method Not Allowed) response if a POST request is
received.

Flask-RESTful provides a 405 (Method Not Allowed) response for any CRUD
operation requests that are not implemented by an API module. It also
provides default support for handling HEAD and OPTIONS requests.

The name of the class that implements the supported CRUD operations is
the same as the main part of the API module file name. For example,
this class is named *Chassis* in the API module that has the file name
*Chassis.py*.

The second class in a Singleton API module has a method that implements
basic handling of the Actions supported by the corresponding Redfish or
Swordfish singleton. This method is called by Flask-RESTful to handle
requested Actions.

The "basic handling" of Actions means they are detected, responded to
with an HTTP response, and reported to the user console.

The name of the class that implements Actions is the same as the class
that handles supported CRUD operations, but with "Actions" appended.
For example, if the class handling CRUD operations is called *Chassis*,
then the class that handles Actions is called *ChassisActions*.

Singleton API modules also define a function called *activate()* that
registers with Flask-RESTful the URIs that the API module responds to.
These URIs include the URIs that request the Actions supported by the
Redfish or Swordfish singleton. This function is called by
*fishem\_restops.py* as part of the fishem initialization process.

###### Special-purpose API modules

There are a few API modules that are not defined by Redfish or
Swordfish CSDL schema.

These API modules each have one class with a method that implements a
GET operation that can be called by Flask-RESTful. They also each
define an *activate()* function for registering with Flask-RESTful the
URI they respond to.

*RedfishProtocolVersion.py* is an API module that responds to a GET
operation on the URI "/redfish" by providing the Redfish protocol
version.

*RedfishODataMetadata.py* is and API module that responds to a GET
operation on the URI "/redfish/odata" by providing the Redfish OData
Service document when this information is included as part of the
initial state of the emulator set by an input fish file or an input
mockup.

*RedfishOdataMetadata.py* is an API module that responds to a GET
operation on the URI "/redfish/$metadata" by providing the Redfish
Metadata document when this information is included as part of the
initial state of the emulator set by an input fish file or an input
mockup.

###### Additional notes about API modules

The API modules in the *fishem/fishapis* directory serve as a basic set
of API modules for bringing Redfish andSwordfish mockups to life. They
are purposely generic, to support a broad range of possible mockups.

The API modules distributed with fishem are programmatically generated
using information from public Redfish and Swordfish CSDL schema files.

When new releases of Redfish and Swordfish become publicly available,
the fishem API modules will be regenerated to become part of the next
fishem release.

API modules can be easily customized to handle different situations
that can range from experimentating with schema changes to connecting
fishem to real equipment. Users must preserve (and possibly update) any
customized API modules when fishem is updated.


### How fishem works

This section provides an overview of how the fishem components work
together to bring mockups to life. The overview covers what happens
when fishem is started up, and what happens when fishem is shut down.

##### fishem startup

The *fishem.py* module coordinates fishem startup by working with other
modules to implement the following sequence:

- Determine configuration parameters
- Initialize API module data
- Input specified files
- Start REST operations

###### Determine configuration parameters

*fishem.py* calls *fishem\_configure.py* to establish values for the
configuration parameters that can be set by the user.

*fishem\_configure.py* establishes these values by using values from
three different sources. First, default values are used. Second, values
from the *fishem\_config.json* file are used. Third, values from the
command line are used. This ordering enables the following:

- Values are always set for all configuration parameters
- The *fishem\_config.json* file is optional
- The *fishem\_config.json* file entries are optional
- Command line values are optional
- Command line values override *fishem\_config.json* file values

After values for the user-settable configuration parameters are set,
*fishem.py* adds name and version information.

The configuration parameters are then stored in the *fish\_data.py*
module's *fishem\_config* dictionary. This shares the configuration
parameters with other fishem modules.

###### Initialize API module data

*fishem.py* imports each API module in the *fishem/fishapis* directory.
Besides allowing each API module to initialize itself, this also
provides each API module with an opportunity to set default values for
data in the *fish\_data.py* module's *fish* dictionary.

Currently, the *RedfishProtocolVersion.py* API module is the only one
that sets default values for data in the *fish* dictionary. This is
because there is no way to set the Redfish protocol version from within
a mockup. All other information loaded into the *fish* dictionary is
currently set by either an input fish file or an input mockup.

###### Input specified files

If an input fish file is specified by the *fishem\_config.json* file or
the command line, *fishem.py* calls *fishem\_fishfileio.py* to handle
the input operation. Information from the input fish file is loaded
into the *fish\_data.py* module's *fish* dictionary.

If an input mockup is specified by the *fishem\_config.json* file or
the command line, *fishem.py* calls *fishem\_mockupio.py* to handle
the input operation. Information from the input fish file is loaded
into the *fish\_data.py* module's *fish* dictionary.

An input fish file and an input mockup can be specified at the same
time. When this is done, the fish file is loaded first, and the mockup
is loaded second. The input mockup can overwrite portions of the data
loaded from the fish file. Care must be taken by the user to ensure
that combining the fish file and the mockup in this manner will result
in a valid initial Redfish/Swordfish state for the emulator.

###### Start REST operations

*fishem.py* calls *fishem\_restops.py* to start REST operations.

Flask and Flask-RESTful are used to handle REST operations for fishem,
so *fishem\_restops.py* begins by creating instances of both. It also 
sets them up to make output more human-readable on browsers without
JSON plugins.

*fishem\_restops.py* then calls the *activate()* function in each API
module in the *fishem/fishapis* directory to register the URIs that
the API module will respond to.

fishem REST operations are then launched. From this point on, incoming
REST operations are received by Flask and Flask-RESTful and forwarded
to the appropriate API module according to the URI for the REST
operation request.

##### fishem shutdown

The *fishem.py* module coordinates fishem shutdown by working with
other modules to implement the following sequence:

- Catch Control-C
- Save a *lastfish.json* file
- Save specified output files

The *fishem.py* module exits when this sequence is completed, and this
terminates the fishem run.

###### Catch Control-C

The user causes fishem to shut down by entering Control-C.

The *fishem.py* module has a signal handler that catches the Control-C
event and starts the fishem shutdown sequence.

###### Save a *lastfish.json* file

The *fishem.py* module calls the *fishem\_fishfileio.py* module to
output a fish file named *lastfish.json*. If the *lastfish.json* fish
file already exists, it will be overwritten.

The *lastfish.json* fish file is a JSON fish file that describes the
state information for all of the Redfish and Swordfish objects known to
fishem when the user entered Control-C.

fishem saves a JSON fish file named *lastfish.json* when it is stopped
to ensure that a developer can access the final state of a fishem run,
even when no output fish file or output mockup was specified when
fishem was started.

The *lastfish.json* fish file can be used to allow a stopped fishem run
to be continued in a subsequent fishem run, by specifying it as an
input fish file.

###### Save specified output files

The *fishem.py* module calls the *fishem\_fishfileio.py* module to
output any fish file that was specified when fishem was started. If the
specified output fish file already exists, it will be overwritten.

The *fishem.py* module calls the *fishem\_mockupio.py* module to output
any mockup that was specified when fishem was started. if the specified
output mockup already exists, it will be overwritten.

An output fish file and an output mockup can be specified at the same
time when fishem is started. When this is done, the output fish file is
written befre the output mockup is written.

----
