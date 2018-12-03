#!/bin/bash
docker stop graphsenserest
docker rm graphsenserest
docker run --restart=always -d --name graphsenserest -p 9000:9000 -it graphsenserest
docker ps -a
