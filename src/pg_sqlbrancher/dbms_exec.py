import psycopg2
from psycopg2 import pool

class ConnectionPool:
    def __init__(self, db_host, db_port, db_name, db_user, db_password, min_connections=1, max_connections=10):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.connection_pool = None

    def create_pool(self):
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.min_connections,
                maxconn=self.max_connections,
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            print("Connection pool created successfully!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while creating connection pool: {error}")

    def get_connection(self):
        if self.connection_pool is None:
            self.create_pool()
        try:
            connection = self.connection_pool.getconn()
            if connection is not None:
                print("Connection retrieved from pool")
                return connection
            else:
                print("Connection pool exhausted")
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while retrieving connection from pool: {error}")
            return None

    def release_connection(self, connection):
        try:
            self.connection_pool.putconn(connection)
            print("Connection released back to pool")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while releasing connection back to pool: {error}")

    def close_pool(self):
        try:
            self.connection_pool.closeall()
            print("Connection pool closed successfully!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while closing connection pool: {error}")

# 커넥션 풀 설정
db_host = "localhost"
db_port = 5432
db_name = "your_database_name"
db_user = "your_username"
db_password = "your_password"

# 커넥션 풀 인스턴스 생성
connection_pool = ConnectionPool(db_host, db_port, db_name, db_user, db_password)

# 커넥션 획득 및 사용 예시
connection = connection_pool.get_connection()
if connection is not None:
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
    finally:
        connection_pool.release_connection(connection)

# 커넥션 풀 종료
connection_pool.close_pool()
