import pandas as pd
import csv
import pymysql
import datetime
data_pd=pd.read_csv('./e약은요정보검색.csv',header=None,index_col=None,names=None,encoding='cp949')
data_np=pd.DataFrame.to_numpy(data_pd)

conn = pymysql.connect(host='49.50.175.105', user='kuperation', password='kuperation2022^^', db='kuperation', charset='utf8', autocommit=True)

cur=conn.cursor()
create_sql="""CREATE TABLE Emedicine( 
품목일련번호 int(10) primary key,
제품명 varchar(255),
업체명 varchar(30),
주성분 varchar(500),
효능 varchar(500) ,
사용법 varchar(1000),
복용전지식 varchar(500),
주의사항 varchar(1200),
병용금기 varchar(1000),
이상반응 varchar(1000),
보관방법 varchar(255),
공개일자 Date,
수정일자 Date
)"""

cur.execute(create_sql)    
conn.commit()
insert_sql="""insert into Emedicine (품목일련번호,제품명,업체명,주성분,효능,사용법,복용전지식,주의사항,병용금기,이상반응,보관방법,공개일자,수정일자)
                         values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
 """
val=[]

nowdata=[0]*13#csv데이터 한셀씩
datetime_format="%Y-%M-%d"
for i in range(1,len(data_np)):
    
    nowdata[0]=int(data_np[i][0])
    nowdata[11]=datetime.datetime.strptime(data_np[i][11],datetime_format).date()
    nowdata[12]=datetime.datetime.strptime(data_np[i][12],datetime_format).date()
    
   #날짜형식
    for k in range(1,11):
        if type(data_np[i][k])==float:
            nowdata[k]=""
            
        else:
            
            nowdata[k]=data_np[i][k]
    
    
    val.append(tuple(nowdata))
    if i%1000==0:
        cur.executemany(insert_sql,val)
        conn.commit()
        val=[]
        print(i) 

    

cur.close()
conn.close()