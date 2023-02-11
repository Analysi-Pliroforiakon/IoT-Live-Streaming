package org.example;

import org.apache.flink.api.common.functions.AggregateFunction;

public class DiffAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> {

        @Override
        public aggregateHelper createAccumulator() {
            return new aggregateHelper();
        }

        @Override
        public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {

            aggregateHelper.variant = tuple.sensor;
            aggregateHelper.timestamp = tuple.datetime;
            //This is difference (last value - new value)
//            System.out.println("Previous value: " +  aggregateHelper.sum);
            aggregateHelper.count = tuple.value - aggregateHelper.sum;
//            System.out.println("Diff: " + aggregateHelper.count);
            //This is new measurement
            aggregateHelper.sum = tuple.value;
//            System.out.println(aggregateHelper.sum);
            return aggregateHelper;
        }

        @Override
        public ourTuple getResult(aggregateHelper aggregateHelper) {
        	ourTuple tuple = new ourTuple();
            tuple.sensor = aggregateHelper.variant;
            tuple.datetime = aggregateHelper.timestamp;
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
        
//        public void reset(aggregateHelper acc1) {
//        	acc1.sum = 0f;
//        	acc1.count = 0;
//        }

}
