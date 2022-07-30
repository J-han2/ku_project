import pandas
import requests # 크롤링에 사용하는 패키지
import json
from bs4 import BeautifulSoup # html 변환에 사용함
import time
import re
from multiprocessing import Process, Queue
import threading

start_time = time.time()

def getLastPage(pharm_num):
    url = 'https://nedrug.mfds.go.kr/pbp/CCEKP1' + str(pharm_num + 2) + '/selectList'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        lastPage = soup.find("button", {"title": "마지막"})
        rtn = int(str(lastPage)[str(lastPage).find('(') + 1:str(lastPage).find(')')])
        # print(rtn)
    else:
        print(response.status_code)
        return 0
    return rtn


def getIDList(pharm_num, page_num, num_list):
    for i in range(0, page_num):
        url = 'https://nedrug.mfds.go.kr/pbp/CCEKP1' + str(pharm_num + 2) + '/selectList?page=' + str(i + 1)
        response = requests.get(url)
        if response.status_code == 200:  # URL OK
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            num_data = soup.findAll("td", {"class": "al_l"})

            flag = True
            num_list.append([])
            for num in num_data:
                if flag == False:
                    flag = True
                    continue
                num_list[i].append(str(num)[95:101])
                flag = False


def getString(str):
    if str is not None:
        return re.sub(pattern='<[^>]*>', repl='', string=str)


id_list1 = []
id_list2 = []
last_page_1 = getLastPage(1)
last_page_2 = getLastPage(2)
getIDList(1, last_page_1, id_list1)
getIDList(2, last_page_2, id_list2)

data_form1 = [] #csv data 형식
data_form2 = []

cookies = {
    'elevisor_for_j2ee_uid': 'gg5stp28hp4sf',
    'jrpid': 'server2',
    'JSESSIONID': 'iz3tByrzRiFijmDR73nNf2p3Osr8Tqmda0lgjV1E8ahN73fF7cydxGGOEz7n4tmh.amV1c19kb21haW4vZXh0X3NlcnZlcjM=',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'elevisor_for_j2ee_uid=gg5stp28hp4sf; jrpid=server2; JSESSIONID=iz3tByrzRiFijmDR73nNf2p3Osr8Tqmda0lgjV1E8ahN73fF7cydxGGOEz7n4tmh.amV1c19kb21haW4vZXh0X3NlcnZlcjM=',
    'Origin': 'https://nedrug.mfds.go.kr',
    'Referer': 'https://nedrug.mfds.go.kr/pbp/CCEKP13/selectEkpPopupList?phcpaArtclNo=300001&artclTitleGubn=kor&phcpaVersion=12&detailPage=1&detailArtclTitleGubn=kor&searchType=detail&phcpaLclasCode=EKP3',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'phcpaLclasCode': '',
    'phcpaVersion': '12',
    'changeTargetIem': '',
    'phcpaArtclNo': '',
    'pageUrl': '',
    'seq': '',
}


category_eng = ['artclTitle', 'ecitmEngName', 'ecitmMlrfma', 'ecitmIngrName', 'ecitmContRegltn', 'ecitmPtcse',
            'ecitmChartn', 'ecitmConfirmExam', 'ecitmRfdx', 'ecitmSapv', 'ecitmSrp', 'ecitmRelimp', 'ecitmAcdv',
            'ecitmAotn', 'ecitmIodv', 'ecitmMtpt', 'ecitmFzpt', 'ecitmVisty', 'ecitmDstlExam', 'ecitmPh',
            'ecitmOtcdt', 'ecitmPrtdgExam', 'ecitmCnstrOutage', 'ecitmRsdueoutage', 'ecitmMostr',
            'ecitmRsdueIgntn', 'ecitmAsh', 'ecitmAiAsh', 'ecitmSterilityExam', 'ecitmEdxn', 'ecitmPyrxiasexmttr',
            'ecitmIslbtAnastExam', 'ecitmInjectionsIslbtExam', 'ecitmCrblgexam', 'ecitmElutionexam',
            'ecitmTostexam', 'ecitmProdtUfmtyExam', 'ecitmProdtUfmtyDistrbExam', 'ecitmInjectionsAcptyExam',
            'ecitmMcrrgnsmLimit', 'ecitmAlchlcnt', 'ecitmAxeCont', 'ecitmFrmExam', 'ecitmImrto', 'ecitmFdqntlaw',
            'ecitmDecsnsex', 'ecitmStmtd']


