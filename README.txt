fishem -- Fish Emulator

fishem is a Redfish/Swordfish emulator that responds to the create,
read, update, delete, and action RESTful API operations defined by the
Redfish protocol. When fishem is started, the initial state of the
emulator is set by an input Redfish/Swordfish mockup or by an input
JSON "fish" file. When fishem is stopped, the final state of the
emulator can be captured as an output mockup and/or as an output
JSON "fish" file.

The mockups used by fishem are normal Redfish/Swordfish mockups. These
mockups are hierarchical folder/directory tree structures where each
node corresponds to a Redfish/Swordfish object, and a JSON file named
"index.json" within each node describes the state elements for the
Redfish/Swordfish object. The top-most node corresponds to the Redfish
root (/redfish/v1).

The JSON "fish" files used by fishem are files that describe the state
information for all of the Redfish/Swordfish objects known to fishem in
a single JSON file. These files are used to allow a stopped fishem run
to be continued in a subsequent fishem run.

An important early step in the development of a Redfish/Swordfish
service implementation is to create a mockup of the intended service,
and the mockup should be as complete as possible. fishem provides
developers with a way to see how these mockups react to real Redfish
protocol API operations, and it supports the incremental development
of mockups for the intended service.

fishem accepts any valid Redfish/Swordfish mockup as input. After the
mockup is loaded, fishem responds to the create, read, update, delete,
and action RESTful API operations supported by the Redfish/Swordfish
elements in the mockup.


Current Status

The current version of fishem is: 0.9.0

This version of fishem is based upon schema from the following
public releases of the DMTF Redfish and SNIA Swordfish standards:
  - DMTF Redfish Release 2021.1, published May 18, 2021
  - SNIA Swordfish v1.2.2a, published June 14, 2021

fishem is a work in progress, but it already supports:
  - The ability to accept any valid Redfish/Swordfish mockup
    (must include the Redfish root) to set the initial state
    of the emulator.
  - Basic handling of the allowed GET, PUT, POST, and DELETE
    operations for all the Collection and Singleton objects
    defined by Redfish/Swordfish schema.
  - Routing of RESTful API operation requests to individual
    API code modules using URIs from Redfish/Swordfish schema.
  - API code modules with simplified access to arguments
    derived from the URIs that invoke the API code modules.
  - Basic handling of all Singleton object Actions defined by
    Redfish/Swordfish schema, with support for also handling
    OEM Actions. ("Basic handling" of Actions means they are
    detected, responded to, and reported by the API modules.)
  - Handling of resource capabilities (Insertable, Updatable,
    and Deletable) defined by Redfish/Swordfish schema.

Functionality that is not yet complete includes:
  - Support for HTTPS connections to the RESTful API.
  - Support for ETags in RESTful API operations.
  - Optional enforcement of schema-defined requirements for
    object propoerties (Read Only, Mandatory, etc)
  - (Other updates are also in progress)


Installing fishem

fishem requires Python 3.6 or higher. Running in a virtual environment
is recommended but not required.

fishen is installed with the following steps:
  - Copy the fishem project files into a folder/directory.
  - Go to the folder/directory where fishem is kept and install the
    Python packages required by fishem by entering this command:
        pip install -r requirements.txt

fishem should now be ready to run in a basic configuration where all
of its arguments come from the command line that starts fishem.


Starting fishem

fishem runs from the command line and accepts several arguments that
establish inputs, outputs, and various aspects of fishem behavior.
These arguments can come from the command line, from a configuration
file (more about this below), or from a combination of the command
line and the configuration file.

In cases where an argument is present in both the command line and
the configuration file, the command line argument always overrides
the configuration file argument.

To run fishem, go to the folder/directory where fishem is kept and
enter this command:
    python fishem.py <arguments>

