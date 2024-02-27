import mysql.connector
import json

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
db_dict = {}
for row in result:
    if row[0] == 'SDI':        
        db_result = row[1].split('\n')
        for item in db_result:
            if '<!' not in item and '<' in item:
                value = item.split('>')[1].split('</')[0]
                key = item.split('/')[-1].split('>')[0]
                if value and key:
                    db_dict[key] = value

# JSON 형태로 정렬해서 출력
print(json.dumps(db_dict, indent=4))

# 연결 및 커서 닫기
cursor.close()
connection.close()



