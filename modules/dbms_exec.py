import psycopg2
from psycopg2 import pool

# 커넥션 풀을 생성합니다
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host='192.168.209.10',
    port='5432',
    dbname='your_database',
    user='your_username',
    password='your_password'
)

# 커넥션 풀에서 커넥션을 가져옵니다
connection = connection_pool.getconn()

# 쿼리를 실행합니다
try:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table")
    results = cursor.fetchall()
    # 결과 처리
finally:
    # 커넥션을 반환합니다
    connection_pool.putconn(connection)
