import happybase
import time
import datetime
connection = happybase.Connection('127.0.0.1', 9090)

table = connection.table('raw')

# Get current unix timestamp.
timestamp = time.time()
# convert to datetime
timestamp = datetime.datetime.fromtimestamp(timestamp)

table.put(f'{timestamp}-TH1', {'f:measurement': 'TH1', 'f:value': '25', 'f:timestamp': f'{timestamp}'})
table.put(f'{timestamp}-TH2', {'f:measurement': 'TH2', 'f:value': '35', 'f:timestamp': f'{timestamp}'})
table.put(f'{timestamp}-TH3', {'f:measurement': 'TH3', 'f:value': '40', 'f:timestamp': f'{timestamp}'})
for k, data in table.scan():
    print(k, data)