#Instructions:
# Run this script from the root directory of the project as follows:
# sh run.sh or ./run.sh

#!/bin/bash

# Set the PYTHONPATH and run the FastAPI application
export PYTHONPATH=$PYTHONPATH:/Users/vivekjadhav/Documents/github/fastapi-oneplus
uvicorn oneplus.main:app --reload --port 8001