package org.flink;

import org.apache.flink.api.common.functions.AggregateFunction;

public class DiffAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> {

	private static final long serialVersionUID = 1L;

		@Override
        public aggregateHelper createAccumulator() {
            return new aggregateHelper();
        }

        @Override
        public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {
        	aggregateHelper.setVariant("AggDayDiff", tuple.sensor);
            aggregateHelper.timestamp = tuple.datetime;
            //This is difference (last value - new value)
            aggregateHelper.count = tuple.value - aggregateHelper.sum;
            //This is new measurement
            aggregateHelper.sum = tuple.value;
            return aggregateHelper;
        }

        @Override
        public ourTuple getResult(aggregateHelper aggregateHelper) {
        	ourTuple tuple = new ourTuple();
            tuple.sensor = aggregateHelper.variant;
            tuple.datetime = aggregateHelper.timestamp;
            //If date is too early label aggregation as not yet applicable
            //These aggregations are filtered out on DataStreamClass
            if(tuple.sensor == null || tuple.datetime != null && tuple.toTimestampLong() <= 1577829600000L) tuple.sensor = "NotApplicable";
            //This returns differences of new and last measurement
            tuple.value = aggregateHelper.count;
            return tuple;
        }

        @Override
        public aggregateHelper merge(aggregateHelper aggregateHelper, aggregateHelper acc1) {
        	
            aggregateHelper.sum = acc1.sum;
            aggregateHelper.count = acc1.count;
            return aggregateHelper;
        }
}
