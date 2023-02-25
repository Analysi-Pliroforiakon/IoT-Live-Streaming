package org.flink;

import java.text.ParseException;

import org.apache.flink.api.common.functions.AggregateFunction;

public class MovCountAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> {

        @Override
        public aggregateHelper createAccumulator() {
            return new aggregateHelper();
        }

        @Override
        public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {
        	aggregateHelper.setVariant("AggDayMov", tuple.sensor);
            aggregateHelper.timestamp = tuple.datetime;
            aggregateHelper.count = aggregateHelper.count + 1f;
            aggregateHelper.sum = aggregateHelper.sum + tuple.value;
            return aggregateHelper;
        }

        @Override
        public ourTuple getResult(aggregateHelper aggregateHelper) {
        	ourTuple tuple = new ourTuple();
            tuple.sensor = aggregateHelper.variant;
            try {
				aggregateHelper.setTimestamp();
			} catch (ParseException e) {
				e.printStackTrace();
			}
            tuple.datetime = aggregateHelper.timestamp;
            tuple.value = aggregateHelper.sum;
            return tuple;
        }

        @Override
        public aggregateHelper merge(aggregateHelper aggregateHelper, aggregateHelper acc1) {
            aggregateHelper.sum = aggregateHelper.sum + acc1.sum;
            aggregateHelper.count = aggregateHelper.count + acc1.count;
            return aggregateHelper;
        }
}
