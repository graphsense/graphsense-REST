#!/bin/bash
docker stop graphsense-rest
docker rm graphsense-rest
docker run --restart=always -d --name graphsense-rest -p 9000:9000 \
           --sysctl net.core.somaxconn=65536 -it graphsense-rest
docker ps -a
