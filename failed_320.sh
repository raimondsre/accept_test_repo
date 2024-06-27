#/bin/bash
DATA=${1:-}
# Run the curl command with the provided data
if [ -z "$DATA" ]; then
  # If no data provided, post without data
  echo "NO DATA"
else
  # Post with data
  echo "DATA"
fi
echo "This script will be called after failure of the program due to unsupported (corrupt) files. The contents will be replaced automatically."