package org.example;

/**
 * Hello world!
 *
 */

public class App 
{
    public static void main( String[] args )
    {
        kafkaFlinkReceiver StramConsumrer = new kafkaFlinkReceiver();
        String inputTopic = "temperature";
        String server = "localhost:9092";

    }
}
