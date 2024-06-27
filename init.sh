#!/bin/bash
#This script will be executed right before running the NextFlow application.
#It is used to install any dependencies that might be necessary.
SCRIPT_DIR=$(dirname "$(realpath "$0")")

python3 -m venv ./venv
source ./venv/bin/activate

OUTPUT=$(python "${SCRIPT_DIR}/validate.py")
EXIT_CODE=$?

# Check if the Python script exited with an error
if [ $EXIT_CODE -ne 0 ]; then
    echo "Python script exited with an error " $OUTPUT
    "${SCRIPT_DIR}/failed_320.sh" "$OUTPUT"
    sleep 10
    exit $EXIT_CODE
fi

# Continue if no error
echo "No file validation errors"

pip install numpy docx python-docx matplotlib scipy
rm -rf ./output/
mkdir ./output && mkdir ./output/files
deactivate
echo "Virtual environment created and dependencies installed"