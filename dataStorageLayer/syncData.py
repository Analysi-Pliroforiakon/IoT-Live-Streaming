from confluent_kafka import Consumer, KafkaError, KafkaException
import happybase
import sys
import argparse

# you must specify the table of kafka

parser = argparse.ArgumentParser(
    description="Sync your data from kafka topic to hbase",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

requiered = parser._action_groups.pop()
requiered.add_argument('-t', '--table', type=str, default='raw',
                help='Table name in HBase', required=True)
parser._action_groups.append(requiered)
args = parser.parse_args()


KAFKA_BOOTSTRAP = 'localhost:9092'
HBASE_SERVER = 'localhost'
HBASE_PORT = 9090
# TOPICS = ['raw','aggregated', 'late']
TOPIC = args.table
RUNNING = True


conn = None
table = None


def valid_table_and_connection(tableName):
    pool = happybase.ConnectionPool(size=3, host=HBASE_SERVER, port=HBASE_PORT)
    with pool.connection() as conn:
    
        print("Connection: ",conn)
        # check if tables exist
        tables = conn.tables()
        # decode the byte array to string
        tables = [x.decode('utf-8') for x in tables]

        print("Tables: ",tables)
        if tableName not in tables:
            print("Table does not exist")
            exit(1)
        else :
            table = conn.table(tableName)
            print("Table exists")
    return pool, table


def valid_datetime(table):
    data = table.scan(columns=['cf:datetime'])
    # decode the byte array to string
    data = list(data)
    if len(data) == 0:
        return '1000-01-01 00:00'
    data = [x[1] for x in data]
    data = [ y.decode("UTF-8") for x in data for y in x.values() ]
    max_timestamp = max(data)
    return max_timestamp

def basic_consume_loop(consumer, topics, validate=False, max_timestamp=None):
    try:
        consumer.subscribe(topics)

        while RUNNING:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg, validate, max_timestamp=max_timestamp)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    RUNNING = False

def validate_mgs(msg):
    msg = msg.value().decode('utf-8')
    print(msg, type(msg))

    # split data into sensor, timestamp and value
    parsed = msg.split("|")
    
    # SENSOR
    sensor = parsed[0]
    # remove extra whitespace
    sensor = sensor.strip()

    
    # TIMESTAMP
    timestamp = parsed[1]
    # remove extra whitespace
    timestamp = timestamp.strip()

    # VALUE
    value = parsed[2]
    # convert to float
    value = (value)


    # put the data in HBase
    rowKey = timestamp + "-" + sensor
    rowKey = rowKey.encode('utf-8')

    dataToPut = {
        'cf:sensor'.encode('utf-8'): sensor.encode('utf-8'),
        'cf:value'.encode('utf-8'): value.encode('utf-8'),
        'cf:datetime'.encode('utf-8'): timestamp.encode('utf-8')
    }
    return rowKey, dataToPut, timestamp

def msg_process(msg, validate=False, max_timestamp=None):
    # logic of msg processing
    rowKey, dataToPut, timestamp = validate_mgs(msg)

    if validate and timestamp <= max_timestamp:
        print(timestamp, max_timestamp)
        print("-----------------------------------------------------------------------")
        print("Data is late")
        print(dataToPut)
        print("-----------------------------------------------------------------------")
        return
    # check if conn is valid
    with pool.connection() as conn:  
        try:
            table.put(
                row=rowKey,
                data=dataToPut
            )
        except Exception as e:
            print(e)
            print("-----------------------------------------------------------------------")
            print("Error in putting data")
            print(dataToPut)
            print("-----------------------------------------------------------------------")
            pass





conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': "foo",
    'auto.offset.reset': 'earliest'
    
}


tableName = TOPIC + "Data"
consumer = Consumer(conf)
pool, table =  valid_table_and_connection(tableName=tableName)
# max timestamp is the latest timestamp already in the table .
# if TOPIC == 'aggregated' :
#     max_timestamp = valid_datetime(table=table)
#     basic_consume_loop(consumer, TOPICs=[TOPIC], validate=True, max_timestamp=max_timestamp)
#     continue
basic_consume_loop(consumer, topics=[TOPIC])
