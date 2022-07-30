package com.example.kuperation_backend.controller;

import com.example.kuperation_backend.domain.Testtable;
import com.example.kuperation_backend.repository.TestRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
//DB에 아직 데이터없어서 확인차
import java.util.List;
@RestController
@RequestMapping("/test")
public class testController {
    @Autowired
    TestRepository testRepository;

    @GetMapping("")//http://localhost:8080/test?name=ha 검색쿼리
    public ResponseEntity<List<Testtable>> getTesttable(@RequestParam("name") String named){
        String[] names=named.split(" ");
        List<Testtable> tt=testRepository.findByNameContains(names[0]);

        if(names.length>=2){
            tt=testRepository.findByNameLikes(names[0],names[1]);
        }

        System.out.print(names[0]);


//        for(int i=0;i<tt.size();i++){
//            System.out.println(tt.get(i).getNum()+" "+tt.get(i).getName());
//
//        }
        if (tt.size()==0)
            return ResponseEntity.notFound().build();
        return ResponseEntity.status(HttpStatus.OK).body(tt);
    }
}
