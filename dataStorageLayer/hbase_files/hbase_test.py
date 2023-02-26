import happybase
import time
import datetime
connection = happybase.Connection('127.0.0.1', 9090)

table = connection.table('rawData')

# Get current unix timestamp.
timestamp = time.time()
# convert to datetime
timestamp = datetime.datetime.fromtimestamp(timestamp)

table.put(f'{timestamp}-TH1', {'cf:sensor': 'TH1', 'cf:value': '25', 'cf:datetime': f'{timestamp}'})
table.put(f'{timestamp}-TH1', {'cf:sensor': 'TH2', 'cf:value': '35', 'cf:datetime': f'{timestamp}'})
table.put(f'{timestamp}-TH1', {'cf:sensor': 'TH3', 'cf:value': '40', 'cf:datetime': f'{timestamp}'})
for k, data in table.scan():
    print(k, data)