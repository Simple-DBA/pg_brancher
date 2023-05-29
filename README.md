# pg_brancher
SQL query branch handler for PostgreSQL

# 기본설계
```
main.py
modules
    daemon_process.py
        데몬프로세스가 실행되면 락파일 생성, 종료 시 락파일 삭제
        데몬프로세스 종류
            DB롤체크 및 DB상태를 전역변수로 저장
            소켓 생성 및 삭제
        서브프로세스
            main daemon
                pgbranch_role_checker
                pgbranch_socketer
                pgbranch_pool_maker
    dbms_exec.py
        pool_maker
        query_exec
    query_parse.py
        query_classifyer : 쿼리를 체크하여 분류한다. 만약 분류된 대로 쿼리를 DBMS에 입력했을 시, 에러가 발생한다면 해당 쿼리를 master로 보낸다.
        function_classifyer : 쿼리가 가지고있는 함수들을 분리해낸다. 함수들은 쿼리의 결과에 따라 read와 write로 분류된다. write를 기본으로하며, 쿼리의 결과가 read only인 경우에만 read로 분류된다. 분류된 함수들은 명칭과 역할로 분류되어 딕셔너리 변수와 JSON파일에 저장된다.(머지문은 나중에)
    tcp_ip_socket.py
        create_socket
        delete_socket
    global.py
        로깅
        컨피규어 파일 로딩
```

# 필수 패키지
pip install sqlparse
pip install psycopg2
pip install pyyaml
