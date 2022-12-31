from confluent_kafka import Producer
import socket

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


print(socket.gethostname())
conf = {
    'bootstrap.servers': "localhost:9092, localhost9192",
    'client.id': socket.gethostname()
}

producer = Producer(conf)

producer.produce('test_topic', key='toulis', value='test message', callback=acked)
producer.poll(2) # wait for events. Callback will be invoked here

