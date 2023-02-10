package org.example;

import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;

public class AverageAggregator implements AggregateFunction<ourTuple, aggregateHelper, Tuple2<aggregateHelper, Float>> {

    @Override
    public aggregateHelper createAccumulator() {
        return new aggregateHelper();
    }

    @Override
    public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {

        aggregateHelper.variant = tuple.sensor;
        aggregateHelper.count = aggregateHelper.count + 1f;
        aggregateHelper.sum = aggregateHelper.sum + tuple.value;
        return aggregateHelper;
    }

    @Override
    public Tuple2<aggregateHelper, Float> getResult(aggregateHelper aggregateHelper) {
        return new Tuple2<>(aggregateHelper, (aggregateHelper.sum / aggregateHelper.count));
    }

    @Override
    public aggregateHelper merge(aggregateHelper aggregateHelper, aggregateHelper acc1) {
        aggregateHelper.sum = aggregateHelper.sum + acc1.sum;
        aggregateHelper.count = aggregateHelper.count + acc1.count;
        return aggregateHelper;
    }


}
