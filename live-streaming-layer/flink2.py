from flink.connectors.kafka import KafkaDeserializationSchema
from flink.connectors.hbase import HbaseSinkFunction
from flink.functions import Function
FILE = '/mnt/c/Users/Nikolas/Downloads/flink-sql-connector-kafka-1.16.0.jar'

# Define a function to deserialize the data from the Kafka stream
class KafkaDeserializationFunction(KafkaDeserializationSchema):
    def deserialize(self, message: bytes) -> any:
        # Deserialize the message and return the value
        return int(message.decode())

# Define a function to write the aggregated data to HBase
class HBaseSinkFunction(HbaseSinkFunction):
    def invoke(self, value: any, context: SinkFunction.Context) -> None:
        # Write the value to HBase
        self.table.put(b'row1', {b'cf1:sum': str(value).encode()})

# Define a function to perform the aggregation
class AggregationFunction(Function):
    def process(self, value: any, context: Function.Context) -> any:
        # Sum the values in the stream
        self.sum += value
        return self.sum

# Set up the Flink job
env = ExecutionEnvironment.get_execution_environment()

# Read data from Kafka
kafka_stream = env.add_source(
    FlinkKafkaConsumer(
        'my-topic',
        KafkaDeserializationFunction(),
        properties={
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'flink-consumer'
        }
    )
)

# Apply the aggregation function to the stream
aggregated_stream = kafka_stream.map(AggregationFunction())

# Write the aggregated data to HBase
aggregated_stream.add_sink(HBaseSinkFunction())

# Execute the Flink job
env.execute()
