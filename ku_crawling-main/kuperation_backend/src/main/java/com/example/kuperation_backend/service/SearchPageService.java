package com.example.kuperation_backend.service;

import com.example.kuperation_backend.domain.Safecountry;
import com.example.kuperation_backend.dto.SearchDataRes;
import com.example.kuperation_backend.dto.SearchPageDto;
import com.example.kuperation_backend.repository.SafeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.server.DelegatingServerHttpResponse;
import org.springframework.stereotype.Service;


import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Service
public class SearchPageService {

    private final SafeRepository safeRepository;

    public SearchPageDto searchAll( int pageNum){
        int amount=10;
        int endlist;

        long ts=safeRepository.count();

        int total=(int)ts;


        if((pageNum)*10>total){//리스트값이 10개가안됨
            endlist=total;
            amount=total%10;
        }else{
            endlist=(pageNum)*10;
        }

        List<Safecountry> sc=safeRepository.findByNumBetween((pageNum-1)*10,endlist);
        if (pageNum!=1)
            sc=safeRepository.findByNumBetween((pageNum-1)*10+1,endlist);



        List<SearchDataRes> result= sc.stream().map(SearchDataRes::new).collect(Collectors.toList());
        System.out.println((pageNum-1)*10+" "+endlist);
        amount=result.size();



        SearchPageDto searchPageDto=new SearchPageDto(pageNum,amount,total,result);

        return searchPageDto;

    }


/////약품명 검색///////
    public SearchPageDto findByItemByPage(String item, int pageNum){
        int amount=10;
        List<Safecountry> sc=safeRepository.findByItemContains(item);

        List<SearchDataRes> result= sc.stream().map(SearchDataRes::new).collect(Collectors.toList());
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


//////증상명검색
    public SearchPageDto findBySymptomByPage(String symptom, int pageNum){

        int amount=10;


        String[] symptoms=symptom.split(" ");
        String str="";
        for(int i=0;i<symptoms.length;i++){//공백추가
            if (i==0)
            str=str+"+"+symptoms[i];
            else
                str=str+" +"+symptoms[i];
        }

        List<Safecountry> sc=safeRepository.findByEfficacyContainsFULLTEXT(str);


        List<SearchDataRes> result= sc.stream().map(SearchDataRes::new).collect(Collectors.toList());

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
