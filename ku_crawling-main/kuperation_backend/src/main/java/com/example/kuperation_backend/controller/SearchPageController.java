package com.example.kuperation_backend.controller;

import com.example.kuperation_backend.dto.SearchDataRes;
import com.example.kuperation_backend.dto.SearchPageDto;
import com.example.kuperation_backend.service.SearchIngredientService;
import com.example.kuperation_backend.service.SearchPageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/search")
public class SearchPageController {
    private final SearchPageService searchPageService;
    private final SearchIngredientService searchIngredientService;

    @Autowired
    public SearchPageController(SearchPageService searchPageService,SearchIngredientService searchIngredientService) {
        this.searchPageService = searchPageService;
        this.searchIngredientService = searchIngredientService;
    }

@GetMapping("/allitem")
SearchPageDto searchAll(@RequestParam("pageNum") int pageNum){
    SearchPageDto searchPageDto = searchPageService.searchAll(pageNum);//
//        if(searchPageDto.getSearchDataReslst().size()>=1)
//            return ResponseEntity.ok().body(searchPageDto);//값 존재시 list 전달
//
//        return ResponseEntity.notFound().build();//전달값이 없을때
    //System.out.println(searchPageDto);
    return searchPageDto;
}


//성분검색
    @GetMapping("/ingredient")//,
    SearchPageDto searchIngredient(@RequestParam("ingredientName") String ingredientName,@RequestParam("pageNum") int pageNum){
        SearchPageDto searchPageDto = searchIngredientService.SearchIngredient(ingredientName,pageNum);//
//        if(searchPageDto.getSearchDataReslst().size()>=1)
//            return ResponseEntity.ok().body(searchPageDto);//값 존재시 list 전달
//
//        return ResponseEntity.notFound().build();//전달값이 없을때
        System.out.println(searchPageDto);
        return searchPageDto;
    }


//약품명 검색
    @GetMapping("/item")
    SearchPageDto getitemResult(@RequestParam("itemName") String itemName,@RequestParam("pageNum") int pageNum){

    SearchPageDto searchPageDto=searchPageService.findByItemByPage(itemName, pageNum);



    return searchPageDto;//전달값이 없을때
}

///증상검색
    @GetMapping("/symptom")
    SearchPageDto getsymptomResult(@RequestParam("symptom") String symptom,@RequestParam("pageNum") int pageNum){

        SearchPageDto searchPageDto=searchPageService.findBySymptomByPage(symptom, pageNum);



        return searchPageDto;//전달값이 없을때
    }
}
