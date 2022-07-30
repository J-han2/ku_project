package com.example.kuperation_backend.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
public class HomeController {


    @RequestMapping("/detail")
    public String detailPage(){
        return "detail.html";
    }

    @RequestMapping("/searchList")
    public String searchPage(){
        return "list.html";
    }
}
