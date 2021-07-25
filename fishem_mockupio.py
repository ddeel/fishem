# Copyright (c) 2021 by Don Deel. All rights reserved.

"""
Handle mockup I/O for fishem.
"""

# Standard library module imports
import json                     # JSON handling
import os                       # File I/O handling

# Third party module imports
import xmltodict                # XML handling for mockups

# Local module imports
from fish_data import fish      # Fish data

# Constants
FISH_KEY_BASE = '/redfish/v1'


# Function: input()

def input(imockup_dir):
    """Load the mockup from 'imockup_dir' into the current fish.
    """

    # Ensure the input mockup directory exists
    if not os.path.exists(imockup_dir):
        print('Input mockup not found', imockup_dir)
        # Failure exit; cannot continue
        print('Input mockup not loaded, fishem ending')
        exit(1)

    for dirpath, dirnames, filenames in os.walk(imockup_dir):
        for file_name in filenames:

            # Only deal with files of interest
            if file_name not in ['index.json', 'index.xml']:
                continue

            # Set up file_path, rel_path, and fish_key
            file_path = os.path.join(dirpath, file_name)
            if dirpath == imockup_dir:      # Service root case
                rel_path = ''
                fish_key = FISH_KEY_BASE
            else:                           # All other cases
                # Normalize slashes and remove topdir from rel_path
                rel_path = dirpath.replace('\\', '/')
                rel_path = rel_path.replace(imockup_dir + '/', '')
                fish_key = FISH_KEY_BASE + '/' + rel_path

            # Get data from individual mockup files
            if file_name == 'index.xml' and rel_path == '$metadata':
                # Get the $metadata document (index.xml) file data
                # Convert XML to JSON before storing it in fish
                try:
                    json_data = xmltodict.parse(
                        open(file_path, 'r').read())
                except Exception as error:
                    print('Failed to read XML data with this error:')
                    print(error)
                    # Failure exit; cannot continue
                    print('Input mockup not loaded, fishem ending')
                    exit(1)
            else:
                # Get the JSON data for a fish object (index.json)
                try:
                    json_data = json.load(open(file_path))
                except Exception as error:
                    print('Failed to read JSON data with this error:')
                    print(error)
                    # Failure exit; cannot continue
                    print('Input mockup not loaded, fishem ending')
                    exit(1)

            # Store the JSON data for a fish object in fish
            fish[fish_key] = json_data

    # Success return
    print('Loaded the mockup in "', imockup_dir, '"', sep='')
    return

    # End of input()


# Function: output()

def output(omockup_dir):
    """Save the current fish as a mockup in 'omockup_dir'.
    """

    # Delete the old output mockup directory hierarchy if it exists;
    # must build a new output mockup directory hierarchy every time
    if os.path.exists(omockup_dir):
        # Walk the existing mockup directory hierarchy (bottom-up)
        for dirpath, dirnames, filenames in os.walk(omockup_dir, \
                topdown = False):
            try:
                # Delete any files in a directory before
                # deleting the directory itself
                for file_name in filenames:
                    file_path = os.path.join(dirpath, file_name)
                    os.remove(file_path)
                # Delete the directory
                os.rmdir(dirpath)
            except Exception as error:
                print('Failed to remove old output mockup directory "',
                    omockup_dir, '":', sep='')
                print(error)
                # Failure exit; cannot continue
                print('Output mockup not saved, fishem ending')
                exit(1)

    # Create a new directory hierarchy for the output mockup
    for fish_key in fish:
        # The Redfish version object is not included in mockups
        if fish_key == '/redfish':
            continue
        dir_path = fish_key.replace(FISH_KEY_BASE, omockup_dir)
        dir_path = os.path.normpath(dir_path)
        if not os.path.isdir(dir_path):
            try:
                os.makedirs(dir_path)
            except Exception as error:
                print('Failed to create output mockup directory "',
                    dir_path, '":', sep='')
                print(error)
                # Failure exit; cannot continue
                print('Output mockup not saved, fishem ending')
                exit(1)

    # Save the fish objects in the output mockup directories
    for fish_key in fish:
        dir_path = fish_key.replace(FISH_KEY_BASE, omockup_dir)
        dir_path = os.path.normpath(dir_path)

        # The Redfish Version object is not included in mockups
        if fish_key == '/redfish':
            continue

        # Save the Redfish $metadata document as 'index.xml'
        if fish_key == '/redfish/v1/$metadata':
            file_path = os.path.join(dir_path, 'index.xml')
            xml_data = xmltodict.unparse(fish[fish_key],
                pretty=True)
            try:
                open(file_path, 'w').write(xml_data)
            except Exception as error:
                print('Failed to save output mockup XML data in "',
                    file_path, '":', sep='')
                print(error)
                # Failure exit; cannot continue
                print('Output mockup not saved, fishem ending')
                exit(1)
            continue

        # Save the fish object as 'index.json'
        file_path = os.path.join(dir_path, 'index.json')
        json_data = json.dumps(fish[fish_key], indent=4)
        try:
            open(file_path, 'w').write(json_data)
        except Exception as error:
            print('Failed to save output mockup JSON data in "',
                    file_path, '":', sep='')
            print(error)
            # Failure exit; cannot continue
            print('Output mockup not saved, fishem ending')
            exit(1)

    # Success return
    print('Saved the current fish as a mockup in "',
          omockup_dir, '"', sep='')
    return

    # End of output()
