#!/bin/bash
docker build -t graphsense-rest --build-arg NUM_WORKERS=3 .
