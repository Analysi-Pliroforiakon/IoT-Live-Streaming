import confluent_kafka
import socket

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Acked message: %s" % (str(msg.value())))

class ProducerClass(confluent_kafka.Producer):
    def __init__(self):
        conf = {
            'bootstrap.servers': "localhost:9092, localhost9192",
            'client.id': socket.gethostname()
        }
        print('producer config used:', conf)

        super().__init__(conf)

    def produce(self, sensor, curr_datetime, value):
        if sensor in ['TH1', 'TH2']:
            topic = 'temperature'
        elif sensor in ['HVAC1', 'HVAC2', 'MiAC1', 'MiAC2', 'Etot']:
            topic = 'energy'
        elif sensor in ['Mov1']:
            topic = 'motion'
        elif sensor in ['W1', 'Wtot']:
            topic = 'water'
        else:
            topic = 'new_topic'

        msg = f'{sensor} | {curr_datetime} | {value}'
        print(f'\t{sensor}: {msg}')
        super().produce(topic, key=sensor, value=msg, callback=acked)