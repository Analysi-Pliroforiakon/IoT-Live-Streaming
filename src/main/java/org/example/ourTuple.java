package org.example;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

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
        return sensor + " | " + datetime + " | " + value;
    }
//    get sensor

    public String getSensor() {
        return sensor;
    }
    
    public Long toTimestampLong() {
    	try {
        	
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");
            dateFormat.setTimeZone(TimeZone.getTimeZone("EET"));
            //System.out.println(this.datetime);
            //System.out.println(event.datetime);
            Date parsedDatetime = dateFormat.parse(this.datetime);
            //System.out.println(parsedDatetime.getTime());
            return parsedDatetime.getTime();
        } catch (Exception e) {
            // handle exception
            return 0L;
        }
    	//return Long.parseLong(datetime);
    }
}
