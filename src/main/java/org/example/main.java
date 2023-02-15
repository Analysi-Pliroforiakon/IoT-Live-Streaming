package org.example;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;


public class main {
    public static void main(String[] args) throws Exception{
        
    	//This is to fix an error that occurs when running many streams at the same time
    	Configuration cfg = new Configuration();
    	int defaultLocalParallelism = Runtime.getRuntime().availableProcessors();
    	cfg.setString("taskmanager.memory.network.max", "1gb");
    	StreamExecutionEnvironment env = StreamExecutionEnvironment.createLocalEnvironment(defaultLocalParallelism, cfg);
    	
        // env
        //StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        String[] inputTopics = {"temperature", "energy", "motion", "water"};
        
        // for temperature -> AVG temperature for each sensor
        KafkaFlinkReceiver temperatureKafka = new KafkaFlinkReceiver();
        temperatureKafka.myKafkaSource(new String[]{inputTopics[0]}, "localhost:9092" );

        DataStreamClass temperatureDataStream = new DataStreamClass();

        temperatureDataStream.startFlinking(env, new AverageAggregator(), new DiffAggregator(), new RestAggregator(), temperatureKafka.getKafkaSource(), "Average Temperature", 96);
        // for energy topic -> Sum wh for each sensor
        KafkaFlinkReceiver energyKafka = new KafkaFlinkReceiver( );
        energyKafka.myKafkaSource(new String[]{inputTopics[1]}, "localhost:9092" );

        DataStreamClass energyDataStream = new DataStreamClass();

        energyDataStream.startFlinking(env, new SumAggregator(), new DiffAggregator(), new RestAggregator(), energyKafka.getKafkaSource(), "Sum Energy", 96);


//        water -> Sum water for each sensor
        KafkaFlinkReceiver waterKafka = new KafkaFlinkReceiver( );
        waterKafka.myKafkaSource(new String[]{inputTopics[3]}, "localhost:9092" );

        DataStreamClass waterDataStream = new DataStreamClass();

        waterDataStream.startFlinking(env, new SumAggregator(), new DiffAggregator(), new RestAggregator(), waterKafka.getKafkaSource(), "Sum Water", 96);
        
        //motion -> Count motion detections per day
        KafkaFlinkReceiver motionKafka = new KafkaFlinkReceiver();
        motionKafka.myKafkaSource(new String[]{inputTopics[2]}, "localhost:9092");
        
        DataStreamClass motionDataStream = new DataStreamClass();
        
        motionDataStream.startFlinking(env, new MovCountAggregator(), new DiffAggregator(), new RestAggregator(), motionKafka.getKafkaSource(), "Count Motion", 96);
        
        env.execute("Flink Streaming Java API Skeleton");

    }
}
