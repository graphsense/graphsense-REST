#!/bin/bash
docker stop graphsense-rest
docker rm graphsense-rest
docker run --restart=always -d --name graphsense-rest \
    --cap-drop all \
    -p 9000:9000 \
    -it graphsense-rest 
docker ps -a
