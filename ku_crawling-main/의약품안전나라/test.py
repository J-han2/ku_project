# 스레딩
# DB / CSV

import requests as rq
from bs4 import BeautifulSoup

# 가져오기
mainPage = rq.get('https://nedrug.mfds.go.kr/searchDrug')

# 데이터 추출
page = 1
flag = True
while(mainPage.status_code == 200 and flag):
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

        data = bsDrugPage.select(
            '#content > section > div.drug_info_top > div.r_sec > table > tr > td')
        data_attribute = bsDrugPage.select(
            '#content > section > div.drug_info_top > div.r_sec > table > tr > th')
        cnt = 0
        for i in data:
            if cnt == 0:
                i = i.select_one('td > span')
            if cnt == 2:
                i = i.select_one('td > button')
            print(data_attribute[cnt].string)
            print(i.string)
            cnt += 1

        # 원료약품 및 분량
        data = bsDrugPage.select('#scroll_02 > div.info_box > p.note')
        if data[0].string != "조회 결과가 없습니다.":
            data2 = bsDrugPage.select_one(
                '#scroll_02 > h3.cont_title3.mt27.pb10')  # 유효성분
            data3 = bsDrugPage.select(
                '#scroll_02 > h3.cont_title4.mt3.pb10.pl10')  # 첨가제
            if data2 is not None:
                print(data2.string)
            for j in data:
                print(j.string)
            for j in data3:
                print(j.string)

        # 효능효과
        data = bsDrugPage.select_one('#_ee_doc > p')

        # 용법용량
        data = bsDrugPage.select_one('#_ud_doc > p')

        # 사용상의 주의사항
        data = bsDrugPage.select('#_nb_doc > p')
        for temp in data:
            print(temp.string)

        #재심사, RMP, 보험, 기타정보

        data = bsDrugPage.select('#scroll_07 > table > tr > td')
        data_attribute = bsDrugPage.select('#scroll_07 > table > tr > th')

        cnt = 0
        for i in data:

            print(data_attribute[cnt].string)
            print(i.string)
            cnt += 1

        # 변경 이력
        data = bsDrugPage.select('#tblChf > tbody > tr')
        if data is not None:
            for temp in data:
                dataTemp = temp.select('tr > td > span:nth-child(2)')
                for i in range(0, 3):
                    print(dataTemp[i].string)

        print()
        print()
        print('----------------------------------')
        print()
        print()

    # page 넘김
    page += 1
    mainPage = rq.get('https://nedrug.mfds.go.kr/searchDrug?sort=&sortOrder=&searchYn=&ExcelRowdata=&page='+str(page) +
                      '&searchDivision=detail&itemName=&entpName=&ingrName1=&ingrName2=&ingrName3=&itemSeq=&stdrCodeName=&atcCodeName=&indutyClassCode=&sClassNo=&narcoticKindCode=&cancelCode=&etcOtcCode=&makeMaterialGb=&searchConEe=AND&eeDocData=&searchConUd=AND&udDocData=&searchConNb=AND&nbDocData=&startPermitDate=&endPermitDate=')
