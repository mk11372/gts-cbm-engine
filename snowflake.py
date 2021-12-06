import snowflake.connector

# ==== Manage connection to Snowflake service ====

def open_snowflake_connection():
    # Configuration parameters
    cnn = snowflake.connector.connect (
    user='MICHAELK',
    password='nEKZUgX4wy7bUj6',
    account='fa82594.us-central1.gcp',
    warehouse='CSR_DB_LOAD',
    database='CSR_DB',
    schema='CSR_RAW'
    )
    return cnn

def open_snowflake_cursor(cnn):
    cs = cnn.cursor()
    return cs

def close_snowflake_cursor(cs):
    cs.close

def close_snowflake_connection(cnn):
    cnn.close