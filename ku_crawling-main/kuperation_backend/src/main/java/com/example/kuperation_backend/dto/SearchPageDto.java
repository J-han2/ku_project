package com.example.kuperation_backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
public class SearchPageDto {
    private int pageNum;
    private int amount;
    private int total;

    private List<SearchDataRes> searchDataReslst;


    public SearchPageDto(int pageNum,int amount,int total,List<SearchDataRes> searchDataReslst){
        this.pageNum=pageNum;
        this.amount=amount;
        this.total=total;
        this.searchDataReslst=searchDataReslst;
    }
}
