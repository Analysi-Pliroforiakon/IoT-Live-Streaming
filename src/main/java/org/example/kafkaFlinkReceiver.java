package org.example;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

//create  a KafkaRecordDeserializationSchema


public class kafkaFlinkReceiver {


    public static KafkaSource<String> myKafkaSource(String[] inputTopics, String server) throws Exception {

        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers(server)
                .setTopics(inputTopics)
                .setGroupId("my-group")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        return source;
    }


    public static KafkaSource<String> getKafkaEnv() throws Exception {
        String[] inputTopics = {"temperature"};
        String server = "localhost:9092";
        return myKafkaSource(inputTopics, server);
    }
}


