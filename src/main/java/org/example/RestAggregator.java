package org.example;

import org.apache.flink.api.common.functions.AggregateFunction;

public class RestAggregator implements AggregateFunction<ourTuple, aggregateHelper, ourTuple> {

        /**
	 * 
	 */
	private static final long serialVersionUID = 1L;

		@Override
        public aggregateHelper createAccumulator() {
            return new aggregateHelper();
        }

        @Override
        public aggregateHelper add(ourTuple tuple, aggregateHelper aggregateHelper) {
        	//If input tuple is total aggregator, use its name and timestamp and add its value
        	if(tuple.sensor.contains("Diff")) {
        		//This is used to set aggregator name
        		aggregateHelper.stripVariant(tuple.sensor);
        		aggregateHelper.setVariant("AggDayRest", aggregateHelper.variant);
        		
        		aggregateHelper.timestamp = tuple.datetime;
        		aggregateHelper.sum += tuple.value;
        	}
        	//If input tuple is not total aggregator, subtract its value
        	else {
        		aggregateHelper.sum -= tuple.value;
        	}
            return aggregateHelper;
        }

        @Override
        public ourTuple getResult(aggregateHelper aggregateHelper) {
        	ourTuple tuple = new ourTuple();
            tuple.sensor = aggregateHelper.variant;
            tuple.datetime = aggregateHelper.timestamp;
            //This returns difference between total sensor and sum of the others
            tuple.value = aggregateHelper.sum;
            return tuple;
        }

        @Override
        public aggregateHelper merge(aggregateHelper aggregateHelper, aggregateHelper acc1) {
        	
            aggregateHelper.sum += acc1.sum;
            aggregateHelper.count += acc1.count;
            return aggregateHelper;
        }
        

}
