# API 
1. Search(검색)
   1. 약품명
   2. 성분명
   3. 증상
   4. 전체보기
2. Detail Page(상세페이지)

## 1. Search
약품/성분명 또는 증상에 대한 약품 목록 제공 API

### 1-1. 약품명
**GET** 방식
> **/search/item**

### Request
```
itemName=제품명
pageNum=페이지 숫자
```
테스트 시 아래의 데이터로 테스트해보세요.
```
itemName=맘스
pageNum=1~5까지 가능
```
### Response
```
{ 
   "pageNum": "1",
   "amount" : "10",
   "total" : "43",
   "searchDataReslst":
   
   [{
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   ,
   {
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   .
   .
   .]
}
```
### 1-2. 성분명
**GET** 방식
> **/search/ingredient**
### Request
```
ingredientName=성분명
pageNum=페이지 숫자
```
테스트 시 아래의 데이터로 테스트해보세요.
```
ingredientName=bevacizumab
pageNum=1
```
### Response
```
{
    "pageNum": 1,
    "amount": 2,
    "total": 2,
    "searchDataReslst": [
        {
            "item": "온베브지주(베바시주맙)",
            "company": "삼성바이오에피스(주)",
            "ingredient": "bevacizumab",
            "efficacy": "<p class=\"title\">● 전이성 직결장암</p><div><p class=\"indent1\">- 플루오로피리미딘계 약물을 기본으로 하는 화학요법과 병용하여 전이성 직결장암 치료. 1차 요법에서 이 약이 포함된 항암 요법을 투여한 후 진행된 전이성 직결장암 환자에게 2차 요법제로 이 약을 투여하고자 할 경우는 플루오로피리미딘-이리노테칸 또는 플루오로피리미딘-옥살리플라틴을 기본으로 하는 화학요법과 병용 투여</p></div><p class=\"title\">● 전이성 유방암</p><div><p class=\"indent1\">- 전이성 유방암 환자에 1차 요법제로 파클리탁셀과 병용투여</p><p class=\"indent1\">- 탁산 또는 안트라싸이클린을 포함하는 화학요법이 적절하지 않은 전이성 유방암 환자에 1차 요법제로 카페시타빈과 병용투여. 수술 후 보조요법으로 최근 12개월 내에 탁산과 안트라싸이클린을 투여 받은 환자는 이 약과 카페시타빈을 병용투여하지 않도록 한다.</p></div><p class=\"title\">● 비소세포폐암</p><div><p class=\"indent1\">- 수술이 불가능한 진행성, 전이성 또는 재발성 비편평상피세포성 비소세포폐암의 1차 요법제로 백금계 약물을 기본으로 하는 화학요법제와 병용투여</p><p class=\"indent1\">- EGFR 활성 변이가 있는 수술이 불가능한 진행성, 전이성 또는 재발성 비편평상피세포성 비소세포폐암의 1 차 요법제로 엘로티닙과 병용투여</p></div><p class=\"title\">● 진행성 또는 전이성 신세포암</p><div><p class=\"indent1\">- 진행성 또는 전이성 신세포암의 1차 요법제로 인터페론알파-2a와 병용투여</p></div><p class=\"title\">● 교모세포종</p><div><p class=\"indent1\">- 이전 치료 후 진행성인 교모세포종에서 이 약의 단독투여</p></div><p class=\"title\">● 상피성 난소암, 난관암 또는 원발성 복막암</p><div><p class=\"indent1\">- 진행성(FIGO stages ⅢB, ⅢC 및 Ⅳ) 상피성 난소암, 난관암 또는 원발성 복막암 환자에게 front-line 요법제로 카보플라틴과 파클리탁셀 화학요법에 병용투여</p><p class=\"indent1\">- 백금계 약물에 감수성이 있는(platinum-sensitive) 상피성 난소암, 난관암 또는 원발성 복막암 환자의 첫 번째 재발 시 카보플라틴·파클리탁셀 화학요법과 병용투여</p></div><p class=\"title\">● 자궁경부암</p><div><p class=\"indent1\">- 지속성(persistent), 재발성 또는 전이성 자궁경부암에 파클리탁셀과 시스플라틴 병용요법 또는 파클리탁셀과 토포테칸 병용요법과 함께 투여</p></div>",
            "permitDate": "2021-03-11"
        },
        {
            "item": "아바스틴주(베바시주맙)",
            "company": "(주)한국로슈",
            "ingredient": "bevacizumab",
            "efficacy": "<p class=\"title\">● 전이성 직결장암</p><div><p class=\"indent0\">- 플루오로피리미딘계 약물을 기본으로 하는 화학요법과 병용하여 전이성 직결장암 치료. 1차 요법에서 이 약이 포함된 항암 요법을 투여한 후 진행된 전이성 직결장암 환자에게 2차 요법제로 이 약을 투여하고자 할 경우는 플루오로피리미딘-이리노테칸 또는 플루오로피리미딘-옥살리플라틴을 기본으로 하는 화학요법과 병용투여</p></div><p class=\"title\">● 전이성 유방암</p><div><p class=\"indent0\">- 전이성 유방암 환자에 1차 요법제로 파클리탁셀과 병용투여</p><p class=\"indent0\">- 탁산 또는 안트라싸이클린을 포함하는 화학요법이 적절하지 않은 전이성 유방암 환자에 1차 요법제로 카페시타빈과 병용투여. 수술 후 보조요법으로 최근 12개월 내에 탁산과 안트라싸이클린을 투여 받은 환자는 이 약과 카페시타빈을 병용투여하지 않도록 한다.</p></div><p class=\"title\">● 비소세포폐암</p><div><p class=\"indent0\">- 수술이 불가능한 진행성, 전이성 또는 재발성 비편평상피세포성 비소세포폐암의 1차 요법제로 백금계 약물을 기본으로 하는 화학요법제와 병용투여</p><p class=\"indent0\">- EGFR 활성 변이가 있는 수술이 불가능한 진행성, 전이성 또는 재발성 비편평상피세포성 비소세포폐암의 1차 요법제로 엘로티닙과 병용투여</p></div><p class=\"title\">● 진행성 또는 전이성 신세포암</p><div><p class=\"indent0\">- 진행성 또는 전이성 신세포암의 1차 요법제로 인터페론알파-2a와 병용투여</p></div><p class=\"title\">● 교모세포종</p><div><p class=\"indent0\">- 이전 치료 후 진행성인 교모세포종에서 이 약의 단독투여</p></div><p class=\"title\">● 상피성 난소암, 난관암 또는 원발성 복막암</p><div><p class=\"indent0\">- 진행성(FIGO stages ⅢB, ⅢC 및 Ⅳ) 상피성 난소암, 난관암 또는 원발성 복막암 환자에게 front-line 요법제로 카보플라틴과 파클리탁셀 화학요법에 병용투여</p><p class=\"indent0\">- 이전에 이 약 또는 다른 VEGF 저해제 또는 VEGF 수용체-표적 치료제를 투여한 적이 없으면서 백금계 약물에 감수성이 있는(platinum-sensitive) 상피성 난소암, 난관암 또는 원발성 복막암 환자의 첫 번째 재발 시 카보플라틴·젬시타빈 화학요법과 병용투여</p><p class=\"indent0\">- 백금계 약물에 감수성이 있는(platinum-sensitive) 상피성 난소암, 난관암 또는 원발성 복막암 환자의 첫 번째 재발 시 카보플라틴·파클리탁셀 화학요법과 병용투여</p><p class=\"indent0\">- 이전에 이 약 또는 다른 VEGF 저해제 또는 VEGF 수용체-표적 치료제를 투여한 적이 없으면서 이전에 2가지 종류 이하의 화학요법을 투여한 환자로서 백금계 약물에 저항성이 있는(platinum-resistance) 상피성 난소암, 난관암 또는 원발성 복막암 재발 시 파클리탁셀, 토포테칸 또는 페길화 리포좀 독소루비신(pegylated liposomal doxorubicin)과 병용 투여</p></div><p class=\"title\">● 자궁경부암</p><div><p class=\"indent0\">- 지속성(persistent), 재발성 또는 전이성 자궁경부암에 파클리탁셀과 시스플라틴 병용요법 또는 파클리탁셀과 토포테칸 병용요법과 함께 투여</p></div>",
            "permitDate": "2007-09-12"
        }
    ]
}
```

