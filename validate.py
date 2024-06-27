import os
import json
import sys

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

# Read input JSON file
with open(current_directory + "/input/input.json", "r") as f:
    input_data = json.load(f)
    uploaded_file = current_directory + input_data["field_user_text"]["filename"]
    with open(uploaded_file, 'r') as file:
        counter = 0
        for line in file:
            counter += 1
            if 'error' in line:
                print("Invalid file, we have error on line " + str(counter))
                sys.exit(1)

print("File valid")
