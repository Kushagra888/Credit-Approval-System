import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_postgres_db():
    
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5433')
    user = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'root')
    dbname = os.environ.get('POSTGRES_DB', 'credit_approval')
    
    if os.environ.get('DOCKER_ENV') == 'true':
        host = 'db'
        port = '5432'
    
    # Connect to server
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
    exists = cursor.fetchone()
    
    if not exists:
        try:
            # Create db
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"Database '{dbname}' created successfully")
        except Exception as e:
            print(f"Error creating database: {e}")
    else:
        print(f"Database '{dbname}' already exists")
    
 
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_postgres_db()
    print("PostgreSQL database setup complete")