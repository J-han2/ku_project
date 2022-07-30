from base64 import encode
import requests as rq
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import pymysql
from datetime import datetime, timedelta

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
cur = conn.cursor()


# 안전나라 크롤링
def work():
    today_date = datetime.today()
    update_date = today_date + timedelta(days=-3)
    
    cur.execute("select 허가일 from safecountry order by 허가일 desc limit 1")
    recent_date = cur.fetchone()[0]
    recent_four_date = recent_date + timedelta(days=-4)
    
    cur.execute("select * from safecountry where 허가일 > %s order by 허가일 desc", recent_four_date)
    table = cur.fetchall()
    
    page = 1
    while(True):
        mainPage = rq.get('https://nedrug.mfds.go.kr/searchDrug?sort=ITEM_PERMIT_DATE&sortOrder=true&searchYn=&ExcelRowdata=&page='+str(page)+'&searchDivision=detail&itemName=&entpName=&ingrName1=&ingrName2=&ingrName3=&itemSeq=&stdrCodeName=&atcCodeName=&indutyClassCode=&sClassNo=&narcoticKindCode=&cancelCode=&etcOtcCode=&makeMaterialGb=&searchConEe=AND&eeDocData=&searchConUd=AND&udDocData=&searchConNb=AND&nbDocData=&startPermitDate=&endPermitDate=')
        time.sleep(random.randint(1, 5))
        bsMainPage = BeautifulSoup(mainPage.content, 'html.parser')
        for dataNum in range(1, 16):

            # category = [category for category in f.columns]
            category = ['제품명','성상','모양','업체명','전문/일반','허가일','품목기준코드','허가심사유형','마약류구분','취소/취하구분','기타식별표시','취소/취하일자','모델명','원료약품 및 분량','효능효과','용법용량','사용상의 주의사항','저장방법','사용기간','포장정보','보험약가','ATC코드','변경이력']
            lst = [None]*len(category)

            link = bsMainPage.select_one('#con_body > div.mediWrap.m-search > div.r_sec_md > div.table_scroll > table > tbody > tr:nth-child('+str(
                dataNum)+') > td:nth-child(2) > span:nth-child(2) > a')
            if(link is None):
                print("crawling 종료")
                exit()

            drugPage = rq.get("https://nedrug.mfds.go.kr" + link["href"])
            bsDrugPage = BeautifulSoup(drugPage.content, 'html.parser')

            # 기본 정보
            data = bsDrugPage.select(
                '#content > section > div.drug_info_top > div.r_sec > table > tr')

            if data is not None:
                for i in data:
                    data_tr = i.select_one('th')
                    data_td = i.select_one('td')
                    try:
                        index = category.index(data_tr.string)
                    except IndexError:
                        continue
                    except ValueError:
                        continue
                    except AttributeError:
                        continue
                    if category[index] == '제품명':
                        data_td = data_td.select_one('span')
                    if category[index] == '업체명':
                        data_td = data_td.select_one('button')
                    if category[index] == '허가일':
                        if datetime.strptime(data_td.string, "%Y-%m-%d").date() <= recent_four_date:
                            print("크롤링 종료")
                            exit()

                    try:
                        lst[index] = data_td.string
                    except AttributeError:
                        lst[index] = data_td

            data = bsDrugPage.select_one('#scroll_02 > h3')
            if data is not None:
                index = category.index("원료약품 및 분량")
                lst[index] = data

            # 효능효과
            data = bsDrugPage.select_one('#_ee_doc')
            index = category.index("효능효과")
            if data is not None:
                lst[index] = data

            # 용법용량
            data = bsDrugPage.select_one('#_ud_doc')
            index = category.index("용법용량")
            if data is not None:
                lst[index] = data

            # 사용상의 주의사항
            data = bsDrugPage.select('#_nb_doc')
            index = category.index("사용상의 주의사항")
            if data is not None:
                lst[index] = data


            data = bsDrugPage.select('#scroll_07 > table > tr')

            if data is not None:
                for i in data:
                    data_tr = i.select_one('th')
                    data_td = i.select_one('td')
                    try:
                        index = category.index(data_tr.string)
                    except IndexError:
                        continue
                    except ValueError:
                        continue
                    try:
                        lst[index] = data_td.string
                    except AttributeError:
                        lst[index] = data_td
                        

            # 변경 이력
            data = bsDrugPage.select('#tblChf > tbody > tr')
            if data is not None:
                sum = ""
                for temp in data:
                    dataTemp = temp.select('tr > td > span:nth-child(2)')
                    for i in range(0, 3):
                        sum += dataTemp[i].string
                index = category.index("변경이력")
                lst[index] = sum
            
            
            
            for e in range(len(lst)):
                if lst[e] is None:
                    lst[e] = ''
                else:
                    lst[e] = str(lst[e])
            lst = processing(lst)
            
            insert_sql = "INSERT INTO safecountry (제품명,성상,모양,업체명,전문일반,허가일,품목기준코드,허가심사유형,마약류구분,취소취하구분,기타식별표시,취소취하일자,모델명,원료약품및분량,효능효과,용법용량,주의사항,저장방법,사용기간,포장정보,보험약가,ATC코드,변경이력) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            if datetime.strptime(lst[5], "%Y-%m-%d")>=update_date:
                print('page : {0}, 약품 : {1}, 허가일 : {2} -> 최근 3일 데이터, 저장 안함'.format(page, dataNum, lst[5]))
                
            elif datetime.strptime(lst[5], "%Y-%m-%d").date() > recent_date:
                cur.execute(insert_sql, tuple(lst))
                print('page : {0}, 약품 : {1}, 허가일 : {2} -> 바로 저장'.format(page, dataNum, lst[5]))
                
            else:
                print('page : {0}, 약품 : {1}, 허가일 : {2} -> db기준 최신4일 데이터, 비교 후 저장'.format(page, dataNum, lst[5]))
                
                dup_flag = False
                for db in table:
                    if lst[0]==db[1] and lst[3]==db[4] and lst[5]==str(db[6]):
                        dup_flag=True
                        break
                
                if dup_flag:
                    print('page : {0}, 약품 : {1}, 허가일 : {2} -> 중복데이터 저장안함'.format(page, dataNum, lst[5]))
                else:
                    cur.execute(insert_sql, tuple(lst))
                    print('page : {0}, 약품 : {1}, 허가일 : {2} -> 중복없음 저장'.format(page, dataNum, lst[5]))
    
        page += 1


