from confluent_kafka import Consumer, KafkaError, KafkaException
import happybase
import sys



KAFKA_BOOTSTRAP = 'localhost:9092'
HBASE_SERVER = 'localhost'
HBASE_PORT = 9090
TOPIC_NAME = 'aggregated'
TABLE_NAME = TOPIC_NAME+'Data'
RUNNING = True


conn = None
table = None


conn = happybase.Connection(
    host=HBASE_SERVER,
    port=HBASE_PORT
)


# take the largest data from the table with column "cf:timestamp"
table = conn.table(TABLE_NAME)
data = table.scan(columns=['cf:datetime'])
# decode the byte array to string
data = list(data)
print(data[:1])
data = [x[1] for x in data]
print(data[:1])
# data = [y for y in x.values() for x in data]
data = [ y.decode("UTF-8") for x in data for y in x.values() ]
print(data)
max_timestamp = max(data)
print(max_timestamp)