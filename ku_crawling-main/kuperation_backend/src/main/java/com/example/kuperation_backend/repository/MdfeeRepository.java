package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.MdFee;
import com.example.kuperation_backend.repository.EventReadOnlyRepository;

import java.util.List;

public interface MdfeeRepository extends EventReadOnlyRepository<MdFee, String> {
    MdFee findByCode(String code);

    List<MdFee> findByCommonCode(String commonCode);
}
