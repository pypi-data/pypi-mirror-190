import os
import pandas as pd
import logging
import snowflake.connector

from datetime import datetime
from configparser import ConfigParser
from snowflake.connector.pandas_tools import write_pandas

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def connect(connection_identifier: str):
    if os.environ.get('DE_PYTOOLS_CONFIG_PATH') is not None:
        config_path = os.path.join(os.environ.get('DE_PYTOOLS_CONFIG_PATH'), 'connection-details-snowflake.cfg')
        config = ConfigParser()
        config.read_file(open(config_path))

        # snowflake connection details
        account = config.get(connection_identifier, "account")
        warehouse = config.get(connection_identifier, "warehouse")
        database = config.get(connection_identifier, "database")
        user = config.get(connection_identifier, "user")
        password = config.get(connection_identifier, "password")
        role = config.get(connection_identifier, "role")
        conn_type = config.get(connection_identifier, "conn_type")

        if conn_type == 'browser':
            conn = connect_using_browser_auth(user, account, warehouse, database, role)
        elif conn_type == 'credentials':
            conn = connect_using_credential(user, password, account, warehouse, database, role)

        return conn

    else:
        logger.exception('Missing DE_PYTOOLS_CONFIG_PATH')


def connect_using_credential(user: str, password: str, account: str, warehouse: str, database: str, role: str):
    try:
        # Snowflake Connection
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            role=role
        )

        return conn

    except Exception as e:
        print(e)


def connect_using_browser_auth(user: str, account: str, warehouse: str, database: str, role: str):
    try:
        # Snowflake Connection
        conn = snowflake.connector.connect(
            user=user,
            account=account,
            warehouse=warehouse,
            database=database,
            role=role,
            authenticator="externalbrowser"
        )

        return conn

    except Exception as e:
        print(e)


def read_query(connection, schema: str, query: str):
    cursor = connection.cursor()
    query_schema = "USE SCHEMA {}".format(schema)
    try:
        cursor.execute(query_schema)
        cursor.execute(query)
        names = [x[0] for x in cursor.description]

        rows = cursor.fetchall()

        return pd.DataFrame(rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()


def read_val(connection, schema, query):
    cursor = connection.cursor()
    # cursor.outputtypehandler = NumberToDecimal
    query_schema = f"USE SCHEMA {schema}"
    try:
        cursor.execute(query_schema)
        cursor.execute(query)
        return cursor.fetchone()[0]
    finally:
        if cursor is not None:
            cursor.close()


def create_table(connection, schema, ddl_sql):
    cursor = connection.cursor()
    query_schema = f"USE SCHEMA {schema}"
    try:
        cursor.execute( query_schema )
        result = cursor.execute( ddl_sql )
        return result
    except Exception as e:
        print(e)
    finally:
        if cursor is not None:
            cursor.close()


def drop_table(connection, schema, table):
    cursor = connection.cursor()
    query_schema = f"USE SCHEMA {schema}"
    query_drop = f"DROP TABLE IF EXISTS {table}"
    try:
        cursor.execute( query_schema )
        cursor.execute( query_drop )
    except Exception as e:
        print(e)
    finally:
        if cursor is not None:
            cursor.close()


def truncate_table(connection, schema, table):
    cursor = connection.cursor()
    query_schema = f"USE SCHEMA {schema}"
    query = f"TRUNCATE TABLE IF EXISTS {table}"
    try:
        cursor.execute( query_schema )
        cursor.execute( query )
    finally:
        if cursor is not None:
            cursor.close()


# Function: Write pandas dataframe to a snowflake table
def write_pandas2(connection, df_to_write, schema, table, mode='append'):
    start_time = datetime.now()

    if mode == 'truncate_load':
        truncate_table(connection, schema, table)

    try:
        success, nchunks, nrows, output = write_pandas(connection, df_to_write, table, schema=schema)
        if success:
            if nrows == df_to_write.shape[0]:
                end_time = datetime.now()
                time_taken = end_time - start_time
                logger.info(f"({end_time} - {time_taken}) Successfully exported {nrows} rows in {nchunks} chunks {output[0]}")
        else:
            logger.exception("Failed export for {}".format(table))

        return [success, nchunks, nrows, output]

    except Exception as e:
        logger.exception(f"Error: {e}")


def write_file(connection, data_file, schema, table, mode='append'):
    start_time = datetime.now()

    if mode == 'truncate_load':
        truncate_table(connection, schema, table)

    try:
        put_command = f"PUT file://{data_file} @%{table}"
        copy_command = f"COPY INTO {table} " \
                       f"file_format = (type = csv FIELD_OPTIONALLY_ENCLOSED_BY = '\"' SKIP_HEADER = 1)"

        logger.info(f"put command: {put_command}")
        logger.info(f"copy command: {copy_command}")

        connection.cursor().execute(put_command)
        rows = connection.cursor().execute(copy_command)

        row = rows.fetchone()
        status, nrows_parsed, nrows_loaded = row[1], row[2], row[3]

        if status == 'LOADED':
            if nrows_parsed == nrows_loaded:
                logger.info(f"RESULT: Successfully exported {nrows_loaded} rows")
        else:
            logger.exception("RESULT: Failed")

    except Exception as e:
        print(e)

    end_time = datetime.now()
    time_taken = end_time - start_time
    logger.info(f"Start Time {start_time} | End Time {end_time} | Time taken {time_taken}")


def execute2(connection, sql):
    cursor = connection.cursor()
    try:
        result = cursor.execute(sql)
    finally:
        if cursor is not None:
            cursor.close()

    logger.info(f"{result.rowcount} rows affected")
    return result
