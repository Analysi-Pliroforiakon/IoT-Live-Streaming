package org.example;

public class ourTuple {
    public String sensor;
    public String datetime;
    public Float value;

    @Override
    public String toString() {
        return "Sensor: " + sensor+ " datetime: "+datetime + " value: "+value;
    }
//    get sensor

    public String getSensor() {
        return sensor;
    }

}
