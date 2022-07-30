import pandas as pd
import csv
import pymysql
chdata_pd=pd.read_csv('./data01.csv',header=None,index_col=None,names=None,encoding='UTF-8')
data_pd=pd.read_csv('./medicine_gradient2.csv',header=None,index_col=None,names=None,encoding='cp949')
data_np=pd.DataFrame.to_numpy(data_pd)
chdata_np=pd.DataFrame.to_numpy(chdata_pd)
total=len(chdata_pd)
count=0
boo=False
replaceword=["for","cream","capsules","tablets","syrup","injection"]#제거 단어
for i in range(total):
    boo=False
    
    data=chdata_np[i][1].replace("and",",").split(",") #,기준으로  data나눔  현재는 ,있는 컬럼의 경우 하나만 나오면 break해주는 상태
    for j in range(len(data)):
        thisdata=data[j].lower()
        thisdata=thisdata.replace(" ","")
        
        for p in replaceword:
            thisdata=thisdata.replace(p,"")
        for k in range(len(data_pd)):
            
            if thisdata==data_np[k][2].replace(" ",""):
                count+=1
                #print(chdata_np[i][1])
                boo=True
                break
        if boo:
            break
    if boo==False:
        print(chdata_np[i][1])
print(count/total*100)
