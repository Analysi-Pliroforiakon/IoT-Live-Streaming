package org.example;

import java.util.Properties;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.kafka.common.serialization.StringDeserializer;



public class kafkaFlinkReceiver {


    public static void StramConsumrer(String inputTopic, String server) throws Exception {
        StreamExecutionEnvironment environment = StreamExecutionEnvironment.getExecutionEnvironment();
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", server);
        properties.setProperty("group.id", "test");
        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers(server)
                .setTopics(inputTopic)
                .setGroupId("my-group")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        environment.fromSource(source, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .map(new MapFunction<String, String>() {
                    @Override
                    public String map(String value) throws Exception {
                        return value;
                    }
                })
                .print();
        environment.execute();

    }


    public static void main(String[] args) throws Exception {
        String inputTopic = "temperature";
        String server = "localhost:9092";
        StramConsumrer(inputTopic, server);
    }
}

//        stringInputStream.map(new MapFunction<String, String>() {
//            private static final long serialVersionUID = -999736771747691234L;
//
//            @Override
//            public String map(String value) throws Exception {
//                return "Receiving from Kafka : " + value;
//            }
//        }).print();
//
//        environment.execute();

//    public static KafkaSource<String> MyFlinkKafkaConsumer (
//            String topic, String kafkaAddress) {
//        return  KafkaSource.<String>builder()
//                .setBootstrapServers(kafkaAddress)
//                .setTopics("input-topic")
//                .setGroupId("my-group")
//                .setStartingOffsets(OffsetsInitializer.earliest())
//                .setValueOnlyDeserializer(new SimpleStringSchema())
//                .build();
//    }

