package com.example.kuperation_backend.repository;

import com.example.kuperation_backend.domain.Safecountry;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import com.example.kuperation_backend.repository.EventReadOnlyRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface SafeRepository extends EventReadOnlyRepository<Safecountry,Long> {
    Safecountry findByItem(String Item);
    Safecountry findByItemAndPermitDate(String item, LocalDate permitDate);
    List<Safecountry> findByItemContains(String Item);

    @Query(value="select * from safecountry WHERE MATCH (효능효과) AGAINST(:efficacy IN boolean MODE)",nativeQuery=true)
    List<Safecountry> findByEfficacyContainsFULLTEXT(@Param("efficacy")String efficacy);



    Safecountry findByInsurance(String code);

    long count();
    List<Safecountry> findByNumBetween(int startNum,int endNum);
//    @Query("select u from Safecountry u WHERE u.efficacy Like %:efficacy% or u.efficacy Like %:efficacy2%")
//    List<Safecountry> findByEfficacyFULLTEXTTwo(@Param("efficacy")String efficacy, @Param("efficacy2")String efficacy2);
//
//    @Query("select u from Safecountry u WHERE u.efficacy Like %:efficacy% or u.efficacy Like %:efficacy2% or u.efficacy Like %:efficacy3%")
//    List<Safecountry> findByEfficacyThreeLike(@Param("efficacy")String efficacy, @Param("efficacy2")String efficacy2,@Param("efficacy3")String efficacy3);

    List<Safecountry> findByInsuranceStartsWith(String insurance);
}
