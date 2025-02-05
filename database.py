import psycopg2

# Konfiguracja bazy danych
DB_NAME = "communicator"
DB_USER = "postgres"
DB_PASSWORD = "Kornel2012!"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn
