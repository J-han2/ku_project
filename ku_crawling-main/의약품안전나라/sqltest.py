import pymysql

# crawlingDB 데이터베이스 생성
conn = pymysql.connect(host='localhost', user='root',
                       password='roel0429', db='crawlingtestdb', charset='utf8')
cursor = conn.cursor()

# sql = "CREATE DATABASE crawlingDB"
# sql = "insert into medicine(indutyCode, compName, cnsgnEntpName, profGen, classificationCode, appearance, permitDate, atcCode) values(200511454, '(주)곰스포츠', null, '의약외품', 33800, '무색의 접착제가 도포되어 있는 유백색의 테이프', '2005-01-27', null)"
sql = "insert into medicine(indutyCode, compName, cnsgnEntpName, profGen, classificationCode, appearance, permitDate, atcCode) values(%s, %s, %s, %s, %s, %s, %s, %s)"
# 참조 -> 숫자 문자 상관 없이 %s

cursor.execute(sql, (199806988, '(주)미성종합가스의료용산소', None, '전문의약품', None,
               '무색의 가스로 냄새는 없다. 1mL는 온도20℃,기압101.3Kpa에서 물32mL또는에탄올7mL에 녹는다. 1L는0℃,기압101.3Kpa에서 약1.429g이다.', '1998-07-13', None))

conn.commit()
conn.close()
