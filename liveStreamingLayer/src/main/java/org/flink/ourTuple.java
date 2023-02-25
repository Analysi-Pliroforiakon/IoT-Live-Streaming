package org.flink;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

public class ourTuple implements Serializable{
  
	private static final long serialVersionUID = 1L;
	public String sensor;
    public String datetime;
    public Float value;

    @Override
    public String toString() {
        return sensor + " | " + datetime + " | " + value;
    }
//    get sensor
    public String getSensor() {
        return sensor;
    }
    
    public Long toTimestampLong() {
    	try {
        	
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            //This is because our machine is using Eastern European Time
            dateFormat.setTimeZone(TimeZone.getTimeZone("EET"));
            Date parsedDatetime = dateFormat.parse(this.datetime);
            return parsedDatetime.getTime();
        } catch (Exception e) {
            // handle exception
            return 0L;
        }
    	
    }
}
