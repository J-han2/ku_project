import requests,xmltodict, json
import csv
import pymysql
import time
# f=open('의약품약효성분조회.csv','w',encoding='cp949',newline='')
# wr=csv.writer(f)
s=open("약가기준정보조회서비스(정렬후).csv",'r',encoding='cp949')#
db=s.readlines()

conn = pymysql.connect(host='localhost', user='root', 
                password='0104' )
#githubasdasd          

cur=conn.cursor()
cur.execute('CREATE DATABASE medicine_gradient')
conn.commit()
conn.close()
cur.close()
conn = pymysql.connect(host='localhost', user='root', 
                password='0104',database='medicine_gradient' )

cur=conn.cursor()

sql = '''번호 int(10) primary key,
분류명 varchar(255),
제형구분명 varchar(30),
일반명 varchar(255),
일반명코드 varchar(10) NOT NULL,
투여경로명 varchar(5),
함량내용 varchar(50),
약효분류번호 int(10),
단위 varchar(100),
품목명 varchar(255),
제조업체명 varchar(255)

) 
'''     


cur.execute(sql)    
conn.commit()
# andd="123"
# # cur = conn.cursor(pymysql.cursors.DictCursor)
# insert_sql="""insert into medicine (divNm,fomnTpNm,gnlNm,gnlNmCd,injcPthNm,iqtyTxt,meftDivNo,unit)
#                         values (%s,%s,%s,%s,%s,%s,%s,%s)"""
# val=(andd,2,"",'4','5','6','7','8')
# cur.execute(insert_sql,val)
# conn.commit()
search=['1','2','3','4','5','6','7','8','9','A','B','C']
#search=['E']
count=0

start=1#젤윗줄 건너뛰기위해서
remaincount=0
isData=False
# wr.writerow(["분류명","제형구분명","일반명","일반명코드","투여경로명","함량내용","약효분류명","단위","품목명","제조업체명"])
for num in search:
    #try:
        pagenum=1
        
        
        while(True):#페이지 모두읽으면 break
            time.sleep(2)
            key="2efPT4X0Z2LY%2BvuDRqs2j6OBfdEJ0jbYG3f1ZMPJTHWcAPdwNXTYqJATWbgKgJamy5Pzo559S8IUogx7GM56BA%3D%3D"
            url="http://apis.data.go.kr/B551182/msupCmpnMeftInfoService/getMajorCmpnNmCdList?ServiceKey={}&gnlNmCd={}&numOfRows=9999&pageNo={}".format(key,num,pagenum)
            # http://apis.data.go.kr/B551182/msupCmpnMeftInfoService/getMajorCmpnNmCdList?ServiceKey=2efPT4X0Z2LY%2BvuDRqs2j6OBfdEJ0jbYG3f1ZMPJTHWcAPdwNXTYqJATWbgKgJamy5Pzo559S8IUogx7GM56BA%3D%3D&gnlNmCd=1&numOfRows=9999
            content=requests.get(url).content
            
            dict=xmltodict.parse(content)

            jsonString=json.dumps(dict['response']['body'],ensure_ascii=False)
            
            jsonObj=json.loads(jsonString)
            if jsonObj["totalCount"]=='0':
                print(num)
                break
            result=jsonObj["items"]["item"]
            totalcount=int(jsonObj["totalCount"])


            print(num,"검색 데이터갯수: ",totalcount)
            
            val=[]

            for i in range(len(result)):#페이지에존재하는 데이터 갯수
            
                if result[i].get("unit")==None:#빈데이터 예외처리
                    result[i]["unit"]="None"
                if result[i].get("fomnTpCdNm")==None:
                    result[i]["fomnTpCdNm"]="None"
                if result[i].get("iqtyTxt")==None:
                    result[i]["iqtyTxt"]="None"
                if result[i].get("divNm")==None:
                    result[i]["divNm"]="None"
                
                for rownum in range(start,len(db)):
                    dblist=db[rownum].split(",")
                
                    if(dblist[7]==result[i]["gnlNmCd"]):
                        # wr.writerow([result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"],dblist[9],dblist[14]])
                        
                        val.append((count,result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"],"",""))
                    
                        #print(result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"],dblist[9],dblist[14])
                        count=count+1
                        start=rownum
                        isData=True
                        break

                
                if isData==False:
                    # wr.writerow([result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"]])
                    val.append((count,result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"],"",""))
                    #print(result[i]["divNm"],result[i]["fomnTpCdNm"],result[i]["gnlNm"],result[i]["gnlNmCd"],result[i]["injcPthCdNm"],result[i]["iqtyTxt"],result[i]["meftDivNo"],result[i]["unit"])
                       
                    
                    count=count+1

                    
                if count%200==0:
                    insert_sql="""insert into medicine (번호,분류명,제형구분명,일반명,일반명코드,투여경로명,함량내용,약효분류번호,단위,품목명,제조업체명)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cur.executemany(insert_sql,val)
                    conn.commit()
                    val=[]
                    print(count)    
                isData=False
            remaincount-=9999
            
            
            if remaincount<=0:
                break
            else:
                pagenum+=1        
    #except:
       # print(jsonObj)
       # break

print("끝")

# f.close()
cur.close()
conn.close()