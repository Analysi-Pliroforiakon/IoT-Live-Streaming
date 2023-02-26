#!/bin/bash

python ./dataStorageLayer/hbase_files/hbase_make_clear_tables.py
./presentationLayer/import_data_sources.sh