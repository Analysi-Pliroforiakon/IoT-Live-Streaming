package org.flink;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class aggregateHelper {

    public String variant;
    public String timestamp;
    public float count = 0f;
    public Float sum = 0f;

    @Override
    public String toString() {
        return "{" +
                "variant='" + variant + '\'' +
                ", count=" + count +
                ", sum=" + sum +
                '}';
    }
    
    public void setVariant(String aggreagationFunctionName, String sensor) {
    	variant = aggreagationFunctionName + '[' + sensor + ']';
    }
    
    //undoes what setVariant does
    public void stripVariant(String aggregator) {
    	variant = aggregator.substring(aggregator.indexOf("[") + 1, aggregator.indexOf("]"));
    }
    
    public void setTimestamp() throws ParseException {
    	String dt = timestamp;
    	SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    	
    	
    	Calendar c = Calendar.getInstance();
    	c.setTime(sdf.parse(dt));
    	c.add(Calendar.DATE, 1);  // number of days to add
    	dt = sdf.format(c.getTime());  // dt is now the new date
    	dt += " 00:00";
    	timestamp = dt;
    }
}
