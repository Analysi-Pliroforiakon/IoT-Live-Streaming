#!/bin/sh

for topic in temperature energy motion water aggregated raw late
do
	kafka-topics --create --topic $topic --bootstrap-server kafka0:29092 --partitions 2
done
/bin/sh