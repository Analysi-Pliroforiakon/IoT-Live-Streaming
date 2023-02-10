package org.example;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.util.Collector;

import java.util.Properties;

public class DataStreamClass {

    public void startFlinking(StreamExecutionEnvironment env, AggregateFunction aggregateFunction, KafkaSource<String> kafkaSource, String jobName, int period) throws Exception {

        SingleOutputStreamOperator dataStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .flatMap(new Splitter())
                .keyBy(value -> value.sensor)
                .window(TumblingProcessingTimeWindows.of(Time.seconds(period)))
                .aggregate(aggregateFunction);
        dataStream.print();

//    add a sink
        KafkaSink<Tuple2<aggregateHelper, Float>> sink = KafkaSink.<Tuple2<aggregateHelper, Float>>builder()
                .setBootstrapServers("localhost:9092")
                .setRecordSerializer(
                        KafkaRecordSerializationSchema.builder()
                                .setTopic("aggrs")
                                .setValueSerializationSchema(
                                        new TupleSerializationSchema()
                                )
                                .build()
                )

                .build();
        dataStream.sinkTo(sink);
        System.out.println("Adding a sink done");


    }



    public static class Splitter implements FlatMapFunction<String, ourTuple> {
        @Override
        public void flatMap(String input, Collector<ourTuple> output) throws Exception {
            String[] words = input.split("\\|");
            float value = Float.parseFloat(words[2]);
            ourTuple tuple = new ourTuple();
            tuple.sensor = words[0];
            tuple.datetime = words[1];
            tuple.value = value;
            output.collect(tuple);
        }
    }
}
