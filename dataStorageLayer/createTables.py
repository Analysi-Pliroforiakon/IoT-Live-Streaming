#!/usr/bin/python3

# deletes every table in hbase
import happybase
import sys

HBASE_SERVER = '172.29.194.94'
HBASE_PORT =9090




# connect to HBase's thrift api
conn = happybase.Connection(
    host=HBASE_SERVER, 
    )

# check if tables exist
tables = conn.tables()
print("Tables: ",tables)
# create column families for HBase
families = {
    'cf' : dict(),
}

tables = [ "rawData2", "aggregatedData", "lateEventsTable"]

# create table to store avg values for each sensor
# every row has the data's timestamp as a key and avg_value as column
for table in tables:
    print("Creating table ",table)
    conn.create_table(table, families)
    
print("Done creating tables")