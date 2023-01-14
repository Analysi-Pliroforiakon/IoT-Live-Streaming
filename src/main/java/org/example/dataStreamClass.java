package org.example;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;

import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.util.Collector;
public class dataStreamClass {


    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        KafkaSource kafkaSource = kafkaFlinkReceiver.getKafkaEnv();

        DataStream<Float> dataStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .flatMap(new Splitter())
                .keyBy(value -> value)
                .window(TumblingProcessingTimeWindows.of(Time.seconds(30)))
                .sum(0);

        dataStream.print();

        env.execute("Window WordCount");
    }

    public static class Splitter implements FlatMapFunction<String, Float> {
        @Override
        public void flatMap(String sentence, Collector<Float> out) throws Exception {
            System.out.println("sentence: " + sentence);
            String [] words = sentence.split("\\|");
            for (String word : words) {
                System.out.println("word: " + word);
            }

            float Value = Float.parseFloat(words[2]);
            out.collect(Value);
        }
    }
}
