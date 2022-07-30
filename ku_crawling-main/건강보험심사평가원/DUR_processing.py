import pymysql
import pandas as pd
import re

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
cur = conn.cursor()

durTable = pd.read_csv("건강보험심사평가원\DUR.csv", encoding='utf-8',keep_default_na=False)
durTable = durTable.values.tolist()
# print(durTable)

delete_sql = "delete from durtable where 약품코드=%s"
update_preg_sql = "update durtable set 임부금기=%s where 약품코드=%s"

regExp = re.compile('[(][A-Za-z ]+[)]') # (성분명)의 형식
regExp1 = re.compile(', [(][A-Za-z ]+[)]') # , (성분명)의 형식으로 한 문장 사이에 끼어있는 경우
regExp2 = re.compile('[0-9][.][0-9]') # 0.2mg 처럼 숫자 소수점
regExp3 = re.compile('[0-9]') #숫자
regExp4 = re.compile('[가-힣][/][A-Za-z]') #성분명:설명/성분명:설명 의 형식에서 / 찾기

result = []
# for i in range(0, 500):
for row in durTable:
    append_flag = True
    
    # row = durTable[i]
    # print(row)
    medcCd = row[0] #약품코드
    age = row[2] #연령금기
    pregnant = row[3] #임부금기
    stopUse = row[4] #사용중지
    capacity = row[5] #용량주의
    period = row[6] #투여기간주의
    senior = row[7] #노인주의
    
    #임부금기
    if pregnant=='-': # '-'만 들어가있는 데이터 제거
        print(row)
        pregnant=''
        
    if (age=='' and pregnant=='' and stopUse=='' and capacity =='' and period=='' and senior=='') :
        print(medcCd, '삭제')
        cur.execute(delete_sql, medcCd)
        append_flag=False
        
    if pregnant != '': #임부금기 데이터가 존재하는 경우
        
        # . 으로 구분해서 리스트 형태로 데이터 삽입
        if regExp2.search(pregnant) is not None: #.으로 구분했을때 숫자 소수점 구분되는 경우 방지
            pregList = pregnant.split(".")
            pregnant=[]
            i=0
            while i<len(pregList)-1:
                if regExp3.match(pregList[i][-1]) is not None and regExp3.match(pregList[i+1][0]) is not None:
                    pregnant.append(pregList[i]+'.'+pregList[i+1])
                    i+=1
                else:
                    pregnant.append(pregList[i])
                i+=1
            
            pregList = pregnant
            pregnant=[]
            i=0
            while i<len(pregList)-1:
                if regExp3.match(pregList[i][-1]) is not None and regExp3.match(pregList[i+1][0]) is not None:
                    pregnant.append(pregList[i]+'.'+pregList[i+1])
                    i+=1
                else:
                    pregnant.append(pregList[i])
                i+=1
        else :
            pregList = pregnant.split(".")
            pregnant = pregList
        
        update_preg = []
        for preg in pregnant:
            # print(preg)
            preg = preg.strip()
            
            if preg != '': #리스트 안에 빈 항목 제거
                update_preg.append(preg)
            
            if preg.find("\n")!= -1: #\n이 들어가 있는 항목 분리
                update_preg.remove(preg)
                temp = preg.split("\n")
                for j in temp:
                    update_preg.append(j)
            
            if preg.find("/")==0: #/로 시작하는 항목 제거
                update_preg.remove(preg)
                update_preg.append(preg[1:])
            
            # /으로 구분된 성분관련 정보 분리
            r=regExp4.findall(preg)
            if len(r)!=0:
                print(preg)
                update_preg.remove(preg)
                start=0
                for i in r:
                    end = preg.find(i)
                    update_preg.append(preg[start:end+1])
                    start = end+2
                    
                update_preg.append(preg[start:])
            
            if regExp.match(preg) is not None: #(성분명):~~ 인 항목 -> 성분명:~~ 으로 변경
                update_preg.remove(preg)
                preg = preg[1:]
                preg = preg.replace(')',':',1)
                update_preg.append(preg)

            r=regExp1.search(preg)
            if r is not None:
                update_preg.remove(preg)
                update_preg.append(preg[:r.start()])
                temp = preg[r.start()+3:].replace(')',':',1)
                update_preg.append(temp)
            

    row = [medcCd, row[1], age, update_preg, stopUse, capacity, period, senior]

    
    if append_flag:
        cur.execute(update_preg_sql, (str(row[3]), medcCd))
        result.append(row)
        # print(row)

    
df = pd.DataFrame(result, columns=['약품코드','일반명코드','연령금기','임부금기','사용중지','용량주의','투여기간주의','노인주의'])
df.to_csv("건강보험심사평가원\DUR_process.csv", mode='w', encoding='utf-8-sig', index=False)