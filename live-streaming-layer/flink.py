import os

FILE = 'C:/Users/Nikolas\Downloads/flink-sql-connector-kafka-1.16.0.jar'

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .use_blink_planner()\
                      .build()

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
            date_time TIMESTAMP(3),
            temp FLOAT,
        ) WITH (
            'connector' = 'temperature',
            'topic' = 'sales-usd',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'foo',
            'format' = 'json'
        )
    """

    tbl_env.execute_sql(src_ddl)

    # create and initiate loading of source Table
    tbl = tbl_env.from_path('sales_usd')

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
    # revenue_tbl = tbl_env.sql_query(sql)

    # print('\nProcess Sink Schema')
    # revenue_tbl.print_schema()

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


if __name__ == '__main__':
    main()