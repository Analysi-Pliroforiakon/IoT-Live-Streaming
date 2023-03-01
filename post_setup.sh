#!/bin/bash

echo "Flink" &
java -jar ./liveStreamingLayer/flinkExecutable.jar &


./deviceLayer/produce.sh &


./dataStorageLayer/sync.sh &

# echo "Presentation" &
./presentationLayer/import_data_sources.sh &

wait