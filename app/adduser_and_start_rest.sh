sudo mkdir /var/lib/graphsense-rest;
sudo chmod 777 /var/lib/graphsense-rest;
python3 adddefaultusers.py $1 $2;
python3 graphsenserest.py;