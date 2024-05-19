#!/bin/bash
#This script will be executed right before running the NextFlow application.
#It is used to install any dependencies that might be necessary.
python3 -m venv ./venv
source ./venv/bin/activate
pip install numpy docx python-docx matplotlib scipy
rm -rf ./output/
mkdir ./output && mkdir ./output/files
deactivate
echo "Virtual environment created and dependencies installed"