package org.flink;


import org.apache.flink.connector.hbase.sink.HBaseMutationConverter;
import org.apache.flink.connector.hbase.sink.HBaseSinkFunction;
import org.apache.flink.connector.hbase.util.HBaseTableSchema;
import org.apache.flink.connector.hbase.util.HBaseTypeUtils;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.Mutation;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;
import  org.apache.flink.types.*;

import java.io.IOException;

public class MyHbaseSink {
    public Configuration config;
    public
    HBaseSinkFunction<org.flink.ourTuple> sinkFunction;
    public void initialize(String quorum, String port, String table) {
       Configuration config = HBaseConfiguration.create();
       config.set("hbase.zookeeper.quorum", quorum);
       config.set("hbase.zookeeper.property.clientPort", port);
       this.config = config;
//     create a hbase sink function
        HBaseSinkFunction<ourTuple> hbaseSinkFunction = new HBaseSinkFunction<ourTuple>(table, config, new HBaseMutationConverter<ourTuple>() {
            @Override
            public void open() {


//                System.out.println("open hbase sink function");
//                HBaseTableSchema tableSchema = new HBaseTableSchema();
//                tableSchema.addColumn("cf", "sensor", HBaseTypeUtil);
//                tableSchema.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("datetime"));
//                tableSchema.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("value"));


            }

            @Override
            public Mutation convertToMutation(ourTuple ourTuple) {
                Put put = new Put(Bytes.toBytes(ourTuple.sensor + ourTuple.datetime));
                put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("sensor"), ourTuple.sensor.getBytes());
                put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("datetime"), ourTuple.datetime.getBytes());
                put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("value"), ourTuple.value.toString().getBytes());
                return put;
            }
        },
                1000,
                1000,
                1000);
            this.sinkFunction = hbaseSinkFunction;

        System.out.println("Hbase sink initialized");
    }



}
