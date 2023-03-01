from confluent_kafka import Consumer, KafkaError, KafkaException
import happybase
import sys
import argparse


KAFKA_BOOTSTRAP = 'localhost:9092'
HBASE_SERVER = 'localhost'
HBASE_PORT = 9090
TOPICS = ['raw','aggregated', 'late']
# TOPIC = args.table
RUNNING = True


conn = None
table = None

rawCount = 0
aggregatedCount = 0
lateCount = 0

def print_valid_msg(topic):
    global rawCount, aggregatedCount, lateCount
    if topic == 'raw':
        if rawCount%100 == 0:
            print("raw count: ", rawCount)
        rawCount += 1
    elif topic == 'aggregated':
        if aggregatedCount%5 == 0:
            print("aggregated count: ", aggregatedCount)
        aggregatedCount += 1
    elif topic == 'late':
        if lateCount > 0:
            print("late count: ", lateCount)
        lateCount += 1
    
    
   
def valid_table_and_connection(tableNames):
    conn = happybase.Connection( host=HBASE_SERVER, port=HBASE_PORT)

    # check if tables exist
    tables = conn.tables()
    # decode the byte array to string
    tables = [x.decode('utf-8') for x in tables]
    tablesDict ={}
    for name in tableNames:
        if name in tables:
            tablesDict[name] = conn.table(name)
        else:
            print("Table does not exist")
            exit(1)
    return conn, tablesDict


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

def basic_consume_loop(consumer, topics):
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
                msg_process(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    RUNNING = False

def validate_mgs(msg):
    topic = msg.topic()
    msg = msg.value().decode('utf-8')
    if topic != 'raw':
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
    return rowKey, dataToPut, timestamp, topic

def msg_process(msg):
    # logic of msg processing
    rowKey, dataToPut, timestamp, topic = validate_mgs(msg)
    # check if the connection is still valid    
    
    try:
        tablesDict[topic+"Data"].put(
            row=rowKey,
            data=dataToPut
        )
        print_valid_msg(topic)
    except Exception as e:
        print('ERROR: ', e)
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

tableNames = []
for topic in TOPICS:
    tableNames.append(topic+"Data")

consumer = Consumer(conf)
conn, tablesDict =  valid_table_and_connection(tableNames=tableNames)
basic_consume_loop(consumer, topics=TOPICS)
