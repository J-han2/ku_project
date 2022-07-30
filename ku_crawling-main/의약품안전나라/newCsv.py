from base64 import encode
from threading import Thread
import requests as rq
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import unicodedata
import queue


def work(id, num):
    # f = pd.read_csv("의약품안전나라\dataCsv.csv", encoding='utf-8')
    global q
    page = num*3
    end_page = page + 3
    if(page == 0):
        page += 1
    
    
    while(page < end_page):
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
            
            q.put(lst)
            

            print('page : {0}, 약품 : {1} 저장'.format(
                page, dataNum))

        page += 1
    flag[num] = True
    return

q = queue.Queue()
flag = [False for i in range(5)]
th1 = Thread(target=work, args=(1, 0))
th2 = Thread(target=work, args=(2, 1))
th3 = Thread(target=work, args=(3, 2))
th4 = Thread(target=work, args=(4, 3))
th5 = Thread(target=work, args=(5, 4))

th1.start()
th2.start()
th3.start()
th4.start()
th5.start()

th1.join()
th2.join()
th3.join()
th4.join()
th5.join()

while(True):
    time.sleep(20)
    if(flag[0] is True and flag[1] is True and flag[2] is True and flag[3] is True and flag[4] is True):
        while(q.qsize() != 0):
            df = pd.DataFrame(q.get())
            df = df.transpose()
            df.to_csv("의약품안전나라\dataCsv.csv", header=False, mode='a', index=False, encoding="utf-8")
        break
    