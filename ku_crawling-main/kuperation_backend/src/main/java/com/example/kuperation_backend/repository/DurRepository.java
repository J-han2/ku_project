package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.Dur;
import com.example.kuperation_backend.repository.EventReadOnlyRepository;

public interface DurRepository extends EventReadOnlyRepository<Dur, String> {
    Dur findByCode(String code);
}
