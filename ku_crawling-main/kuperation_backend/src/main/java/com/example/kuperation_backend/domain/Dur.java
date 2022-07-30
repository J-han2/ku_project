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
@Table(name="durtable")
public class Dur {
    @Id
    @Column(name="약품코드")
    private String code;

    @Column(name="연령금기")
    private String ageTaboo;

    @Column(name="임부금기")
    private String pragTaboo;

    @Column(name="사용중지")
    private String stopUsing;

    @Column(name="용량주의")
    private String capacityWarning;

    @Column(name="투여기간주의")
    private String dosingPeriodWarning;

    @Column(name="노인주의")
    private String elderWarning;

}
