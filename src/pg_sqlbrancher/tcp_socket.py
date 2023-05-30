import sqlparse
import psycopg2
from psycopg2 import pool
from multiprocessing import Process
import threading

# 1번 서버 커넥션 풀 생성
server1_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host='1번 서버 주소',
    port=5432,
    user='사용자명',
    password='비밀번호',
    database='데이터베이스명'
)

# 2번 서버 커넥션 풀 생성
server2_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host='2번 서버 주소',
    port=5432,
    user='사용자명',
    password='비밀번호',
    database='데이터베이스명'
)

def execute_query(query, pool):
    connection = pool.getconn()  # 커넥션 풀에서 커넥션 가져오기
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    pool.putconn(connection)  # 커넥션 풀에 커넥션 반환

    return result

def process_query(query):
    # sqlparse를 사용하여 쿼리를 분석합니다.
    parsed_query = sqlparse.parse(query)[0]

    # 분석된 쿼리의 유형을 확인합니다.
    if parsed_query.get_type() == "SELECT":
        pool = server1_pool  # 1번 서버 커넥션 풀 선택
    else:
        pool = server2_pool  # 2번 서버 커넥션 풀 선택

    result = None

    def execute_query_in_thread():
        nonlocal result
        result = execute_query(query, pool)

    # 멀티프로세스를 이용하여 연결 유지하고 쿼리 실행
    process = Process(target=execute_query_in_thread)
    process.start()
    process.join()

    return result
