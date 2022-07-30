import requests
import pymysql
import bs4
import math
from datetime import date

decoding = 'oCzRd7OAJtjjwnI0uBuAX4BqUpAhLWak1rh1PktX5FGssOgeD3/NQ/tG3Ps7lVrKEmZYiK6XZqy6KhlRnuO6Ew=='
encoded_key = decoding.encode('utf-8')

ingred_url = 'http://apis.data.go.kr/B551182/msupCmpnMeftInfoService/getMajorCmpnNmCdList'
ingred_params = {'ServiceKey':encoded_key, 'numOfRows':1, 'pageNo':1, 'gnlNmCd':'0'}

colIngredNameList = ['divNm', 'fomnTpCdNm', 'gnlNm', 'gnlNmCd', 'injcPthCdNm', 'iqtyTxt', 'meftDivNo', 'unit']

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
cur = conn.cursor()

# totalCount를 기준으로 의약품성분약효 업데이트
def ingred_update(gnl_nm_cd):
    ingred_params['pageNo']=1
    ingred_params['numOfRows']=1
    ingred_params['gnlNmCd']=gnl_nm_cd
    print("gnlNmCd=", gnl_nm_cd)
    
    count_select_sql = "select count(*) from ingredient where 일반명코드 like '"+str(gnl_nm_cd)+"%';"
    cur.execute(count_select_sql)
    oldCount = cur.fetchone()[0]
    print(oldCount)
    
    response = requests.get(ingred_url, params=ingred_params)
    content = response.text

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    newCount = int(xml_obj.find('totalCount').get_text())
    print(newCount)
    
    j=0
    if newCount > oldCount:
        ingred_params['numOfRows']=9999
        response = requests.get(ingred_url, params=ingred_params)
        content = response.text

        xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
        rows = xml_obj.findAll('item')
        count = math.ceil(newCount/ingred_params['numOfRows'])
        
        #마지막 페이지까지 반복
        for page in range(1, count+1):
            if page!=1:
                print("page:", page)
                ingred_params['pageNo'] = page
                response = requests.get(ingred_url, params=ingred_params)
                content = response.text
                xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
                rows = xml_obj.findAll('item')
                
            for item in rows:
                colList = []
                
                gnlNmCd_value = item.find("gnlNmCd").get_text()
                select_sql = "select * from ingredient where 약품코드 = '"+str(gnlNmCd_value)+"';"
                cur.execute(select_sql)
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


# db에 없는 gnlNmCd를 insert
# 업데이트하는 날짜 기준 약 5일에 한번씩 업데이트
today_date = date.today().day
print("오늘 날짜:",today_date)
for i in range(36):
    if i%5 != today_date%5:
        continue
    if i<10:
        key = str(i)
    else:
        key = chr(i+55)
    
    ingred_update(key)
