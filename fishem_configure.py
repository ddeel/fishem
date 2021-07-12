# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
Handle configuration setup for fishem.
"""

# Standard library module imports
import argparse                 # CLI handling
import json                     # JSON handling
import os                       # File I/O handling

# Third party module imports
# None

# Local module imports
from fishem_version import __version__      # fishem version

# Constants
FISHEM_CONFIG_FILE = 'fishem_config.json'


# Function: getconfig()

def getconfig():
    """Establish fishem configuration parameters
    """

    # Set up configuration defaults for all parameters
    fishemconfig = {'ifish': None,
                    'ofish': None,
                    'imockup': None,
                    'omockup': None,
                    'port': 5000,
                    'https': False,
                    'fishdoctorEnabled': False}

    # Read in an optional fishem config file containing one or more
    # arguments. Arguments in this file override the default values.
    if os.path.exists(FISHEM_CONFIG_FILE):
        try:
            jsonconfig = json.load(open(FISHEM_CONFIG_FILE))
        except Exception as error:
            print('Failed to read the fishem config file:')
            print(error)
            exit(0)
        for key in jsonconfig:
            fishemconfig[key] = jsonconfig[key]
    else:
        print('Running without a fishem config file')

    # Handle optional command line arguments. When present, these
    # arguments override the corresponding configuration file values
    # and/or default values.
    # TODO: Allow multiple input mockups to be specified                # Note
    # TODO: Finish implemneting https functionality                     # Note
    # TODO: Finish implementing fishdoctorEnable functionality          # Note
    parser = argparse.ArgumentParser(
        description = 'Fish Emulator version ' + __version__,
        epilog = 'Developed by Don Deel')
    parser.add_argument('--version', '-v', '-V', action='store_true',
        help='Show version and exit')
    parser.add_argument('--ifish', '-if',
        help='Input JSON fish file name')
    parser.add_argument('--ofish', '-of',
        help='Output JSON fish file name')
    parser.add_argument('--imockup', '-im',
        help='Input mockup directory name')
    parser.add_argument('--omockup', '-om',
        help='Output mockup directory name')
    parser.add_argument('--port', '-p', type = int,
        help='Port number for the API')
    parser.add_argument('--https', action='store_true',
        help='Use HTTPS for the API')
    parser.add_argument('--fishdoctorEnabled', action='store_true',
        help='Enable fishdoctor API')
    args = parser.parse_args()
    if args.version:            # Show version and exit
            print('fishem version', __version__)
            exit(0)
    if not(args.ifish==None): fishemconfig['ifish'] = args.ifish
    if not(args.ofish==None): fishemconfig['ofish'] = args.ofish
    if not(args.imockup==None): fishemconfig['imockup'] = args.imockup
    if not(args.omockup==None): fishemconfig['omockup'] = args.omockup
    if not(args.port==None): fishemconfig['port'] = args.port
    if not(args.https==None): fishemconfig['https'] = args.https
    if not(args.fishdoctorEnabled==None):
        fishemconfig['fishdoctorEnabled'] = args.fishdoctorEnabled

    # Return configuration parameters as a dictionary
    return fishemconfig

    # End of getconfig()
