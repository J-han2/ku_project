package com.example.kuperation_backend.domain;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.time.LocalDate;

@Entity
@Getter
@Setter
@Table(name="safecountry")
public class Safecountry {
    @Id
    @Column(name="idx")
    private int num;

    @Column(name="제품명")
    private String item;//제품명

    @Column(name="성상")
    private String appearance;//성상

    @Column(name="모양")
    private String shape;//모양

    @Column(name="업체명")
    private String company;//제조회사

    @Column(name="전문일반")
    private String specialty;//전문/일반

    @Column(name="허가일")
    private LocalDate permitDate; //허가일

    @Column(name="품목기준코드")
    private String codeByItem;///품목기준 코드

    @Column(name="허가심사유형")
    private String permissionExamType;//허가심사유형

    @Column(name="마약류구분")
    private String drugClassification;//마약류 구분

    @Column(name="취소취하구분")
    private String cancelClassification;//취소취하 구분

    @Column(name="기타식별표시")
    private String etc;//기타식별 표시

    @Column(name="취소취하일자")
    private String cancelDate;//취소취하일자

    @Column(name="회수폐기이력")
    private String disuseHistory;//회수 폐기이력

    @Column(name="모델명")
    private String modelName;//모델명

    @Column(name="원료약품및분량")
    private String rawGredient;//원료약품 및 분량

    @Column(name="효능효과")
    private String efficacy;//효능효과

    @Column(name="용법용량")
    private String dosage;//용법용량

    @Column(name="주의사항")
    private String caution;//주의사항

    @Column(name="저장방법")
    private String store;//저장방법

    @Column(name="사용기간")
    private String duration;//사용기간

    @Column(name="포장정보")
    private String packaging;//포장정보

    @Column(name="보험약가")
    private String insurance;//보험약가

    @Column(name="ATC코드")
    private String atcCode;//ATC코드

    @Column(name="변경이력")
    private String changedHistory;//변경이력


}
