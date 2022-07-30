package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.MdBook;
import com.example.kuperation_backend.repository.EventReadOnlyRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface PharmRepository extends EventReadOnlyRepository<MdBook, Integer> {
    MdBook findByEngName(String engName);

    String FIND_ENGNAME = "SELECT 영문명 FROM mdbook";

    @Query(value = FIND_ENGNAME, nativeQuery = true)
    List<String> findEngNames();
}
