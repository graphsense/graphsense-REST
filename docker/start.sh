#!/bin/bash
docker stop graphsense_rest
docker rm graphsense_rest
docker run --restart=always -d --name graphsense_rest -p 9000:9000 -it graphsense_rest
docker ps -a
