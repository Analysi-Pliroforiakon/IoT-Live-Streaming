package org.example;


import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;


public class main {
    public static void main(String[] args) throws Exception{

        // env
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        String[] inputTopics = {"temperature", "energy", "motion", "water"};

        // for temperature -> AVG temperature for each sensor
        KafkaFlinkReceiver temperatureKafka = new KafkaFlinkReceiver();
        temperatureKafka.myKafkaSource(new String[]{inputTopics[0]}, "localhost:9092" );

        DataStreamClass temperatureDataStream = new DataStreamClass();

        temperatureDataStream.startFlinking(env, new AverageAggregator(), temperatureKafka.getKafkaSource(), "Average Temperature", 10);

        // for energy topic -> Sum wh for each sensor
        KafkaFlinkReceiver energyKafka = new KafkaFlinkReceiver( );
        energyKafka.myKafkaSource(new String[]{inputTopics[1]}, "localhost:9092" );

        DataStreamClass energyDataStream = new DataStreamClass();

        energyDataStream.startFlinking(env, new SumAggregator(), energyKafka.getKafkaSource(), "Sum Energy", 10);


//        water -> Sum water for each sensor
        KafkaFlinkReceiver waterKafka = new KafkaFlinkReceiver( );
        waterKafka.myKafkaSource(new String[]{inputTopics[3]}, "localhost:9092" );

        DataStreamClass waterDataStream = new DataStreamClass();

        waterDataStream.startFlinking(env, new SumAggregator(), waterKafka.getKafkaSource(), "Sum Water", 10);
        env.execute("Flink Streaming Java API Skeleton");

    }
}
