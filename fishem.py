# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
Fish emulator.

Emulates a Redfish/Swordfish service using mockups as input.
Capable of capturing and saving state as an output mockup.

Run this command to see the available command line parameters:
    python fishem.py --help
"""

# Standard library module imports
import json                     # JSON handling
import os                       # CLI and file I/O handling
import signal                   # Control-C handling
import sys                      # Control-C handling
import importlib                # API module imports

# Third party module imports
# None

# Local module imports
import fishem_version           # fishem version
import fishem_configure         # Set up configuration parameters
import fishem_fishfileio        # Fish file input and output
import fishem_mockupio          # Mockup input and output
import fishem_restops           # Set up and start REST operations
import fish_data                # Data shared with all API modules
# Note: API modules are programmatically imported in main()

# Constants
# None


# Function: signal_handler()

def signal_handler(sig, frame):
    """Catch Control-C to do final cleanup before exiting.
    """
    print('\nfishem stopped with Control-C --------------------------')

    # Save the current fish in the file 'lastfish.json'
    fishem_fishfileio.output('lastfish.json')

    # Save the current fish in an output fish file, if requested
    if fishemconfig['ofish']:
        fishem_fishfileio.output(fishemconfig['ofish'])

    # Save the current fish as an output mockup, if requested
    if fishemconfig['omockup']:
        fishem_mockupio.output(fishemconfig['omockup'])

    # End program
    print('fishem ended normally ----------------------------------')
    sys.exit(0)


# Initialization for catching Control-C
signal.signal(signal.SIGINT, signal_handler)


# main()

def main():
    """main()

    Determines configuration parameters and launches the emulator.
    The configuration parameters control startup, shutdown, and
    some of the operational behaviors of the fish emulator.
    """

    # fishemconfig is a dictionary for configuration paramters;
    # it's global to allow access by the signal_handler() above
    global fishemconfig

    # Get fishem configuration parameters, name, and version
    fishemconfig = fishem_configure.getconfig()
    fishemconfig['name'] = __name__
    fishemconfig['version'] = fishem_version.__version__

    # Share fishem configuration parameters with API modules
    fish_data.fishem_config = fishemconfig

    # Start fishem initialization
    print('fishem initialization ----------------------------------')

    # Import API modules so they can set up initial data objects
    for dirpath, dirnames, filenames in os.walk('fishapis'):
        if dirpath == 'fishapis':
            for fn in filenames:
                if fn == '__init__.py': continue
                api_module = 'fishapis.' + fn.replace('.py', '')
                importlib.import_module(api_module)

    # Load an input fish, if requested
    if fishemconfig['ifish']:
        fishem_fishfileio.input(fishemconfig['ifish'])

    # Load an input mockup, if requested
    if fishemconfig['imockup']:
        fishem_mockupio.input(fishemconfig['imockup'])

    # Start normal REST operations
    print('fishem starting ----------------------------------------')
    fishem_restops.startup(fishemconfig)

    # End of main()


if __name__ == '__main__':
    main()      # If this is the main module, run main()
else:
    pass        # If this module is imported, do nothing
