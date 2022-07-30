import requests
import pymysql
import bs4
import math
import json
import re

decoding = 'oCzRd7OAJtjjwnI0uBuAX4BqUpAhLWak1rh1PktX5FGssOgeD3/NQ/tG3Ps7lVrKEmZYiK6XZqy6KhlRnuO6Ew=='
encoded_key = decoding.encode('utf-8')
mdfee_url = 'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getDgamtList'
params = {'ServiceKey':encoded_key, 'numOfRows':9999, 'pageNo':1, 'mdsCd':'0'}

dur_url = 'https://www.hira.or.kr/rg/dur/getRestListJson.do'
dur_sndData = {'medcCd':'', 'gnlNmCd':''}

ingred_url = 'http://apis.data.go.kr/B551182/msupCmpnMeftInfoService/getMajorCmpnNmCdList'
ingred_params = {'ServiceKey':encoded_key, 'numOfRows':9999, 'pageNo':1, 'gnlNmCd':'0'}

colNameList = ['mdsCd', 'itmNm', 'mnfEntpNm', 'gnlNmCd', 'injcPthNm', 'nomNm', 'unit', 'adtStaDd', 'meftDivNo', 'payTpNm', 'sbstPsblTpNm', 'optCpmdImplTpNm',  'spcGnlTpNm',]
colNameKorList = ['약품코드', '품목명', '제조업체명', '일반명코드', '투여경로명', '규격명', '단위', '적용시작일자', '약효분류번호', '급여구분명', '대체가능구분명', '임의조제구분명', '전문일반구분명']
colIngredNameList = ['divNm', 'fomnTpCdNm', 'gnlNm', 'gnlNmCd', 'injcPthCdNm', 'iqtyTxt', 'meftDivNo', 'unit']

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
cur = conn.cursor()

# dur table의 임부금기 데이터를 처리
def dur_processing(row):
    regExp = re.compile('[(][A-Za-z ]+[)]') # (성분명)의 형식
    regExp1 = re.compile(', [(][A-Za-z ]+[)]') # , (성분명)의 형식으로 한 문장 사이에 끼어있는 경우
    regExp2 = re.compile('[0-9][.][0-9]') # 0.2mg 처럼 숫자 소수점
    regExp3 = re.compile('[0-9]') #숫자
    regExp4 = re.compile('[가-힣][/][A-Za-z]') #성분명:설명/성분명:설명 의 형식에서 / 찾기
    
    append_flag = True
    age = row[2] #연령금기
    pregnant = row[3] #임부금기
    stopUse = row[4] #사용중지
    capacity = row[5] #용량주의
    period = row[6] #투여기간주의
    senior = row[7] #노인주의
    
    #임부금기
    update_preg = []
    if pregnant=='-': # '-'만 들어가있는 데이터 제거
        print(row)
        pregnant=''
        
    if (age=='' and pregnant=='' and stopUse=='' and capacity =='' and period=='' and senior=='') :
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
    
    if append_flag:
        return (row[0], row[1], age, str(update_preg), stopUse, capacity, period, senior)
    else:
        return ()


# 새로 업데이트된 약가기준 데이터를 기준으로 dur 업데이트
def dur_update(medc_cd, gnl_nm_cd):
    flag=False
                    
    # count+=1
    dur_sndData['medcCd'] = medc_cd
    dur_sndData['gnlNmCd'] = gnl_nm_cd
    
    # print(sndData)
    
    response = requests.post(dur_url, data=dur_sndData)
    
    if response.status_code==200:
        data = json.loads(response.text)
        data = data['data']['rest']
        
        age=""
        pregnant=""
        stopUse=""
        capacity=""
        period=""
        senior = ""
        
        # 연령금기
        if data['B'] != None:
            age = data['B'][0]['spcAge'] + data['B'][0]['spcAgeUnit']
            flag=True
        
        # 임부금기
        if data['C'] != None:
            pregnant = data['C'][0]['imcompReason']
            flag=True
            
        # 사용(급여)중지
        if data['D'] != None:
            stopUse = data['D'][0]['suspDt']
            flag=True
            
        # 용량주의
        if data['I'] != None:
            capacity = data['I'][0]['suspDt'] + '이내'
            flag=True
            
        # 투여기간 주의
        if data['J'] != None:
            period = data['J'][0]['suspDt']
            flag=True
            
        # 노인주의
        if data['L'] != None:
            senior = '65세이상 고령자 복용 시 주의'
            flag=True
            
        if flag==True:
            row = [medc_cd, gnl_nm_cd, age, pregnant, stopUse, capacity, period, senior]

            update_row = dur_processing(row)
            if len(update_row) != 0:
                print(update_row)
                insert_dur_sql = "insert into durtable (약품코드,일반명코드,연령금기,임부금기,사용중지,용량주의,투여기간주의,노인주의) values (%s,%s,%s, %s, %s, %s, %s, %s);"
                cur.execute(insert_dur_sql, update_row)
                

