package org.flink;

import org.apache.flink.api.common.serialization.SerializationSchema;

public class OurTupleSerializationSchema implements SerializationSchema<ourTuple> {

	private static final long serialVersionUID = 1L;

    @Override
    public byte[] serialize(ourTuple element) {
        return (element.toString()).getBytes();
    }
}