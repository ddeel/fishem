# Copyright (c) 2021-2022 by Don Deel. All rights reserved.

"""
Handle fish file I/O for fishem.
"""

# Standard library module imports
import json                     # JSON handling
import os                       # File I/O handling

# Third party module imports
# None

# Local moduleimports
from fish_data import fish      # Fish data

# Constants
# None


# Function: input()

def input(ifish_file):
    """Load the fish file 'ifish_file' into the current fish.
    """

    if not os.path.exists(ifish_file):
        print('Failed to find the fish file "',
              ifish_file, '"', sep='')
        # Failure exit; cannot continue
        print('Input fish file not loaded, fishem ending')
        exit(1)

    try:
        input_dict = json.load(open(ifish_file))
    except Exception as error:
        print('Failed to read the fish file "', ifish_file,
              '":', sep='')
        print(error)
        # Failure exit; cannot continue
        print('Input fish file not loaded, fishem ending')
        exit(1)

    for key in input_dict:
        fish[key] = input_dict[key]

    # Success return
    print('Loaded the fish file "', ifish_file, '"', sep='')
    return

    # End of input()


# Function: output()

def output(ofish_file):
    """Save the current fish as the fish file 'ifish_file'.
    """

    try:
        json.dump(fish, open(ofish_file, 'w'))
    except Exception as error:
        print('Failed to save the current fish in "',
              ofish_file, '":', sep='')
        print(error)
        # Failure exit; cannot continue
        exit(1)

    # Success return
    print('Saved the current fish as a JSON file in "',
        ofish_file, '"', sep='')
    return

    # End of output()