# totalCount를 기준으로 약가기준 데이터 업데이트
def mdfee_update(mds_cd):
    # 첫번째 페이지를 읽어와서 totalCount값과 데이터 얻어옴
    params['pageNo']=1
    params['mdsCd']=mds_cd
    print("mdsCd=", mds_cd)
    
    count_select_sql = "select count(*) from mdfee where 약품코드 like '"+str(mds_cd)+"%';"
    cur.execute(count_select_sql)
    oldCount = cur.fetchone()[0]
    print(oldCount)
    
    response = requests.get(mdfee_url, params=params)
    content = response.text;

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')
    newCount = int(xml_obj.find('totalCount').get_text())
    print(newCount)
    
    j=0
    if newCount > oldCount:
        count = math.ceil(newCount/params['numOfRows'])

        # 맨 마지막 page까지 반복
        for page in range(1,count+1):
            if page!=1:
                print("page:", page)
                params['pageNo'] = page
                response = requests.get(mdfee_url, params=params)
                content = response.text;
                xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
                rows = xml_obj.findAll('item')
                
            # 한 page 내의 전체 데이터에서 item별로 분리
            for item in rows:
                colList = {}
                
                mdsCd_value = item.find("mdsCd").get_text()
                select_sql = "select * from mdfee where 약품코드 = '"+str(mdsCd_value)+"';"
                cur.execute(select_sql)
                select_res = cur.fetchone()

                if select_res is None:
                    j+=1
                
                    for colName in colNameList:
                        try:
                            value = item.find(colName).get_text()
                        except AttributeError:
                            value = ""
                        index = colNameList.index(colName)
                        colList[colNameKorList[index]]=value

                    print(tuple(colList.values()))
                    insert_mdfee_sql = "INSERT INTO mdfee (약품코드, 품목명, 제조업체명, 일반명코드, 투여경로명, 규격명, 단위, 적용시작일자, 약효분류번호,  급여구분명, 대체가능구분명, 임의조제구분명, 전문일반구분명) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cur.execute(insert_mdfee_sql, tuple(colList.values()))
                    
                    # 새로 insert된 약가기준 데이터에 대한 dur 데이터 insert
                    dur_update(colList['약품코드'], colList['일반명코드'])
                    
                if newCount-oldCount == j:
                    print(mdsCd_value)
                    break
            if newCount-oldCount == j:
                break
    
    
# totalCount를 기준으로 의약품성분약효 업데이트
def ingred_update(gnl_nm_cd):
    ingred_params['pageNo']=1
    ingred_params['gnlNmCd']=gnl_nm_cd
    print("gnlNmCd=", gnl_nm_cd)
    
    count_select_sql = "select count(*) from ingredient where 일반명코드 like '"+str(gnl_nm_cd)+"%';"
    cur.execute(count_select_sql)
    oldCount = cur.fetchone()[0]
    print(oldCount)
    
    response = requests.get(ingred_url, params=ingred_params)
    content = response.text;

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')
    newCount = int(xml_obj.find('totalCount').get_text())
    print(newCount)
    
    j=0
    if newCount > oldCount:
        count = math.ceil(newCount/ingred_params['numOfRows'])
        
        #마지막 페이지까지 반복
        for page in range(1, count+1):
            if page!=1:
                print("page:", page)
                ingred_params['pageNo'] = page
                response = requests.get(ingred_url, params=ingred_params)
                content = response.text;
                xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
                rows = xml_obj.findAll('item')
                
            for item in rows:
                colList = []
                
                gnlNmCd_value = item.find("gnlNmCd").get_text()
                select_sql = "select * from ingredient where 약품코드 = '"+str(gnlNmCd_value)+"';"
                select_res = cur.fetchone()
                
                if select_res is None:
                    j+=1
                    for colName in colIngredNameList:
                        try:
                            value = item.find(colName).get_text()
                        except AttributeError:
                            value = ""
                        colList.append(value)
                    
                    insert_ingred_sql="insert into ingredient (분류명,제형구분명,일반명,일반명코드,투여경로명,함량내용,약효분류번호,단위) values (%s,%s,%s,%s,%s,%s,%s,%s);"
                    cur.execute(insert_ingred_sql, tuple(colList))
                    print(tuple(colList))
            
                if newCount-oldCount == j:
                    print(gnlNmCd_value)
                    break
            if newCount-oldCount == j:
                break


# db에 없는 mdsCd를 insert
for i in range(36):
    if i<10:
        key = i
    else:
        key = chr(i+55)
    
    mdfee_update(key)
    ingred_update(key)
