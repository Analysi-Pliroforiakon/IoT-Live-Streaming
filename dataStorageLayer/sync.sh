#!/bin/bash

pip3 install -r ./dataStorageLayer/requirements.txt
# for raw late and aggregated run a loop to sync data
for table in raw late aggregated
do
    python3 ./dataStorageLayer/syncData.py -t $table
done