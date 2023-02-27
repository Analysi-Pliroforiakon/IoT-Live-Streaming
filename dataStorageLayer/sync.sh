#!/bin/bash
echo "Installing requirements"
pip3 install -r ./dataStorageLayer/requirements.txt

echo "Creating tables"
python3  ./dataStorageLayer/hbase_files/hbase_make_clear_tables.py


echo "Syncing data..."
python3 ./dataStorageLayer/syncData.py 
wait 