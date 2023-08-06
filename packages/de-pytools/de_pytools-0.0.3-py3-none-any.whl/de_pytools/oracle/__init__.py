import configparser
import cx_Oracle
import csv
import decimal
import logging
import pandas as pd
import os

from datetime import datetime

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def connect(identifier):
    if os.environ.get('DE_PYTOOLS_CONFIG_PATH') is not None:
        config_path = os.path.join(os.environ.get('DE_PYTOOLS_CONFIG_PATH'), 'connection-details-oracle.cfg')
        config = configparser.ConfigParser()
        config.read_file(open(config_path))

        tns_name = config.get(identifier, "tnsname")
        user = config.get(identifier, "user")
        password = config.get(identifier, "password")
        conn_type = config.get(identifier, "conn_type")

        if conn_type == 'TNS':
            conn = ora_connect_tns(user, password, tns_name)
        return conn

    else:
        logger.exception('Missing DE_PYTOOLS_CONFIG_PATH')


def connect_using_tns(user, password, tns_name):
    conn = cx_Oracle.connect(user, password, tns_name, encoding="UTF-16")
    logger.info(f'Connected to Oracle DB. connection version {conn.version}')
    return conn


def disconnect(conn_name):
    # Closing the connection
    conn_name.close()


def read_val(connection, query):
    cursor = connection.cursor()
    # cursor.outputtypehandler = NumberToDecimal

    try:
        logger.info('Executing SQL query: {}'.format(query))
        cursor.execute(query)
        return cursor.fetchone()[0]
    finally:
        if cursor is not None:
            cursor.close()


def NumberToDecimal(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.NUMBER:
        return cursor.var(decimal.Decimal, arraysize=cursor.arraysize)


def read_query(connection, query):
    cursor = connection.cursor()
    # cursor.outputtypehandler = NumberToDecimal

    try:
        logger.info('Executing SQL query: {}'.format(query))
        cursor.execute(query)

        names = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()


def read_query_to_csv(connection, query, max_rows, total_count, output_file):
    start_time = datetime.now()
    logger.info(f'Started at {start_time}')
    cursor = connection.cursor()
    exported_count = 0

    try:
        logger.info(f'Executing SQL query: {query}')
        cursor.execute(query)
        names = [x[0] for x in cursor.description]

        with open(output_file, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow(names)  # heading row

            while True:
                rows = cursor.fetchmany(max_rows)
                if not rows:
                    break

                writer.writerows(rows)

                exported_count += len(rows)
                exported_pctg = round(exported_count*100/total_count,2)
                logger.info(f'Exported {exported_count} / {total_count} rows. {exported_pctg}% complete')

    finally:
        if cursor is not None:
            cursor.close()


def truncate_table(connection, tbl):
    cursor = connection.cursor()
    query = f"TRUNCATE TABLE {tbl}"
    try:
        cursor.execute(query)
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()


def execute_sql(connection, sql):
    cursor = connection.cursor()
    try:
        logger.info(f"Executing SQL query: {sql}")
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        logger.exception(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()


def insert_df(connection, insert_sql, df_to_write):
    cursor = connection.cursor()

    try:
        cursor.prepare(insert_sql)
        cursor.executemany(None, df_to_write.values.tolist())
        connection.commit()
    except cx_Oracle.Error as e:
        logger.exception(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()


def obj_dependency(conn, schema, obj, obj_type):
    if obj_type == 'TABLE':
        dep_df = ora_query_to_df(conn, sql_queries_oracle.sql_tbl_dependencies.format(schema, obj))

    elif obj_type in ['VIEW', 'MATERIALIZED VIEW']:
        dep_df = ora_query_to_df(conn, sql_queries_oracle.sql_view_dependencies.format(schema, obj))

    return dep_df


def addLevel(depDf):
    level = 1
    processed = []
    all_objs = list(set(list(depDf['PARENT'].dropna()) + list(depDf['CHILD'])))
    all_objs.sort()

    all_rows = []

    while len(all_objs) > 0:
        processed_obj_level = []

        for id, obj in enumerate(all_objs, start=1):
            obj_parents = list(set(depDf[depDf.CHILD == obj]['PARENT']))
            logger.info(f"Level: {level} | Object#: {id} | Object: {obj}")

            row = {}
            if len(obj_parents) == 0 or all(x in processed for x in obj_parents):
                row['CHILD'] = obj
                row['PARENT'] = obj_parents
                row['LEVEL'] = level

                all_rows.append(row)
                processed_obj_level.append(obj)

        level += 1
        processed += processed_obj_level
        all_objs = [x for x in all_objs if x not in processed]

    return pd.DataFrame(all_rows)