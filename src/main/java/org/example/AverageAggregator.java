package org.example;

import org.apache.flink.api.common.functions.AggregateFunction;


public class AverageAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> {

    @Override
    public aggregateHelper createAccumulator() {
        return new aggregateHelper();
    }

    
    @Override
    public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {

        aggregateHelper.variant = tuple.sensor;
        aggregateHelper.timestamp = tuple.datetime;
        aggregateHelper.count = aggregateHelper.count + 1f;
        aggregateHelper.sum = aggregateHelper.sum + tuple.value;
        return aggregateHelper;
    }


    @Override
    public ourTuple getResult(aggregateHelper aggregateHelper) {
    	ourTuple tuple = new ourTuple();
        tuple.sensor = aggregateHelper.variant;
        tuple.datetime = aggregateHelper.timestamp;
        tuple.value = (aggregateHelper.sum / aggregateHelper.count);
        return tuple;
    }
    

    @Override
    public aggregateHelper merge(aggregateHelper aggregateHelper, aggregateHelper acc1) {
        aggregateHelper.sum = aggregateHelper.sum + acc1.sum;
        aggregateHelper.count = aggregateHelper.count + acc1.count;
        return aggregateHelper;
    }


}

