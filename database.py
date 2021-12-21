"""Database connection"""
from os import getenv
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_connection_string():
    """Connects to database

    Raises:
        KeyError: Missing .env variables

    Returns:
        str: Postgres link
    """
    user_name = getenv("MY_PSQL_USER")
    password = getenv("MY_PSQL_PASSWORD")
    host = getenv("MY_PSQL_HOST")
    database_name = getenv("MY_PSQL_DBNAME")

    if user_name and password and host and database_name:
        return f"postgresql://{user_name}:{password}@{host}/{database_name}"

    raise KeyError("Some necessary environment variable(s) are not defined")


def open_database():
    """Connects to database

    Raises:
        exception: Database connection error

    Returns:
        connection: Database connection
    """
    try:
        connection_string = get_connection_string()
        db_connection = connect(connection_string)
        db_connection.autocommit = True
        return db_connection

    except DatabaseError as exception:
        raise exception


def connection_handler(function):
    """Decorator to insert cursor into db query function

    Args:
        function: Query runner function
    """

    def wrapper(*args, **kwargs):
        db_connection = open_database()
        dict_cur = db_connection.cursor(cursor_factory=RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        db_connection.close()
        return ret_value

    return wrapper


@connection_handler
def run_query(cursor, query, query_vars={}, single=False):
    """Runs Postgres query

    Args:
        cursor: Injected DB cursor
        query (str): Query string; must use %(name)s for variables
        query_vars (dict, optional): Dict with {"name": value} pairs. Defaults to {}.
        single (bool, optional): Returns single dictionary?. Defaults to False.

    Returns:
        (dict || list[dict]): DB query results
    """
    cursor.execute(query, query_vars)
    if single:
        return cursor.fetchone()
    return cursor.fetchall()
