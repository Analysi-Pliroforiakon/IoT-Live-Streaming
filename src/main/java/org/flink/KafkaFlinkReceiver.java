package org.flink;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;

//create  a KafkaRecordDeserializationSchema


public class KafkaFlinkReceiver  {

    private KafkaSource<String> kafkaSource;
    public void myKafkaSource(String[] inputTopics, String server) throws Exception {

        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers(server)
                .setTopics(inputTopics)
                .setGroupId("my-group")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

       this.kafkaSource = source;
    }


    public KafkaSource<String> getKafkaSource() throws Exception {
        return this.kafkaSource;
    }
}


