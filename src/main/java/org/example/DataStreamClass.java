package org.example;

import org.apache.flink.api.common.eventtime.TimestampAssigner;
import org.apache.flink.api.common.eventtime.WatermarkGenerator;
import org.apache.flink.api.common.eventtime.WatermarkOutput;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.connector.sink.Sink;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.streaming.api.datastream.AllWindowedStream;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.KeyedStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.AssignerWithPeriodicWatermarks;
import org.apache.flink.streaming.api.functions.AssignerWithPunctuatedWatermarks;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.streaming.api.watermark.Watermark;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.util.Collector;

import java.text.SimpleDateFormat;
import java.time.Duration;
import java.util.Optional;
import java.util.Properties;

public class DataStreamClass {

    public void startFlinking(StreamExecutionEnvironment env, AggregateFunction<ourTuple, aggregateHelper, ourTuple> quarterAggregateFunction, AggregateFunction<ourTuple, aggregateHelper, ourTuple> dailyAggregateFunction, AggregateFunction<ourTuple, aggregateHelper, ourTuple> restAggregateFunction, KafkaSource<String> kafkaSource, String jobName, int dailyPeriod) throws Exception {

    	SingleOutputStreamOperator<ourTuple> dataStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .flatMap(new Splitter())
                .assignTimestampsAndWatermarks(
                        WatermarkStrategy.
                        <ourTuple>forMonotonousTimestamps()
                                .withTimestampAssigner((event, timestamp) -> event.toTimestampLong())
                                .withIdleness(Duration.ofSeconds(1))
                );
    	
    	SingleOutputStreamOperator<ourTuple> newStream = dataStream
                .filter(value -> !value.sensor.contains("tot"))
                .keyBy(value -> value.sensor)
                .window(TumblingEventTimeWindows.of(Time.days(1)))
                .aggregate(quarterAggregateFunction);
                
    	SingleOutputStreamOperator<ourTuple> totStream = dataStream
                .filter(value -> value.sensor.contains("tot"))
                .keyBy(value -> value.sensor)
                .window(SlidingEventTimeWindows.of(Time.days(2), Time.days(1)))
                .aggregate(dailyAggregateFunction);
        
    	DataStream<ourTuple> finalStream = newStream.union(totStream);
        
    	
    	KafkaSink<ourTuple> sink = KafkaSink.<ourTuple>builder()
                .setBootstrapServers("localhost:9092")
                .setRecordSerializer(
                        KafkaRecordSerializationSchema.builder()
                                .setTopic("aggrs")
                                .setValueSerializationSchema(
                                        new OurTupleSerializationSchema()
                                )
                                .build()
                )

                .build();
    	//Checking if topic is energy or water. If true calculate rest aggregator
    	if(jobName.contains("Sum")) {
    	    SingleOutputStreamOperator<ourTuple> restStream =  finalStream
    	    		.windowAll(TumblingEventTimeWindows.of(Time.days(1)))
    	    		.aggregate(restAggregateFunction);
    	    
            finalStream.sinkTo(sink);
            System.out.println("Adding a sink done");
            
            restStream.sinkTo(sink);
            System.out.println("Adding rest sink done");
    	    
    	}
        
    	//If topic is not energy or water, do not calculate rest aggregator
    	else {

            finalStream.sinkTo(sink);
            System.out.println("Adding a sink done");
            
    	}
    		
    }

    static SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy:MM:dd HH:mm");

    public static class Splitter implements FlatMapFunction<String, ourTuple> {
        /**
		 * 
		 */
		private static final long serialVersionUID = 1L;

		@Override
        public void flatMap(String input, Collector<ourTuple> output) throws Exception {
            String[] words = input.split("\\|");
           // Check if float
            float value;
            try {
                Float.parseFloat(words[2]);
                value = Float.parseFloat(words[2]);
            } catch(NumberFormatException e) {
                // Not float
            	value = 0f; 
            }
            
            ourTuple tuple = new ourTuple();
			//Remove space at the end of sensor type string
            tuple.sensor = Optional.ofNullable(words[0])
            		   .filter(sStr -> sStr.length() != 0)
            		   .map(sStr -> sStr.substring(0, sStr.length() - 1))
            		   .orElse(words[0]);
            tuple.datetime = Optional.ofNullable(words[1])
         		   .filter(sStr -> sStr.length() != 0)
         		   .map(sStr -> sStr.substring(1, sStr.length() - 1))
         		   .orElse(words[1]);
            tuple.value = value;
            output.collect(tuple);
        }
    }
    
}
