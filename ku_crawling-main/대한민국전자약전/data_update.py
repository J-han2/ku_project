import datetime
import pymysql
import pandas
import requests
import json
from bs4 import BeautifulSoup
import re
import numpy

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
    'phcpaLclasCode': 'EKP3',
    'phcpaVersion': '12',
    'changeTargetIem': '',
    'phcpaArtclNo': '300001',
    'pageUrl': '',
    'seq': '',
}


category_eng = ['artclTitle', 'ecitmEngName', 'ecitmContRegltn', 'ecitmPtcse',
            'ecitmChartn', 'ecitmConfirmExam','ecitmFdqntlaw', 'ecitmStmtd', 'updateTs']


category_kor = ['한글명', '영문명', '구성', '제법',
            '성상', '확인시험', '정량법', '저장법', '갱신일']


file = open("update_info.txt", 'r')
dtemp1 = file.readline().split('-')
update_date = datetime.date(int(dtemp1[0]), int(dtemp1[1]), int(dtemp1[2]))
print("마지막 data 추가일 :", update_date)
update_num = int(file.readline())
print("data 갯수 :", update_num)
file.close()

new_data = []


def getLastPage(pharm_num):
    url = 'https://nedrug.mfds.go.kr/pbp/CCEKP1' + str(pharm_num + 2) + '/selectList'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        lastPage = soup.find("button", {"title": "마지막"})
        rtn = int(str(lastPage)[str(lastPage).find('(') + 1:str(lastPage).find(')')])
    else:
        print(response.status_code)
        return 0
    return rtn


def getNum(pharm_num, last_page):
    url = 'https://nedrug.mfds.go.kr/pbp/CCEKP1' + str(pharm_num + 2) + '/selectList?page=' + str(last_page)
    response = requests.get(url)
    if response.status_code == 200:  # URL OK
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        num_data = soup.findAll("td", {"class": "al_l"})
        return int((last_page-1) * 10 + (len(num_data) / 2))


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


def getString(s):
    if s is not None:
        return re.sub(pattern='<[^>]*>', repl='', string=s)


def updateData(pharm_num, page_num, id_list):
    cnt = 0
    data['phcpaLclasCode'] = 'EKP' + str(pharm_num + 2)
    for j in range(len(id_list[page_num])):
        data['phcpaArtclNo'] = id_list[page_num][j]
        url = 'https://nedrug.mfds.go.kr/pbp/CCEKP1' + str(pharm_num + 2) + '/selectEkpPopupView'
        response = requests.post(url, cookies=cookies, headers=headers, data=data)
        if response.status_code == requests.codes.ok:
            jsonObj = json.loads(response.text)['item']
            dtemp2 = getString(jsonObj['ekpVo']['updateTs']).split('-')
            add_date = datetime.date(int(dtemp2[0]), int(dtemp2[1]), int(dtemp2[2]))
            if add_date > update_date:
                temp = []
                for k in category_eng:
                    temp.append(getString(jsonObj['ekpVo'][k]))
                new_data.append(temp)
                cnt += 1
                if cnt == add_num:
                    return cnt
        else:
            print("접속 실패", data['phcpaArtclNo'])
            print(response)
            return -1

print("대한민국 전자약전 사이트의 data 갯수 확인중..")
last_page_1 = getLastPage(1)
last_page_2 = getLastPage(2)
data_num = getNum(1, last_page_1) + getNum(2, last_page_2)
print("사이트의 data 갯수 :", data_num)


conn = pymysql.connect(
    host='49.50.175.105',
    user='kuperation',
    password='kuperation2022^^',
    db='kuperation',
    charset='utf8',
    autocommit=True)
conn.set_charset('utf8mb4')
curs = conn.cursor()

sql_string = "select * from mdbook"
curs.execute(sql_string)

row = curs.fetchone()
date_list = []

while row:
    date_list.append(row[9]) #갱신일
    row = curs.fetchone()


if len(date_list) > update_num:
    print("오류 : 데이터 개수가 올바르지 않습니다.")
elif len(date_list) == data_num:
    print("추가할 데이터가 없습니다.")
elif len(date_list) < data_num:
    add_num = data_num - len(date_list)
    print(add_num, "개의 추가 데이터를 발견 했습니다.")
    print("데이터 추가 중..")
    id_list1 = []
    getIDList(1, last_page_1, id_list1)
    if updateData(1, last_page_1, id_list1) < add_num:
        id_list2 = []
        getIDList(2, last_page_2, id_list2)
        updateData(2, last_page_2, id_list2)


if len(new_data) != 0:
    ins_sql = "insert into mdbook (영문명,한글명,구성,제법,성상,확인시험,정량법,저장법,갱신일) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    curs.executemany(ins_sql, new_data)
    for row in new_data:
        if row[9] > update_date:
            update_date = row[9]

    update_num = update_num + len(new_data)

    file2 = open("update_info.txt", 'w')
    file2.write(str(update_date) + '\n')
    file2.write(str(update_num))
    file2.close()

curs.close()
conn.close()
