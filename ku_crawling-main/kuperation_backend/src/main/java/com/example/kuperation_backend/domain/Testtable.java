package com.example.kuperation_backend.domain;

import lombok.Getter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
//데이터없어서 잘 전달되는지 확인차
@Entity
@Table(name="test")
@Getter
public class Testtable {
    @Id
    private int num;

    @Column(name="name")
    private String name;
}
