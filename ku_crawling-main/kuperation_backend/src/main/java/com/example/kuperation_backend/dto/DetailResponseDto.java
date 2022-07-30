package com.example.kuperation_backend.dto;

import com.example.kuperation_backend.domain.*;
import lombok.Getter;

import javax.validation.constraints.NotNull;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Getter
public class DetailResponseDto {

    /* 의약품안전나라 */

    // 제품명
    @NotNull
    private String name;
    // 성상
    private String appearance;
    // 모양
    private String shape;
    // 업체명
    private String company;
    // 전문/일반
    private String speciality;
    // 허가일
    private LocalDate permitDate;
    // 마약류구분
    private String drugClassification;
    // 취소/취하구분
    private String cancelClassification;
    // 기타식별표시
    private String etc;
    // 모델명
    private String modelName;
    // 원료약품 및 분량 - 약가기준 정보가 없을 경우 대체
    private String rawGradient;
    // 효능효과
    private String efficacy;
    // 용법용량
    private String dosage;
    // 주의사항
    private String caution;
    // 저장방법
    private String store;
    // 사용기간
    private String duration;
    // 포장정보
    private String packaging;

    /* DUR */
    // 연령금기
    private String ageTaboo;

    // 임부금기
    private String pragTaboo;

    // 사용중지
    private String stopUsing;

    // 용량주의
    private String capacityWarning;

    // 투여기간주의
    private String dosingPeriodWarning;

    // 노인주의
    private String elderWarning;


    /* 의약품성분약효 */
    List<List<String>> ingreList = new ArrayList<>();


    /* 약가기준 */
    // 투여경로명
    private String dosingRoute;

    // 규격명
    private String specName;

    // 대체가능
    private String alterClassName;

    // 단위
    private String mdfeeUnit;


    /* 대한민국전자약전 */
    List<List<String>> mbList = new ArrayList<>();

    public DetailResponseDto(Safecountry safe, MdFee mdfee, Dur dur, List<Ingredient> ingredientList, List<MdBook> mdbookList) {
        if(safe != null) {
            // 제품명
            this.name = safe.getItem();
            // 성상
            this.appearance = safe.getAppearance();
            // 모양
            this.shape = safe.getShape();
            // 업체명
            this.company = safe.getCompany();
            // 전문/일반
            this.speciality = safe.getSpecialty();
            // 허가일
            this.permitDate = safe.getPermitDate();
            // 마약류구분
            this.drugClassification = safe.getDrugClassification();
            // 취소/취하구분
            this.cancelClassification = safe.getCancelClassification();
            // 기타식별표시
            this.etc = safe.getEtc();
            // 모델명
            this.modelName = safe.getModelName();
            // 원료약품및분량
            this.rawGradient = safe.getRawGredient();
            // 효능효과
            this.efficacy = safe.getEfficacy();
            // 용법용량
            this.dosage = safe.getDosage();
            // 주의사항
            this.caution = safe.getCaution();
            // 저장방법
            this.store = safe.getStore();
            // 사용기간
            this.duration = safe.getDuration();
            // 포장정보
            this.packaging = safe.getPackaging();
        }

        if(mdfee != null){
            // 투여경로명
            this.dosingRoute = mdfee.getDosingRoute();

            // 규격명
            this.specName = mdfee.getSpecName();

            // 대체가능구분명
            this.alterClassName = mdfee.getAlterClassName();

            // 단위
            this.mdfeeUnit = mdfee.getUnit();
        }

        if(dur != null){
            // 연령금기
            this.ageTaboo = dur.getAgeTaboo();

            // 임부금기
            this.pragTaboo = dur.getPragTaboo();

            // 사용중지
            this.stopUsing = dur.getStopUsing();

            // 용량주의
            this.capacityWarning = dur.getCapacityWarning();

            // 투여기간주의
            this.dosingPeriodWarning = dur.getDosingPeriodWarning();

            // 노인주의
            this.elderWarning = dur.getElderWarning();
        }

        if(ingredientList != null){
            for(Ingredient data : ingredientList){
                ingreList.add(new ArrayList<>());
                ingreList.get(ingreList.size()-1).add("commonName: " + data.getCommonName());
                ingreList.get(ingreList.size()-1).add("content: " + data.getContent());
                ingreList.get(ingreList.size()-1).add("ingredientUnit: " + data.getUnit());
            }
        }

        if(mdbookList != null) {
            for(MdBook data: mdbookList) {
                mbList.add(new ArrayList<>());
                if(data == null){
                    for(int i=0 ; i<6 ; i++)
                        mbList.get(mbList.size()-1).add("null");
                } else {
                    mbList.get(mbList.size() - 1).add("config: " + data.getConfig());
                    mbList.get(mbList.size() - 1).add("pharmAppearance: " + data.getAppearance());
                    mbList.get(mbList.size() - 1).add("manufacturingMethod: " + data.getManufacturingMethod());
                    mbList.get(mbList.size() - 1).add("confirmTest: " + data.getConfirmTest());
                    mbList.get(mbList.size() - 1).add("quantification: " + data.getQuantification());
                    mbList.get(mbList.size() - 1).add("saveMethod: " + data.getSaveMethod());
                }

            }
        }

    }
}
