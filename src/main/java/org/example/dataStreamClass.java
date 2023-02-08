package org.example;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.FlatMapFunction;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;

public class dataStreamClass {


    private static Object v;

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        KafkaSource<String> kafkaSource = kafkaFlinkReceiver.getKafkaEnv();

        SingleOutputStreamOperator<Tuple2<AverageAggregator.MyAverage, Float>> dataStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .flatMap(new Splitter())
                .keyBy(value -> value.sensor)
                .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
                .aggregate(new AverageAggregator());
        System.out.println("done with datastream for 10 seconds");
        dataStream.print();

        env.execute("Window WordCount");
    }

    public static class Splitter implements FlatMapFunction<String, ourTuple> {
        @Override
        public void flatMap(String input, Collector< ourTuple > output) throws Exception {
//            System.out.println("sentence: " + sentence);
            String [] words = input.split("\\|");
            float value = Float.parseFloat(words[2]);
            ourTuple tuple = new ourTuple();
            tuple.sensor = words[0];
            tuple.datetime = words[1];
            tuple.value = value;
            output.collect(tuple);
        }
    }
}
