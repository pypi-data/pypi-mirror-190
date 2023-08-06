import logging
from enum import Enum, unique
from typing import Any, Dict, List, Optional

import boto3
import pandas as pd
import psycopg2
from awswrangler import _databases as _db_utils
from awswrangler import exceptions
from awswrangler._config import apply_configs
from awswrangler._databases import ConnectionAttributes, get_connection_attributes
from psycopg2 import _psycopg

logger = None


def get_logger():
    global logger

    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        logger_handler.setFormatter(formatter)

        logger.addHandler(logger_handler)

    return logger


def convert_value_to_native_python_type(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "to_pydatetime"):
        return value.to_pydatetime()

    return value


@unique
class SSLMode(str, Enum):
    DISABLE = "disable"
    ALLOW = "allow"
    PREFER = "prefer"
    REQUIRE = "require"
    VERIFY_CA = "verify-ca"
    VERIFY_FULL = "verify-full"


def connect(
    connection: Optional[str] = None,
    secret_id: Optional[str] = None,
    catalog_id: Optional[str] = None,
    dbname: Optional[str] = None,
    boto3_session: Optional[boto3.Session] = None,
    sslmode: Optional[SSLMode] = None,
    connect_timeout: Optional[int] = None,
    keepalives: int = 1,
) -> _psycopg.connection:
    """Return a psycopg2 connection from a Glue Catalog Connection.

    https://github.com/psycopg/psycopg2

    Note
    ----
    You MUST pass a `connection` OR `secret_id`.
    Here is an example of the secret structure in Secrets Manager:
    {
    "host":"postgresql-instance-wrangler.dr8vkeyrb9m1.us-east-1.rds.amazonaws.com",
    "username":"test",
    "password":"test",
    "engine":"postgresql",
    "port":"3306",
    "dbname": "mydb" # Optional
    }

    Parameters
    ----------
    connection : Optional[str]
        Glue Catalog Connection name.
    secret_id: Optional[str]:
        Specifies the secret containing the connection details that you want to retrieve.
        You can specify either the Amazon Resource Name (ARN) or the friendly name of the secret.
    catalog_id : str, optional
        The ID of the Data Catalog.
        If none is provided, the AWS account ID is used by default.
    dbname: Optional[str]
        Optional database name to overwrite the stored one.
    boto3_session : boto3.Session(), optional
        Boto3 Session. The default boto3 session will be used if boto3_session receive None.
    sslmode: Optional[SSLMode]
        This option determines whether or with what priority
        a secure SSL TCP/IP connection will be negotiated with the server.
        This parameter is forwarded to psycopg2.
       https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS
    connect_timeout: Optional[int]
        This is the time in seconds before the connection to the server will time out.
        The default is None which means no timeout.
        This parameter is forwarded to psycopg2.
        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS
    keepalives: int
        If 1 then use TCP keepalive. The default is 1.
        This parameter is forwarded to psycopg2.
        https://github.com/psycopg/psycopg2

    Returns
    -------
    psycopg2.connection
        psycopg2 connection

    Examples
    --------
    >>> con = connect("MY_GLUE_CONNECTION")
    >>> with con.cursor() as cursor:
    >>>     cursor.execute("SELECT 1")
    >>>     print(cursor.fetchall())
    >>> con.close()

    """
    attrs: ConnectionAttributes = get_connection_attributes(
        connection=connection,
        secret_id=secret_id,
        catalog_id=catalog_id,
        dbname=dbname,
        boto3_session=boto3_session,
    )
    if attrs.kind not in ("postgresql", "postgres"):
        raise exceptions.InvalidDatabaseType(
            f"Invalid connection type ({attrs.kind}. It must be a postgresql connection.)"
        )

    return psycopg2.connect(
        user=attrs.user,
        database=attrs.database,
        password=attrs.password,
        port=attrs.port,
        host=attrs.host,
        sslmode=sslmode,
        connect_timeout=connect_timeout,
        keepalives=keepalives,
    )