### 1-3. 증상

**GET** 방식
> **/search/symptom**

### Request

```
symptom=증상1 증상2 증상3 
pageNum=페이지 숫자
증상개수는 제한없음
공백을 기준으로 증상이 모두 포함되어있는 의약품 검색
```
테스트 시 아래의 데이터로 테스트해보세요.
```
symptom= 치통 구토
pageNum=1
```
### Response
```
{ 
   "pageNum": "1",
   "amount" : "10",
   "total" : "2199",
   "searchDataRelst":
   [{
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   ,
   {
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   .
   .
   .]
}
```
### 1-4. 전체보기
**GET** 방식
> **/search/allitem**

### Request
```
pageNum=페이지 숫자
```
테스트 시 아래의 데이터로 테스트해보세요.
```

pageNum=1
```
### Response
```
{ 
   "pageNum": "1",
   "amount" : "10",
   "total" : "108970",
   "searchDataReslst":
   
   [{
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   ,
   {
       "item": " ",
       "company": " ",
       "ingredient": " ",
       "efficacy": ">"
       "permitDate" : " "
   }
   .
   .
   .]
}
```
## 2. DetailPage
특정 약품에 대한 상세 정보 제공하는 API

**POST** 방식
> **/detailPage/product**
### Request
```
{
   "name":"testName",
   "permitDate:"yyyy-mm-dd"
}
```
테스트 시 아래의 데이터로 테스트해보세요.
```
{
  "name":"라베듀엣정20/500밀리그램",
  "permitDate":"2022-01-27"
}
```
### Response
```
{
"name": "test",
"appearance": "test",
"shape": "test",
"company": "test",
"speciality": "test",
"permitDate": "yyyy-mm-dd",
"drugClassification": "test",
"cancelClassification": "test",
"etc": "test",
"modelName": "test",
"rawGradient": "test",
"efficacy": "test",
"dosage": "test",
"caution": "test",
"store": "test",
"duration": "test",
"packaging": "test",
"ageTaboo": "test",
"pragTaboo": "test",
"stopUsing": "test",
"capacityWarning":"test",
"dosingPeriodWarning": "test",
"elderWarning": "test",
"ingreList":[
["commonName: test1", "content: 00", "ingredientUnit: test"],
["commonName: test2", "content: 00", "ingredientUnit: test"]
],
"dosingRoute": "test",
"specName": "test",
"alterClassName": "test",
"mdfeeUnit": "test",
"mbList":[
   ["null", "null", "null", "null", "null", "null"],
   [
      "config: testtest",
      "pharmAppearance: testtest",
      "manufacturingMethod: testtest",
      "confirmTest: testtest",
      "quantification: testtest",
      "saveMethod: testtest"
   ]
]
}
```
