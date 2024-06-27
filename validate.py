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
        for line in file:
            if 'error' in line:
                print("Invalid file")
                sys.exit(1)

print("File valid")