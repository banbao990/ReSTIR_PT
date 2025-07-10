# create a new file called `slangdconfig.json`
# for slang intellisense

import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))


def create_slangdconfig():
    config = {
        "slang.additionalSearchPaths": [
            os.path.join(PROJECT_DIR, 'Source', 'Falcor')
        ]
    }

    # Define the path for the new file
    file_path = os.path.join(PROJECT_DIR, 'slangdconfig.json')

    # Write the configuration to the file
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)
    print("slangdconfig.json created successfully.")


if __name__ == "__main__":
    create_slangdconfig()
