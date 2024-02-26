import mysql.connector

# MariaDB 또는 MySQL 서버에 연결
connection = mysql.connector.connect(
    host="10.1.0.145", user="root", password="mediaexcel", database="hmc"
)

# 커서 생성
cursor = connection.cursor()

# 쿼리 실행
cursor.execute("SELECT * FROM _videoprofile")

# 결과 가져오기
result = cursor.fetchall()

# 결과 출력
for row in result:
    if row[0] == "SDI":
        print(row[1])

# 연결 및 커서 닫기
cursor.close()
connection.close()