The <arguments> are all optional, and can be used in any combination
with the command that starts fishem. Most arguments support both a
long form (begins with "--") and a short form (begins with "-"):

  --help
  -h
      Show the fishem help message and immediately exit.

  --version
  -v
  -V
      Show the fishem version and immediately exit.

  --imockup IMOCKUP
  -im IMOCKUP
      Input mockup IMOCKUP when fishem is started. IMOCKUP must specify
      the name of the directory where a Redfish/Swordfish mockup is
      located. Note that fishem does not do any checking of the input
      mockup. It is assumed that the input mockup provides a valid JSON
      description of the Redfish/Swordfish initial state for the
      emulator.

  --omockup OMOCKUP
  -om OMOCKUP
      Output mockup OMOCKUP when fishem is stopped. OMOCKUP must
      specify the name of the directory where the mockup is to be
      stored. If OMOCKUP already exists, it will be overwritten.

  --ifish IFISH
  -if IFISH
      Input JSON fish file IFISH when fishem is started. IFISH must
      specify the filename of a JSON file from a previous fishem run.
      Note that if an input mockup is also specified, then some of
      the state from the input JSON fish file may be overwritten by
      the state from the input mockup.

  --ofish OFISH
  -of OFISH
      Output JSON fish file OFISH when fishem is stopped. OFISH must
      specify the filename where the fish file is to be stored. If
      IFISH already exists, it will be overwritten.

  --port PORT
  -p PORT
      Set the port number that fishem will use for the RESTful API.
      A default value of 5000 will be used unless this is set to a
      different value by the command line or the configuration file.

  --https
      [THIS FUNCIONTALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]
      Use HTTPS for the RESTful API. A default value of "False" is
      used unless it is set otherwise by the command line or the
      configuration file. There is no short form for this argument.

  --fishdoctorEnabled
      [THIS FUNCIONTALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]
      Enable fishdoctor for the RESTful API. A default value of "False"
      is used unless it is set otherwise by the command line or the
      configuration file. There is no short form for this argument.


Configuration file for fishem

Most of the command line arguments can also be set by an optional JSON
configuration file named "fishem_config.json" in the folder/directory
where fishem.py is kept. This is a JSON key-value file, where the
supported entries are as follows:

  "imockup": "IMOCKUP"
      Input mockup IMOCKUP when fishem is started. IMOCKUP must specify
      the name of the directory where a Redfish/Swordfish mockup is
      located. Note that fishem does not do any checking of the input
      mockup. It is assumed that the input mockup provides a valid JSON
      description of the Redfish/Swordfish initial state for the
      emulator.

  "omockup": "OMOCKUP"
      Output mockup OMOCKUP when fishem is stopped. OMOCKUP must
      specify the name of the directory where the mockup is to be
      stored. If OMOCKUP already exists, it will be overwritten.

  "ifish": "IFISH"
      Input JSON fish file IFISH when fishem is started. IFISH must
      specify the filename of a JSON file from a previous fishem run.
      Note that if an input mockup is also specified, then some of
      the state from the input JSON fish file may be overwritten by
      the state from the input mockup.

  "ofish": "OFISH"
      Output JSON fish file OFISH when fishem is stopped. OFISH must
      specify the filename where the fish file is to be stored. If
      IFISH already exists, it will be overwritten.

  "port": "PORT"
      Set the port number that fishem will use for the RESTful API.
      A default value of 5000 will be used unless this is set to a
      different value by the command line or the configuration file.

  "https": "FLAG"
      [THIS FUNCIONTALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]
      Use HTTPS for the RESTful API if FLAG is set to "true". A default
      value of "false" will be used unless it is set otherwise by the
      command line or the configuration file.

  "fishdoctorEnabled": "FLAG"
      [THIS FUNCIONTALITY IS NOT YET FULLY IMPLEMENTED OR DOCUMENTED]
      Enable fishdoctor for the RESTful API if FLAG is set to "true".
      A default value of "false" is used unless it is set otherwise by
      the command line or the configuration file.

The configuration file is optional, but a basic "fishem_config.json"
configuration file is distributed with fishem. It sets all the input
and output file argument values to null (""), it sets the "port"
argument to 5000, and it sets the "https" and "fishdoctorEnabled"
arguments to "false". These are the same default values that fishem
uses when it cannot find the optional configuration file.

Command line arguments always override configuration file arguments,
so the basic "fishem_config.json" file effectively only serves as a
ready-to-use template.

Note: If fishemm is started with no arguments set by the command line
and no arguments set by the configuration file, then the emulator will
not have any Redfish/Swordfish state at all, and the RESTful API will
only be able to respond to requests for the Redfish protocol version.


Stopping fishem

Enter Control-C to stop fishem at any time after it is fully started
and ready to handle RESTful API operations. The current state of the
emulator will be saved in a JSON fish file named "lastfish.json" in
the folder/directory where fishem is kept, and then the current state
of the emulator will also be saved in any form that was requested
(mockup and/or fish file) on the command line that started fishem.

fishem always saves a JSON fish file named "lastfish.json" to ensure
that a developer can access the final state of an emulator run, even
when no output fish file or output mockup was requested when fishem
was started.

If needed, an output mockup can be created from "lastfish.json" by
running fishem. Start fishem with "lastfish.json" as an input JSON
fish file and specify a name for an output mockup. After fishem has
fully started, stop fishem with Control-C (before any RESTful API
operations have caused additional state changes) and the requested
output mockup will be created.

----
