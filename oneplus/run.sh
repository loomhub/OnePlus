#!/bin/bash
# filepath: /Users/vivekjadhav/Documents/github/fastapi-oneplus/run.sh

# Instructions:
# 1. Make this script executable: chmod +x run.sh
# 2. Run this script from the root directory of the project: ./run.sh

# Set the PYTHONPATH to include the project root directory
export PYTHONPATH=$PYTHONPATH:/Users/vivekjadhav/Documents/github/fastapi-oneplus

# Run the FastAPI application using uvicorn
# Adding --host 0.0.0.0 to make it accessible from other devices
uvicorn oneplus.main:app --reload --host 0.0.0.0 --port 8001