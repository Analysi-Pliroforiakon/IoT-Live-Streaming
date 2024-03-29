# HBase

## Intrucitons for manual installation

General can be found [here](https://towardsdatascience.com/setting-up-a-standalone-hbase-local-instance-and-connect-to-it-with-python-happybase-9751c9fe6941)
Basicly there are the steps.
Proceed with your own risk.
Please make sure the _apt-get_ is updated.

1. You should install JDK-8

```
sudo apt-get -y install openjdk-8-jdk-headless
```

2. Download the hbase-version you want. from [here](https://www.apache.org/dyn/closer.lua/hbase/)

```
 wget https://archive.apache.org/dist/hbase/2.2.3/hbase-2.2.3-bin.tar.gz
```

3. Unzip the hbase-files.

```
 tar xzvf hbase-2.2.3-bin.tar.gz.1
```

4. Edit the hbase-2.2.3/conf/hbase-env.sh file

```
vi hbase-2.2.3/conf/hbase-env.sh
```

and then add the JAVA_HOME

```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```

5. start the thrift server.

```
 ./bin/hbase-daemon.sh start thrift
```

6. Finaly start hbase.

```
./bin/start-hbase.sh
```

## WSL and Windows

We do NOT recommend to use WSL for HBase. It is not stable and it is not easy to install.

## Late rejected.

Late rejected data , is data that is rejected because they are received after the aggregation time.
The assignment says that we should store late data and in a

# Flow

<p>
10 days Late events -> live data & late data table
<p>
2 days late events -> live data & aggregated
<p>
normal events -> live & aggregated tables
 
---

# Tables

## Name

---

There are 3 tables.

1. live data table
2. aggregated data table
3. late data table

## Name & Use case.

---

| Table Name     | Use Case                        | Row Key                  | Sensor                                                         | Value                        | Datetime         |
| -------------- | ------------------------------- | ------------------------ | -------------------------------------------------------------- | ---------------------------- | ---------------- |
| rawData        | Store the data, late and normal | {DateTime}+{SensorValue} | The sensor name, eg TH1,MiAc2                                  | The value of the metric      | YYYY-MM-DD HH:mm |
| aggregatedData | Store only the aggragated data. | {DateTime}+{Aggregation} | Aggregatio name you may see the live streaming layer for that. | The value of the aggragation | YYYY-MM-DD HH:mm |
| lateData       | Store only the late data.       | {DateTime}+{SensorValue} | The sensor name, eg TH1,MiAc2                                  | The value of the metric      | YYYY-MM-DD HH:mm |
