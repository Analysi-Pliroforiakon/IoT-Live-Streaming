#!/bin/bash


java -jar ./liveStreamingLayer/flinkExecutable.jar &


./deviceLayer/produce.sh &


./dataStorageLayer/sync.sh &


./presentationLayer/import_data_sources.sh &

wait