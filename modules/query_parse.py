import sqlparse

def classify_query(query):
    parsed = sqlparse.parse(query)
    if parsed:
        for statement in parsed:
            if isinstance(statement, sqlparse.sql.Statement):
                for token in statement.tokens:
                    if isinstance(token, sqlparse.sql.Function) and token.get_name().lower() == 'nextval':
                        return 'UPDATE'
                if statement.get_type() == 'SELECT':
                    return 'SELECT'
                elif statement.get_type() in ('INSERT', 'UPDATE', 'DELETE'):
                    return 'DML'
    return 'UNKNOWN'

# 예시 쿼리
select_query = "SELECT * FROM users"
update_query = "SELECT nextval('seqname')"

# 쿼리 분류
select_classification = classify_query(select_query)
update_classification = classify_query(update_query)

# 분류 결과 출력
print(f"SELECT Query: {select_classification}")
print(f"UPDATE Query: {update_classification}")


## 함수 분류
import sqlparse

def classify_functions(query):
    parsed = sqlparse.parse(query)
    function_dict = {}
    query_classification = 'WRITE'  # 기본값 설정

    for statement in parsed:
        if isinstance(statement, sqlparse.sql.Statement):
            for token in statement.tokens:
                if isinstance(token, sqlparse.sql.Function):
                    function_name = token.get_name()
                    function_type = classify_function_type(token)

                    # 쿼리 전체가 READ로 분류되면 함수도 READ로 설정
                    if query_classification == 'READ':
                        function_dict[function_name] = 'READ'
                    else:
                        function_dict[function_name] = function_type

            # 쿼리 전체 분류 결정
            if query_classification != 'READ':
                query_classification = classify_query_type(statement)

    return function_dict

def classify_query_type(statement):
    statement_type = statement.get_type().upper()

    if statement_type == 'SELECT':
        return 'READ'
    else:
        return 'WRITE'

def classify_function_type(function):
    function_name = function.get_name().lower()

    if function_name == 'nextval':
        return 'WRITE'
    else:
        return 'READ'

# 예시 쿼리
example_query = "SELECT nextval('seqname'), current_date, sum(sales) FROM orders"

# 함수 분류
function_classification = classify_functions(example_query)

# 분류 결과 출력
for function_name, function_type in function_classification.items():
    print(f"Function: {function_name}, Classification: {function_type}")
