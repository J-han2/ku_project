# 약가기준 정보조회 서비스 api 크롤링 코드

import requests
import pandas as pd
import bs4
import math
import pymysql

# 공공데이터포털 인증키, url, 파라미터
encoding = 'oCzRd7OAJtjjwnI0uBuAX4BqUpAhLWak1rh1PktX5FGssOgeD3%2FNQ%2FtG3Ps7lVrKEmZYiK6XZqy6KhlRnuO6Ew%3D%3D'
decoding = 'oCzRd7OAJtjjwnI0uBuAX4BqUpAhLWak1rh1PktX5FGssOgeD3/NQ/tG3Ps7lVrKEmZYiK6XZqy6KhlRnuO6Ew=='
encoded_key = decoding.encode('utf-8')
url = 'http://apis.data.go.kr/B551182/dgamtCrtrInfoService/getDgamtList'
params = {'ServiceKey':encoded_key, 'numOfRows':9999, 'pageNo':1, 'mdsCd':'0'}


# 응답메시지 항목명 리스트
colNameList = ['mdsCd', 'itmNm', 'mnfEntpNm', 'gnlNmCd', 'injcPthNm', 'nomNm', 'unit', 'adtStaDd', 'meftDivNo', 'payTpNm', 'sbstPsblTpNm', 'optCpmdImplTpNm',  'spcGnlTpNm',]
colNameKorList = ['약품코드', '품목명', '제조업체명', '일반명코드', '투여경로명', '규격명', '단위', '적용시작일자', '약효분류번호', '급여구분명', '대체가능구분명', '임의조제구분명', '전문일반구분명']


conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
conn.set_charset('utf8mb4')
cur = conn.cursor()

sql = "INSERT INTO mdfee (약품코드, 품목명, 제조업체명, 일반명코드, 투여경로명, 규격명, 단위, 적용시작일자, 약효분류번호,  급여구분명, 대체가능구분명, 임의조제구분명, 전문일반구분명) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

# 요청 파라미터의 mdsCd값을 바꿈
for i in range(36):
    if i<10:
        mds_cd = i
    else:
        mds_cd = chr(i+55)
    
    # 첫번째 페이지를 읽어와서 totalCount값과 데이터 얻어옴
    params['pageNo']=1
    params['mdsCd']=mds_cd
    print("mdsCd=", mds_cd)
    
    response = requests.get(url, params=params)
    content = response.text;

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')
    totalCount = int(xml_obj.find('totalCount').get_text())
    print(totalCount)
    count = math.ceil(totalCount/params['numOfRows'])

    result = []
    
    # 맨 마지막 page까지 반복
    for page in range(1,count+1):
        if page!=1:
            print("page:", page)
            params['pageNo'] = page
            response = requests.get(url, params=params)
            content = response.text;
            xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
            rows = xml_obj.findAll('item')
            
        # 한 page 내의 전체 데이터에서 item별로 분리
        for item in rows:
            colList = []
            
            # item 내에서 항목별로 분리
            for colName in colNameList:
                try:
                    value = item.find(colName).get_text()
                except AttributeError:
                    value = ""
                index = colNameList.index(colName)
                colList[index]=value
            result.append(colList)
            # print(tuple(colList.values()))
            
    cur.execute(sql, tuple(result))

# 전체 데이터 csv로 저장
# df = pd.DataFrame(result)
# df.to_csv("약가기준정보조회서비스.csv", mode='w', encoding='utf-8-sig')

# sql = "select * from mdfee"
# cur.execute(sql)
# result = cur.fetchall()
# print(result)
