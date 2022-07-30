import traceback
import pymysql
import requests
import json
import pandas as pd
import sys
import time
import random

sndData = {'medcCd':'', 'gnlNmCd':''}
url = 'https://www.hira.or.kr/rg/dur/getRestListJson.do'

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
cur = conn.cursor()

select_sql = "select 약품코드,일반성분코드 from mdfee"
cur.execute(select_sql)
table = cur.fetchall()

result=[]
insert_sql = "insert into durtable (약품코드,일반명코드,연령금기,임부금기,사용중지,용량주의,투여기간주의,노인주의) values (%s,%s,%s, %s, %s, %s, %s, %s);"

for i in range(1, len(table)):
    medc_cd = table[i][0]
    gnl_nm_cd = table[i][1]
    flag=False
    row={}
    
    sndData['medcCd'] = medc_cd
    sndData['gnlNmCd'] = gnl_nm_cd
    
    response = requests.post(url, data=sndData)
    
    if response.status_code==200:
        try:
            data = json.loads(response.text)

            data = data['data']['rest']
            
            age=""
            reason=""
            suspDtD=""
            suspDtI=""
            suspDtJ=""
            msg = ""
            
            # 연령금기
            if data['B'] != None:
                age = data['B'][0]['spcAge'] + data['B'][0]['spcAgeUnit']
                flag=True
            
            # 임부금기
            if data['C'] != None:
                reason = data['C'][0]['imcompReason']
                flag=True
                
            # 사용(급여)중지
            if data['D'] != None:
                suspDtD = data['D'][0]['suspDt']
                flag=True
                
            # 용량주의
            if data['I'] != None:
                suspDtI = data['I'][0]['suspDt'] + '이내'
                flag=True
                
            # 투여기간 주의
            if data['J'] != None:
                suspDtJ = data['J'][0]['suspDt']
                flag=True
                
            # 노인주의
            if data['L'] != None:
                msg = '65세이상 고령자 복용 시 주의'
                flag=True
                
            if flag==True:
                row = {'약품코드':medc_cd,'일반성분코드':gnl_nm_cd, '연령금기': age, '임부금기': reason, '사용중지':suspDtD, '용량주의':suspDtI, '투여기간주의':suspDtJ, '노인주의':msg}
            
                result.append(row)
                cur.execute(insert_sql, tuple(row.values()))
        except Exception as e:
            print(e)
            print(type(e))
            print(traceback.format_exc())
            print(medc_cd, gnl_nm_cd, i)
            sys.exit(0)
    
    if i%5==0:
        if i%100 ==0:
            print(i, row)
        t = random.randrange(1,5)
        print(i)
        time.sleep(t)

df = pd.DataFrame(result)
df.to_csv("dur.csv", mode='w', encoding='utf-8-sig')