category_kor = ['한글명', '영문명', '원소기호', '성분명', '구성', '제법',
            '성상', '확인시험', '굴절률', '비누화가', '비선광도', '비중', '산가',
            '선광도', '요오드가', '융점', '응고점', '점도', '증류시험', 'PH',
            '흡광도', '순도시험', '건조감량', '강열감량', '수분',
            '강열잔분', '회분', '산불용성회분', '무균시험', '엔도톡신', '발열성물질',
            '불용성이물시험', '주사제의불용성미립자시험', '붕해시험', '용출시험',
            '입도시험', '제제균일성시험', '제제균일성시험(분포)', '주사제의실용량시험',
            '미생물한도', '알코올수', '엑스함량', '형상시험', '이성질체비', '정량법',
            '결정성', '저장법']


def getData1(page):
    data['phcpaLclasCode'] = 'EKP3'
    for j in range(len(id_list1[page])):
        data['phcpaArtclNo'] = id_list1[page][j]
        response = requests.post('https://nedrug.mfds.go.kr/pbp/CCEKP13/selectEkpPopupView',
                                 cookies=cookies, headers=headers, data=data)
        if response.status_code == requests.codes.ok:
            temp = []
            jsonObj = json.loads(response.text)['item']
            # print(json.dumps(jsonObj, ensure_ascii=False, indent=2)) #json 출력 테스트 구문
            for k in category_eng:
                temp.append(getString(jsonObj['ekpVo'][k]))
                #print(k, ":", getString(jsonObj['ekpVo'][k]))
            #print(temp)
            data_form1.append(temp)
            #print()
        else:
            print("접속 실패", data['phcpaArtclNo'])
            print(response)


def getData2(page):
    data['phcpaLclasCode'] = 'EKP4'
    for j in range(len(id_list2[page])):
        data['phcpaArtclNo'] = id_list2[page][j]
        response = requests.post('https://nedrug.mfds.go.kr/pbp/CCEKP14/selectEkpPopupView',
                                 cookies=cookies, headers=headers, data=data)
        if response.status_code == requests.codes.ok:
            temp = []
            jsonObj = json.loads(response.text)['item']
            # print(json.dumps(jsonObj, ensure_ascii=False, indent=2)) #json 출력 테스트 구문
            for k in category_eng:
                temp.append(getString(jsonObj['ekpVo'][k]))
                #print(k, ":", getString(jsonObj['ekpVo'][k]))
            #print(temp)
            data_form2.append(temp)
            #print()
        else:
            print("접속 실패", data['phcpaArtclNo'])
            print(response)

'''if __name__ == "__main__":
    START, END = 0, 2 #last_page_1

    th1 = Process(target=getData, args=(START, END // 2))
    th2 = Process(target=getData, args=(END // 2, END))

    th1.start()
    th2.start()
    th1.join()
    th2.join()'''

# 멀티쓰레딩 - 22분 소요
# 굳이 멀티쓰레딩으로 할 필요 없을듯

if __name__ == '__main__':
    start = time.perf_counter()
    threads_first = []
    threads_second = []

    for pg in range(0, len(id_list1)):
        t = threading.Thread(target=getData1(pg))
        t.start()
        threads_first.append(t)

    for thread in threads_first:
        thread.join()

    for pg in range(0, len(id_list2)):
        t = threading.Thread(target=getData2(pg))
        t.start()
        threads_second.append(t)

    for thread in threads_second:
        thread.join()
    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')

'''
for i in range(0, len(id_list1)):
    getData1(i) '''

df = pandas.DataFrame(data_form1, columns=category_kor)
df.to_csv("data1.csv", index=False, encoding='utf-8-sig')

'''
data['phcpaLclasCode'] = 'EKP4'
for i in range(0, len(id_list2)):
    getData2(i)'''

df = pandas.DataFrame(data_form2, columns=category_kor)
df.to_csv("data2.csv", index=False, encoding='utf-8-sig')

'''
print("소요 시간 : ", time.time() - start_time)'''
