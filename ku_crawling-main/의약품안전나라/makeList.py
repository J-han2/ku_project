import csv
import requests as rq
from bs4 import BeautifulSoup
import time
import random

with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    mainPage = rq.get('https://nedrug.mfds.go.kr/searchDrug')
    listBasic = []
    listEtc = []

    # 데이터 추출
    page = 1
    flag = True
    while(mainPage.status_code == 200 and flag):
        
        time.sleep(random.randint(1,5))
        bsMainPage = BeautifulSoup(mainPage.content, 'html.parser')
        for i in range(1, 16):
            print('page : {0}, 약품 : {1}'.format(page, i))

            link = bsMainPage.select_one('#con_body > div.mediWrap.m-search > div.r_sec_md > div.table_scroll > table > tbody > tr:nth-child(' +
                                        str(i)+') > td:nth-child(2) > span:nth-child(2) > a')

            # 목록이 15개가 안 될 때
            if link is None:
                flag = False
                break
            # print(link["href"])

            # 각 약품 설명 페이지
            drugPage = rq.get("https://nedrug.mfds.go.kr" + link["href"])
            bsDrugPage = BeautifulSoup(drugPage.content, 'html.parser')
            # print(bsDrugPage)

            # data <- db에 넣을 값들
            # 기본 정보

            data_attribute = bsDrugPage.select(
                '#content > section > div.drug_info_top > div.r_sec > table > tr > th')
            cnt = 0
            for i in data_attribute:
                if (i.string not in listBasic):
                    listBasic.insert(cnt,i.string)
                cnt += 1
                

            #재심사, RMP, 보험, 기타정보

            data_attribute = bsDrugPage.select('#scroll_07 > table > tr > th')

            cnt = 0
            for i in data_attribute:
                if(i.string not in listEtc):
                    listEtc.insert(cnt,i.string)
                cnt += 1

            print(listBasic)
            print(listEtc)

        # page 넘김
        page += 1
        mainPage = rq.get('https://nedrug.mfds.go.kr/searchDrug?sort=&sortOrder=&searchYn=&ExcelRowdata=&page='+str(page) +
                        '&searchDivision=detail&itemName=&entpName=&ingrName1=&ingrName2=&ingrName3=&itemSeq=&stdrCodeName=&atcCodeName=&indutyClassCode=&sClassNo=&narcoticKindCode=&cancelCode=&etcOtcCode=&makeMaterialGb=&searchConEe=AND&eeDocData=&searchConUd=AND&udDocData=&searchConNb=AND&nbDocData=&startPermitDate=&endPermitDate=')

    data = []
    data.extend(listBasic)
    data.append("원료약품 및 분량")
    data.append("효능효과")
    data.append("용법용량")
    data.append("사용상의 주의사항")
    data.extend(listEtc)
    data.append("변경이력")
    
    writer.writerow(data)
    print("데이터 topic crawling 종료")