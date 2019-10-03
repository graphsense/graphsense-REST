#!/bin/bash

sudo mkdir /var/lib/graphsense-rest
sudo chmod 777 /var/lib/graphsense-rest
python3 add_user.py -u "$1" -p "$2" --uid 0
python3 graphsenserest.py
