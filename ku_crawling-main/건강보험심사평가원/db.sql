use medicine;
create table MdfeeCrtrInfo (
	약품코드 varchar(10) primary key,
    품목명 varchar(400) not null,
    제조업체명 varchar(400),
    일반명코드 varchar(10),
    투여경로명 varchar(20) not null,
    규격명 varchar(400),
    단위 varchar(70),
    적용시작일자 varchar(10) not null,
    약효분류번호 varchar(5) not null,
    급여구분명 varchar(20),
    대체가능구분명 varchar(400),
    임의조제구분명 varchar(400),
    전문일반구분명 varchar(10)
);
select * from MdfeeCrtrInfo;
select 약품코드, 일반성분코드 from MdfeeCrtrInfo;
select count(*) from MdfeeCrtrInfo where 약품코드 like '0%';

-- 한방 약가목록
create table MdfeeCrtrInfo2 (
	약품코드 varchar(10) primary key,
    품목명 varchar(400) not null,
    적용시작일자 varchar(10) not null,
    투여경로명 varchar(130) not null,
    규격명 varchar(400),
    단위 varchar(70),
    개당산출단가 varchar(25),
    급여구분명 varchar(20)
);
select * from MdfeeCrtrInfo2;

-- 의약품성분약효
create table MajorCmpnNmCdList (
	idx int auto_increment primary key,
	분류명 varchar(255),
	제형구분명 varchar(30),
	일반명 varchar(255) NOT NULL,
	일반명코드 varchar(10) NOT NULL,
	투여경로명 varchar(5),
	함량내용 varchar(50) NOT NULL,
	약효분류번호 varchar(10),
	단위 varchar(100)
);
select * from MajorCmpnNmCdList order by idx;
select count(*) from MajorCmpnNmCdList;

-- DUR 의약품안전사용서비스
create table durTable (
	약품코드 varchar(10) primary key,
    일반명코드 varchar(10),
    연령금기 varchar(500),
    임부금기 varchar(1000),
    사용중지 varchar(500),
    용량주의 varchar(500),
    투여기간주의 varchar(500),
    노인주의 varchar(500)
);
select * from durTable order by 약품코드;
select count(*) from durTable where 약품코드 like '0%';
select * from durTable where 임부금기!="";
select * from durTable where 약품코드 like '6%';
select * from durTable where 약품코드='C05700031';
SELECT * FROM durTable INTO OUTFILE '\DUR.csv' FIELDS TERMINATED BY ',' enclosed by '"' LINES TERMINATED BY '\n';

-- 전자약전
create table pharmacopoeia (
	영문명 varchar(200),
	한글명 varchar(200),
    구성 varchar(1000),
    제법 varchar(500),
    성상 varchar(500),
    확인시험 text,
    정량법 text,
    저장법 varchar(100),
    primary key(영문명, 한글명)
);
select * from pharmacopoeia;
ALTER DATABASE medicine CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
ALTER TABLE pharmacopoeia CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

create table safecountry (
	idx int auto_increment not null,
    제품명 varchar(500),
    성상 varchar(500),
    모양 varchar(500),
    업체명 varchar(500),
    전문일반 varchar(20),
    허가일 varchar(20),
    품목기준코드 varchar(10),
    허가심사유형 varchar(20),
    마약류구분 varchar(20),
    취소취하구분 varchar(20),
    기타식별표시 varchar(500),
    취소취하일자 varchar(500),
    회수폐기이력 varchar(20),
    모델명 varchar(500),
    원료약품및분량 text,
    효능효과 text,
    용법용량 varchar(500),
    주의사항 text,
    저장방법 varchar(500),
    사용기간 varchar(500),
    포장정보 varchar(500),
    보험약가 varchar(500),
    ATC코드 varchar(10),
    변경이력 varchar(500)
);

-- 테이블명 전부 소문자로 변경
rename table durTable to durtable;
rename table majorcmpnnmcd to ingredient;
rename table mdfeecrtrinfo to mdfee;
rename table pharmacopoeia to mdbook;
