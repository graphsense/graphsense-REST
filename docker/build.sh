#!/bin/bash

if [[ -f "instance/config.py" ]]; then
    echo "Error: config file 'instance/config.py' does not exist."
fi

docker build -t graphsense-rest --build-arg NUM_WORKERS=3 .
