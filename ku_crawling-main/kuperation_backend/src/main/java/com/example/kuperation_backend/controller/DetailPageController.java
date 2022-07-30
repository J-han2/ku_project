package com.example.kuperation_backend.controller;

import com.example.kuperation_backend.dto.DetailResponseDto;
import com.example.kuperation_backend.service.DetailPageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

@RestController
@RequestMapping("/detailPage")
public class DetailPageController {

    private final DetailPageService detailPageService;

    @Autowired
    public DetailPageController(DetailPageService detailPageService) { this.detailPageService = detailPageService; }

    @PostMapping("/product")
    public ResponseEntity<DetailResponseDto> getDetail(@Valid @RequestBody DetailResponseDto detailDto) {
        if (detailDto.getName().equals("") || detailDto.getName().isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(detailDto);
        }

        DetailResponseDto response = detailPageService.getByItemAndPermitDate(detailDto.getName(), detailDto.getPermitDate());

        return ResponseEntity.status(HttpStatus.OK).body(response);
    }
}