@apply_configs
def upsert(
    *,
    df: pd.DataFrame,
    cursor: _psycopg.cursor,
    table: str,
    schema: str,
    upsert_conflict_columns: Optional[List[str]] = None,
    chunksize: int = 200,
) -> None:
    """Write records stored in a DataFrame into PostgreSQL."""
    if df.empty is True:
        return

    if not upsert_conflict_columns:
        raise exceptions.InvalidArgumentValue("<upsert_conflict_columns> needs to be set when using upsert mode.")

    column_placeholders: str = ", ".join(["%s"] * len(df.columns))
    insertion_columns = f"({', '.join(df.columns)})"

    upsert_columns = ", ".join(df.columns.map(lambda column: f"{column}=EXCLUDED.{column}"))
    conflict_columns = ", ".join(upsert_conflict_columns)  # type: ignore
    upsert_str = f" ON CONFLICT ({conflict_columns}) DO UPDATE SET {upsert_columns}"

    placeholder_parameter_pair_generator = _db_utils.generate_placeholder_parameter_pairs(
        df=df, column_placeholders=column_placeholders, chunksize=chunksize
    )

    for placeholders, parameters in placeholder_parameter_pair_generator:
        sql: str = f"""
        INSERT INTO "{schema}"."{table}" {insertion_columns}
        VALUES {placeholders}{upsert_str};
        """
        get_logger().debug("sql: %s", sql)
        cursor.executemany(sql, (parameters,))

    get_logger().info("Upsert %s rows in %s.%s", cursor.rowcount, schema, table)


@apply_configs
def update(
    *,
    df: pd.DataFrame,
    cursor: _psycopg.cursor,
    table: str,
    schema: str,
    key_column: str,
    dtypes: Dict[str, str],
    chunksize: int = 200,
) -> None:
    """Update records stored in a DataFrame into PostgreSQL."""
    if df.empty is True:
        return

    column_placeholders: str = ", ".join(["%s"] * len(df.columns))
    insertion_columns = f"({', '.join(df.columns)})"

    update_columns = ", ".join([f"{c} = CAST(v.{c} AS {dtypes[c]})" for c in df.columns if c != key_column])

    placeholder_parameter_pair_generator = _db_utils.generate_placeholder_parameter_pairs(
        df=df, column_placeholders=column_placeholders, chunksize=chunksize
    )

    for placeholders, parameters in placeholder_parameter_pair_generator:
        sql: str = f"""
            UPDATE "{schema}"."{table}" t SET {update_columns}
            FROM (VALUES {placeholders}) AS v {insertion_columns}
            WHERE t.{key_column} = v.{key_column};
        """
        get_logger().debug("sql: %s, %s", sql, parameters)
        cursor.executemany(sql, (parameters,))

    get_logger().info("Updated %s rows in %s.%s", cursor.rowcount, schema, table)


@apply_configs
def insert(
    *,
    df: pd.DataFrame,
    cursor: _psycopg.cursor,
    table: str,
    schema: str,
    chunksize: int = 200,
) -> None:
    """Write records stored in a DataFrame into PostgreSQL."""
    if df.empty is True:
        return

    column_placeholders: str = ", ".join(["%s"] * len(df.columns))
    insertion_columns = f"({', '.join(df.columns)})"

    placeholder_parameter_pair_generator = _db_utils.generate_placeholder_parameter_pairs(
        df=df, column_placeholders=column_placeholders, chunksize=chunksize
    )

    for placeholders, parameters in placeholder_parameter_pair_generator:
        sql: str = f"""
        INSERT INTO "{schema}"."{table}" {insertion_columns}
        VALUES {placeholders};
        """
        get_logger().debug("sql: %s", sql)
        cursor.executemany(sql, (parameters,))

    get_logger().info("Inserted %s rows in %s.%s", cursor.rowcount, schema, table)