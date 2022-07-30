import pymysql
import pandas as pd
import time

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)
conn.set_charset('utf8mb4')
cur = conn.cursor()

totalCount=0
for i in range(23):
    dataTable = pd.read_csv("csv데이터\dataCsv_"+str(i)+".csv", encoding='utf-8',keep_default_na=False, header=None)
    dataTable = dataTable.values.tolist()
    
    if dataTable[0][0]=='제품명':
        del dataTable[0]
    
    result = []
    # for row in dataTable:
    for j in range(len(dataTable)):
        row = dataTable[j]
        
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
        
        result.append(tuple(row))
        # print(row[0], row[16])
        # print(j, row[0])
        insert_sql = "INSERT INTO safecountry (제품명,성상,모양,업체명,전문일반,허가일,품목기준코드,허가심사유형,마약류구분,취소취하구분,기타식별표시,취소취하일자,모델명,원료약품및분량,효능효과,용법용량,주의사항,저장방법,사용기간,포장정보,보험약가,ATC코드,변경이력) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        if j%100 ==0:
            cur.executemany(insert_sql, tuple(result))
            result = []
            print(j, i)
    
    # print(result)
    cur.executemany(insert_sql, tuple(result))
    print(len(result), i)
    time.sleep(10)
    
    totalCount+=len(dataTable)

print(totalCount)