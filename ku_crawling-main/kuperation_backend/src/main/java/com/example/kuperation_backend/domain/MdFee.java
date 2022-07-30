package com.example.kuperation_backend.domain;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Getter
@Setter
@Table(name="mdfee")
public class MdFee {
    @Id
    @Column(name="약품코드")
    private String code;

    @Column(name="품목명")
    private String itemName;

    @Column(name="제조업체명")
    private String manuName;

    @Column(name="일반명코드")
    private String commonCode;

    @Column(name="투여경로명")
    private String dosingRoute;

    @Column(name="규격명")
    private String specName;

    @Column(name="단위")
    private String unit;

    @Column(name="적용시작일자")
    private String applyStartDate;

    @Column(name="약효분류번호")
    private String drugClassNum;

    @Column(name="급여구분명")
    private String wageClassName;

    @Column(name="대체가능구분명")
    private String alterClassName;

    @Column(name="임의조제구분명")
    private String arbitaryPrepareClassName;

    @Column(name="전문일반구분명")
    private String expertCommonClassName;

}
