#!/bin/bash

rm -rf dataStorageLayer/hbase_files/data
mkdir -p dataStorageLayer/hbase_files/data
docker-compose up