package org.example;

public class aggregateHelper {

    public String variant;
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
}
