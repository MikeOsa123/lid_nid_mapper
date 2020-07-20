import snowflake.connector
import os
import pandas as pd

class SnowflakeApi:
    
    """
    PURPOSE:
        This is the Base/Parent class for programs that use the Snowflake
        Connector for Python.
        This class is intended primarily for:
            * Running Queries
            * Creating tables
    """

    # set environment variables as attributes
    def __init__(self, **kwargs):
        self.user = os.getenv('SNOWSQL_USER', kwargs["user"])
        self.password = os.getenv('SNOWSQL_PWD', kwargs["password"])
        self.account = os.getenv('SNOWSQL_ACCOUNT', kwargs["account"])
        self.warehouse = os.getenv('WAREHOUSE', kwargs["warehouse"])
        self.database = os.getenv('SNOWSQL_DATABASE', kwargs["database"])
        self.schema = os.getenv('SCHEMA', kwargs["schema"])

    def conn(self):
        # create method that creates a snowflake connection
        print("\nConnection being made...")
        return snowflake.connector.connect(
            user = self.user,
            password = self.password,
            account = self.account,
            warehouse = self.warehouse,
            database = self.database,
            schema = self.schema
            )

    def return_nitems(self, query, no_rows):
        self.cur = self.conn().cursor()
        try:
            results = self.cur.execute(query).fetchmany(no_rows)
            print("\nConnection established printing results...")
            print("\n", results)
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            self.cur.close()

    def return_all(self, query):
        self.cur = self.conn().cursor()
        try:
            results = self.cur.execute(query).fetchall()
            print("\nConnection established printing results...")
            return results
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            self.cur.close()

    def get_columns(self, table_name):
        '''
        method that returns a list of columns in the table provided as a parameter
        '''
        self.cur = self.conn().cursor()
        try:
            self.cur.execute(""" select * from {table}""".format(table=table_name))
            return [col[0] for col in self.cur.description]
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            self.cur.close()

    def create_table(self, table_name, column_data):
        '''
        method that creates a table
        '''
        self.cur = self.conn().cursor()
        try:
            self.cur.execute("""CREATE OR REPLACE TABLE {table_name}({column_data})""".format(table_name=table_name, column_data=column_data))
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            # print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
            print(e)
        finally:
            self.cur.close()

    def insert_values(self, table_data, values):
        '''
        method that inserts values into the table provided in the argument above
        '''
        self.cur = self.conn().cursor()
        self.table_name = table_data[0]
        self.columns = table_data[1]
        self.values = values
        self.insert_query = 'insert into ' + self.table_name + ' (' + ','.join(self.columns) + ') VALUES (' + ','.join(['%s'] * len(self.values))+ ')'
        try:
            self.cur.execute(self.insert_query, values)
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            print(e)
            # print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            self.cur.close()

    def get_dataframe(self, query):
        '''
        return dataframe of query results
        '''
        self.cur = self.conn().cursor()
        try:
            self.cur.execute(query)
            print("\nConnection has been established.... fetching data")
            df = self.cur.fetch_pandas_all()
            print("\nDataframe created....")
            return df
        except snowflake.connector.errors.ProgrammingError as e:
            # custom error message that goes into detail
            print(e)
            # print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        finally:
            self.cur.close()



    