# 데이터 전처리 함수
def processing(row):
    # 주의사항
    caution = row[16]
    caution = caution.replace('[<div class="info_box mt30 pt0 notice" id="_nb_doc">', "")
    caution = caution[:-7]
    caution = caution.replace("\n", "")
    
    idx= 0
    for k in range(4):
        idx = caution.find('<p class="title">', idx)
        if idx == -1:
            break
        idx += 17
    
    if idx!= -1:
        caution = caution[:idx-17]
    
    while caution.find('<div class="_table_wrap_out">') > -1:
        start = caution.find('<div class="_table_wrap_out">')
        end = caution.find('</table></div></div>', start+20)
        caution = caution[:start] + caution[end+20:]
    
    while caution.find(' style="') > -1:
        start = caution.find(' style="')
        end = caution.find('"', start+8)
        caution = caution[:start]+caution[end+1:]
    
    while caution.find(' src="') > -1:
        start = caution.find(' src="')
        end = caution.find('"', start+6)
        caution = caution[:start]+caution[end+1:]
    
    if len(caution.encode('utf-8'))>65000:
        idx = caution.rfind('<p class="title">')
        caution = caution[:idx]
        
    row[16] = caution
    # print(caution)
    
    if len(caution.encode('utf-8'))>60000:
        print("caution(60000이상):",row[0])
        print(caution)

    # 용법 용량
    capacity = row[15]
    capacity = capacity.replace('<div class="info_box mt20 pt0" id="_ud_doc">', "")
    capacity = capacity[:-6]
    capacity = capacity.replace("\n", "")
    
    while capacity.find('<div class="_table_wrap_out">') > -1:
        start = capacity.find('<div class="_table_wrap_out">')
        end = capacity.find('</table></div></div>', start+20)
        capacity = capacity[:start] + capacity[end+20:]
    
    while capacity.find(' style="') > -1:
        start = capacity.find(' style="')
        end = capacity.find('"', start+8)
        capacity = capacity[:start]+capacity[end+1:]
    
    while capacity.find(' src="') > -1:
        start = capacity.find(' src="')
        end = capacity.find('"', start+6)
        capacity = capacity[:start]+capacity[end+1:]
        
    # print(capacity)
    row[15] = capacity
    
    if len(capacity.encode('utf-8'))>60000:
        print("capacity(60000이상):",row[0])
        print(capacity)
    
    #효능효과
    effect = row[14]
    effect = effect.replace('<div class="info_box" id="_ee_doc">', "")
    effect = effect[:-6]
    effect = effect.replace("\n", "")
    
    while effect.find('<div class="_table_wrap_out">') > -1:
        start = effect.find('<div class="_table_wrap_out">')
        end = effect.find('</table></div></div>', start+20)
        effect = effect[:start] + effect[end+20:]
    
    while effect.find(' style="') > -1:
        start = effect.find(' style="')
        end = effect.find('"', start+8)
        effect = effect[:start]+effect[end+1:]
        
    while effect.find(' src="') > -1:
        start = effect.find(' src="')
        end = effect.find('"', start+6)
        effect = effect[:start]+effect[end+1:]
        
    # print(effect)
    row[14] = effect
    
    if len(effect.encode('utf-8'))>30000:
        print("effect(30000이상):",row[0])
    
    #원료약품및 분량
    raw = row[13]
    raw = raw.replace('<h3 class="cont_title3 mt27 pb10">', "")
    raw = raw[:-5]
    raw = raw.replace("\n", "")
    # print(raw)
    row[13] = raw
    
    
    # print(row)
    return row


work()

