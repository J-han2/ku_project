package com.example.kuperation_backend.domain;


import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDate;

@Entity
@Getter
@Setter
@Table(name="mdbook")
public class MdBook {
    @Id
    @Column(name="idx")
    private int idx;

    @Column(name="영문명")
    private String engName;

    @Column(name="한글명")
    private String korName;

    @Column(name="구성")
    private String config;

    @Column(name="성상")
    private String appearance;

    @Column(name="제법")
    private String manufacturingMethod;

    @Column(name="확인시험")
    private String confirmTest;

    @Column(name="정량법")
    private String quantification;

    @Column(name="저장법")
    private String saveMethod;

    @Column(name="갱신일")
    private LocalDate updatedDate;

}
