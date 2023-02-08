package org.example;

import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;

public class AverageAggregator implements AggregateFunction<ourTuple, AverageAggregator.MyAverage, Tuple2<AverageAggregator.MyAverage, Float>> {

    public static class MyAverage {

        public String variant;
        public float count = 0f;
        public Float sum = 0f;

        @Override
        public String toString() {
            return "MyAverage{" +
                    "variant='" + variant + '\'' +
                    ", count=" + count +
                    ", sum=" + sum +
                    '}';
        }
    }


    @Override
    public MyAverage createAccumulator() {
        return new MyAverage();
    }

    @Override
    public MyAverage add(ourTuple tuple, MyAverage myAverage) {

        myAverage.variant = tuple.sensor;
        myAverage.count = myAverage.count + 1f;
        myAverage.sum = myAverage.sum + tuple.value;
        return myAverage;
    }

    @Override
    public Tuple2<MyAverage, Float> getResult(MyAverage myAverage) {
        return new Tuple2<>(myAverage,(myAverage.sum/ myAverage.count));
    }

    @Override
    public MyAverage merge(MyAverage myAverage, MyAverage acc1) {
        myAverage.sum = myAverage.sum + acc1.sum;
        myAverage.count = myAverage.count + acc1.count;
        return myAverage;
    }
}
