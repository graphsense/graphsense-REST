#!/bin/bash
docker stop graphsense-rest
docker rm graphsense-rest
docker run --restart=always -d --name graphsense-rest \
    --cap-drop all \
    -e SECRET_KEY="$(python -c 'import os; print(os.urandom(16))')" \
    -p 9000:9000 \
    -it graphsense-rest 
docker ps -a
