package org.example;

import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.java.tuple.Tuple2;

public class TupleSerializationSchema implements SerializationSchema<Tuple2<aggregateHelper, Float>> {

    @Override
    public byte[] serialize(Tuple2<aggregateHelper, Float> element) {
        return (element.f0.toString() + "," + element.f1).getBytes();
    }
}