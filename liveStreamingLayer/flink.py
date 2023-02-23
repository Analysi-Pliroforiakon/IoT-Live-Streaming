import os

# import pyflink

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
import hbase 
# from pyflink.common import Row
# from pyflink.table import (EnvironmentSettings, TableEnvironment, TableDescriptor, Schema,
#                            DataTypes, FormatDescriptor)
# from pyflink.table.expressions import lit, col
# from pyflink.table.udf import udtf
FILE = '/mnt/c/Users/Nikolas/Downloads/flink-sql-connector-kafka-1.16.0.jar'


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .build()

                    #   .use_blink_planner()\
    # create table environment
    tbl_env = StreamTableEnvironment.create(stream_execution_environment=env,
                                            environment_settings=settings)

    # add kafka connector dependency
    kafka_jar = os.path.join(FILE)

    tbl_env.get_config()\
            .get_configuration()\
            .set_string("pipeline.jars", "file://{}".format(kafka_jar))
    print('Kafka Connector JAR added to pipeline')
    print('tbl_env: ', tbl_env)
    #######################################################################
    # Create Kafka Source Table with DDL
    #######################################################################
    src_ddl = """
        CREATE TABLE temperatures (
            date_time TIMESTAMP,
            temp DOUBLE
        ) WITH (
            'connector' = 'temperature',
            'topic' = 'temperatures',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'foo',
            'format' = 'json'
        )
    """

    tbl_env.execute_sql(src_ddl)

    # create and initiate loading of source Table
    tbl = tbl_env.from_path('temperatures')

    print('\nSource Schema')
    tbl.print_schema()

    #####################################################################
    # Define Tumbling Window Aggregate Calculation (Seller Sales Per Minute)
    #####################################################################
    # sql = """
    #     SELECT
    #       seller_id,
    #       TUMBLE_END(proctime, INTERVAL '60' SECONDS) AS window_end,
    #       SUM(amount_usd) * 0.85 AS window_sales
    #     FROM sales_usd
    #     GROUP BY
    #       TUMBLE(proctime, INTERVAL '60' SECONDS),
    #       seller_id
    # """
    # connect to a hbase table
    # sql = """
    #     SELECT
    #         date_time,
    #         temp
    #     FROM temperatures
    # """
    # # create and initiate loading of sink Table
    # temperatures_tbl = tbl_env.sql_query(sql)

    # print('\nProcess Sink Schema')
    # temperatures_tbl.print_schema()

    ###############################################################
    # Create Kafka Sink Table
    ###############################################################
    # sink_ddl = """
    #     CREATE TABLE sales_euros (
    #         seller_id VARCHAR,
    #         window_end TIMESTAMP(3),
    #         window_sales DOUBLE
    #     ) WITH (
    #         'connector' = 'kafka',
    #         'topic' = 'sales-euros',
    #         'properties.bootstrap.servers' = 'localhost:9092',
    #         'format' = 'json'
    #     )
    # """
    # tbl_env.execute_sql(sink_ddl)

    # write time windowed aggregations to sink table
    # revenue_tbl.execute_insert('sales_euros').wait()

    # tbl_env.execute('windowed-sales-euros')


    # ###############################################################
    # # Create HBase Sink Table
    # ###############################################################
    hbase_sink_ddl = """
        CREATE TABLE htable (
            rowkey INT,
            family1 ROW<q1 INT>,
            family2 ROW<q2 STRING, q3 BIGINT>,
            family3 ROW<q4 DOUBLE, q5 BOOLEAN, q6 STRING>,
            PRIMARY KEY (rowkey) NOT ENFORCED 
        ) WITH (
            'connector' = 'hbase-2.2',
            'table-name' = 'test',
            'zookeeper.quorum' = 'localhost:2181',
            """
    hbase_temp = tbl_env.execute_sql(hbase_sink_ddl)
    print('HBase Sink Table Created')
    print('hbase_temp: ', hbase_temp.print_schema())


if __name__ == '__main__':
    main()