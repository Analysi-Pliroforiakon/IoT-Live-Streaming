package org.flink;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.util.Collector;
import org.apache.flink.util.OutputTag;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.util.Optional;

public class DataStreamClass {

    public void startFlinking(StreamExecutionEnvironment env, AggregateFunction<ourTuple, aggregateHelper, ourTuple> quarterAggregateFunction, AggregateFunction<ourTuple, aggregateHelper, ourTuple> dailyAggregateFunction, AggregateFunction<ourTuple, aggregateHelper, ourTuple> restAggregateFunction, KafkaSource<String> kafkaSource, String jobName) throws Exception {
        
    	//This is used to handle rejected late events
    	final OutputTag<ourTuple> lateOutputTag = new OutputTag<ourTuple>("late-data"){
			private static final long serialVersionUID = 1L;};
    	
    	//Out of orderness is set to 2 days for all sensors
		//This means that all aggregations will be sent to the sink 2 days after the end of the corresponding window
    	SingleOutputStreamOperator<ourTuple> dataStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaSource")
                .flatMap(new Splitter())
                .assignTimestampsAndWatermarks(
                        WatermarkStrategy.
                        <ourTuple>forBoundedOutOfOrderness(Duration.ofDays(2))
                                .withTimestampAssigner((event, timestamp) -> event.toTimestampLong())
                                .withIdleness(Duration.ofSeconds(1))
                );
    	
    	//Offset parameter is set to Time.mintues(-119) for two reasons:
    	//First, local machine time is EET, which is GMT+2, so we need the offset to be -120 min
    	//Second, if offset was -120 min, then the window would be [00:00, 23:59]
    	//we want the window to be [00:01, 00:00 (next day)], as the latest timestamp can be 23:59:00 (on motion sensor)
    	//So, we offset another minute: -120 + 1 = 119
    	
    	//SideOutputLateData is used to handle late events for sensor W1
    	SingleOutputStreamOperator<ourTuple> newStream = dataStream
                .filter(value -> !value.sensor.contains("tot"))
                .keyBy(value -> value.sensor)
                .window(TumblingEventTimeWindows.of(Time.days(1), Time.minutes(-119)))
                .sideOutputLateData(lateOutputTag)
                .aggregate(quarterAggregateFunction);
                
    	SingleOutputStreamOperator<ourTuple> totStream = dataStream
                .filter(value -> value.sensor.contains("tot"))
                .keyBy(value -> value.sensor)
                .window(SlidingEventTimeWindows.of(Time.days(2), Time.days(1), Time.minutes(-119)))
                .aggregate(dailyAggregateFunction);
        
    	DataStream<ourTuple> finalStream = newStream.union(totStream);

		KafkaSink<ourTuple> rawSink = KafkaSink.<ourTuple>builder()
				.setBootstrapServers("localhost:9092")
				.setRecordSerializer(
						KafkaRecordSerializationSchema.builder()
								.setTopic("raw")
								.setValueSerializationSchema(
										new OurTupleSerializationSchema()
								)
								.build()
				)
				.build();
		//Sink all raw data to raw topic
		dataStream.sinkTo(rawSink);

		KafkaSink<ourTuple> aggregatedSink = KafkaSink.<ourTuple>builder()
				.setBootstrapServers("localhost:9092")
				.setRecordSerializer(
						KafkaRecordSerializationSchema.builder()
								.setTopic("aggregated")
								.setValueSerializationSchema(
										new OurTupleSerializationSchema()
								)
								.build()
				)
				.build();

		KafkaSink<ourTuple> lateSink = KafkaSink.<ourTuple>builder()
				.setBootstrapServers("localhost:9092")
				.setRecordSerializer(
						KafkaRecordSerializationSchema.builder()
								.setTopic("late")
								.setValueSerializationSchema(
										new OurTupleSerializationSchema()
								)
								.build()
				)
				.build();

    	//Checking if topic is energy or water. If true calculate rest aggregator
    	//Filters out Not Applicable aggregation
    	if(jobName.contains("Sum")) {
    	    SingleOutputStreamOperator<ourTuple> restStream =  finalStream
    	    		.windowAll(TumblingEventTimeWindows.of(Time.days(1), Time.minutes(-119)))
    	    		.aggregate(restAggregateFunction);
    	    
    	    //Sink AggDay and AggDayDiff data to aggregated topic		
            finalStream
	            .filter(value -> !value.sensor.contains("NotApplicable"))
	            .sinkTo(aggregatedSink);
            System.out.println("Adding a sink done");
            
           //Sink AggRest data to aggregated topic
            restStream
	            .filter(value -> !value.sensor.contains("NotApplicable"))
	            .sinkTo(aggregatedSink);
            System.out.println("Adding rest sink done");
            
            //This is the dataStream of late rejected events
            DataStream<ourTuple> lateStream = newStream.getSideOutput(lateOutputTag);
            
            //Sink late rejected data to late topic
            lateStream.sinkTo(lateSink);
    	    
    	}
        
    	//If topic is not energy or water, do not calculate rest aggregator
    	else {
    		//Sink AggDay and AggDayMov data to aggregated topic
    		finalStream
	            .filter(value -> !value.sensor.contains("NotApplicable"))
	            .sinkTo(aggregatedSink);
            System.out.println("Adding a sink done");
            
    	}
    		
    }

    static SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy:MM:dd HH:mm");

    //Function to convert DataStream<String> to DataStream<ourTuple>
    public static class Splitter implements FlatMapFunction<String, ourTuple> {
        
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