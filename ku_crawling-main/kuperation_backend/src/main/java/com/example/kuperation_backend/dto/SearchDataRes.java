package com.example.kuperation_backend.dto;

import com.example.kuperation_backend.domain.Ingredient;
import com.example.kuperation_backend.domain.Safecountry;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

//의약품 검색후 나타나는창에 넣어줄 데이터를 dto로 관리
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchDataRes {
    private String item;
    private String company;
    private String ingredient;
    private String efficacy;
    private LocalDate permitDate;

    public SearchDataRes(Safecountry entity) {
        this.item = entity.getItem();
        this.company = entity.getCompany();
        this.ingredient = entity.getRawGredient();
        this.efficacy = entity.getEfficacy();
        this.permitDate=entity.getPermitDate();
    }

    public SearchDataRes(Safecountry safeEntity, Ingredient ingEntity){
        this.item = safeEntity.getItem();
        this.company = safeEntity.getCompany();
        this.ingredient = ingEntity.getCommonName();
        this.efficacy = safeEntity.getEfficacy();
        this.permitDate=safeEntity.getPermitDate();
    }
}
