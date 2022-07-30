package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.Testtable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TestRepository extends EventReadOnlyRepository<Testtable,Long>{

    //List<Testtable> findByNameContains(String name,String name2);//Select * from test where name Like '%ha%'

    List<Testtable> findByNameContains(String name);

    @Query("select u from Testtable u WHERE u.name Like %:name% or u.name Like %:name2%")
    List<Testtable> findByNameLikes(@Param("name")String name,@Param("name2")String name2);
}
