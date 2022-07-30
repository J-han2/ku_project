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
@Table(name="ingredient")
public class Ingredient {
    @Id
    @Column(name="idx")
    private int num;

    @Column(name="분류명")
    private String className;

    @Column(name="제형구분명")
    private String typeClassName;

    @Column(name="일반명")
    private String commonName;

    @Column(name="일반명코드")
    private String commonCode;

    @Column(name="투여경로명")
    private String dosingRoute;

    @Column(name="함량내용")
    private String content;

    @Column(name="약효분류번호")
    private String classNum;

    @Column(name="단위")
    private String unit;

}
