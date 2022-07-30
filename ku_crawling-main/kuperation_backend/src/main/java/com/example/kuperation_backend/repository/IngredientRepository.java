package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.Ingredient;
import com.example.kuperation_backend.repository.EventReadOnlyRepository;

import java.util.List;

public interface IngredientRepository extends EventReadOnlyRepository<Ingredient, Integer> {
    List<Ingredient> findByCommonCode(String code);
    List<Ingredient> findByCommonNameContains(String ingredientName);
}
