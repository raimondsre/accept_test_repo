#/bin/bash
#This script will be executed right before running the NextFlow application.
#It is used to install any dependencies that might be necessary.
SCRIPT_DIR=$(dirname "$(realpath "$0")")
source "${SCRIPT_DIR}/venv/bin/activate" && python "${SCRIPT_DIR}/validate.py"
EXIT_CODE=$?

# Check if the Python script exited with an error
if [ $EXIT_CODE -ne 0 ]; then
    echo "Python script exited with an error."
    source "${SCRIPT_DIR}/failed_320.sh"
    sleep 10
    exit $EXIT_CODE
fi

# Continue if no error
echo "OK"