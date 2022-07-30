package com.example.kuperation_backend.service;

import com.example.kuperation_backend.domain.Ingredient;
import com.example.kuperation_backend.domain.MdFee;
import com.example.kuperation_backend.domain.Safecountry;
import com.example.kuperation_backend.dto.SearchDataRes;
import com.example.kuperation_backend.dto.SearchPageDto;
import com.example.kuperation_backend.repository.IngredientRepository;
import com.example.kuperation_backend.repository.MdfeeRepository;
import com.example.kuperation_backend.repository.SafeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;


@RequiredArgsConstructor
@Service
public class SearchIngredientService {
    private final IngredientRepository ingredientRepository;
    private final MdfeeRepository mdfeeRepository;
    private final SafeRepository safeRepository;

    @Transactional
    public SearchPageDto SearchIngredient(String ingredientName,int pageNum){//
        List<SearchDataRes> result = new ArrayList<>();
        int amount=10;
        List<Ingredient> ingredientEntity = ingredientRepository.findByCommonNameContains(ingredientName);
        for (Ingredient ingredientData:ingredientEntity){//성분명이 포함된 모든 성분약효 데이터
            List<MdFee> mdfeeEntity = mdfeeRepository.findByCommonCode(ingredientData.getCommonCode());
            if(mdfeeEntity == null || mdfeeEntity.size()<1)//약효에는있는데 약가기준에는 없으면 continue
                continue;
            for(MdFee mdfeeData:mdfeeEntity){//약효와 약가기준 모두에있으면 코드 안전나라와연결
                List<Safecountry> safeEntity = safeRepository.findByInsuranceStartsWith(mdfeeData.getCode());
                if(safeEntity == null || safeEntity.size() < 1)
                    continue;
                for (Safecountry safecountryData:safeEntity){
                    SearchDataRes searchDataRes = new SearchDataRes(safecountryData, ingredientData);
                    boolean flag=true;
                    for(SearchDataRes inResult:result){
                        if(inResult.getItem().equals(searchDataRes.getItem()) && inResult.getCompany().equals(searchDataRes.getCompany())){
                            flag=false;
                            break;
                        }
                    }
                    if(flag)
                        result.add(searchDataRes);
                }
            }
        }


        int total=result.size();

        int endlist;
        if((pageNum)*10>total){//리스트값이 10개가안됨
            endlist=total;
            amount=total%10;
        }else{
        endlist=(pageNum)*10;
        }

        SearchPageDto searchPageDto=new SearchPageDto(pageNum,amount,total,result.subList((pageNum-1)*10,endlist));

        return searchPageDto;
    }

}
