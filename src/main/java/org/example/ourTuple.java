package org.example;

import java.io.Serializable;

public class ourTuple implements Serializable{
    /**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public String sensor;
    public String datetime;
    public Float value;

    @Override
    public String toString() {
        return "Sensor: " + sensor + " datetime: " + datetime + " value: " + value + "";
    }
//    get sensor

    public String getSensor() {
        return sensor;
    }

}
