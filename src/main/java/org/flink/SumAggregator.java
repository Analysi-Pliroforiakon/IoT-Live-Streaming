package org.flink;

import java.text.ParseException;

import org.apache.flink.api.common.functions.AggregateFunction;

public class SumAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> { 
	    	   
        @Override
        public aggregateHelper createAccumulator() {
            return new aggregateHelper();
        }

        @Override
        public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {
        	aggregateHelper.setVariant("AggDay", tuple.sensor);
            aggregateHelper.timestamp = tuple.datetime;
            aggregateHelper.count = aggregateHelper.count + 1f;
            aggregateHelper.sum = aggregateHelper.sum + tuple.value;
            return aggregateHelper;
        }

        @Override
        public ourTuple getResult(aggregateHelper aggregateHelper) {
        	ourTuple tuple = new ourTuple();
            tuple.sensor = aggregateHelper.variant;
            //Increase timestamp for water sensor, so that it is correctly aligned
            if(aggregateHelper.variant.contains("W1")) {
            	try {
    				aggregateHelper.setTimestamp();
    			} catch (ParseException e) {
    				e.printStackTrace();
    			}	
            }
            tuple.datetime = aggregateHelper.timestamp;
            //If date is too early label aggregation as not yet applicable
            //These aggregations are filtered out on DataStreamClass
            if(tuple.sensor == null || tuple.datetime != null && tuple.toTimestampLong() <= 1577829600000L) tuple.sensor = "NotApplicable";
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
