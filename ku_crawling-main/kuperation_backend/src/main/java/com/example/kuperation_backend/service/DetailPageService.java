package com.example.kuperation_backend.service;

import com.example.kuperation_backend.domain.*;
import com.example.kuperation_backend.dto.DetailResponseDto;
import com.example.kuperation_backend.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@RequiredArgsConstructor
@Service
public class DetailPageService {

    private final SafeRepository safeRepo;
    private final MdfeeRepository mdfeeRepo;
    private final DurRepository durRepo;
    private final IngredientRepository ingredientRepo;
    private final PharmRepository pharmRepo;

    // 약품명으로 매칭하며 각 테이블의 상세정보 가져오기
    @Transactional
    public DetailResponseDto getByItemAndPermitDate(String item, LocalDate permitDate) {
        Safecountry safe = safeRepo.findByItemAndPermitDate(item, permitDate);
        if(safe == null)
            return null;
        String code = safe.getInsurance();
        if(code.equals("") | code == "")    // 보험약가가 없을 경우 안전나라 데이터만 표시
            return new DetailResponseDto(safe, null, null, null, null);
        code = code.substring(0, 10);
        MdFee mdfee = mdfeeRepo.findByCode(code);
        // System.out.println("약가기준 code: " + code);
        // System.out.println("약가기준 일반명코드: " + mdfee.getCommonCode());
        Dur dur = durRepo.findByCode(code);
        // System.out.println("DUR code: " + code);
        String commonCode = mdfee.getCommonCode();
        List<Ingredient> ingredientList = ingredientRepo.findByCommonCode(commonCode);
        List<MdBook> mbList = new ArrayList<>();
        List<String> mdBooks = pharmRepo.findEngNames(); // 모든 전자약전 영문명 가져오기
        // System.out.println("성분약효 commonCode: " + commonCode);

        if(ingredientList.size() == 0){ // 매칭되는 성분약효 데이터가 없을 경우
            if(dur == null) // 매칭되는 dur 정보가 없을 경우
                return new DetailResponseDto(safe, mdfee, null, null, null);
            else
                return new DetailResponseDto(safe, mdfee, dur, null, null);
        } else if(ingredientList.size() != 0){  // 매칭되는 성분약효 데이터 존재
            for(Ingredient ingredient : ingredientList){
                MdBook mdbook;
                String val = ingredient.getCommonName();
                // MdBook mdBook = pharmRepo.findByEngName(val);
                List<String> ans = search(val,mdBooks);
                String fit = "";
                int minN = 9999999;
                if(ans.size() > 1) {
                    for(String i : ans) {
                        int num = match(i, val);
                        if(num < minN) {
                            minN = num;
                            fit = i;
                        }
                    }
                    System.out.println("MdBook Found : " + fit + "\n");
                    mdbook = pharmRepo.findByEngName(fit);          // 유사도 알고리즘 - 결과가 여러 개일 경우 가장 유사도가 높은 것으로 선전
                }
                else if(ans.size() == 1) {
                    System.out.println("MdBook Found : " + ans.get(0) + "\n");
                    mdbook = pharmRepo.findByEngName(ans.get(0));   // 유사도 알고리즘 - 결과가 하나일 경우 그 하나로 선정
                }
                else {
                    System.out.println("MdBook Not Found : Null\n");
                    mdbook = null;
                }
                mbList.add(mdbook); // null이면 null대로 저장되도록
            }

            if(dur == null){    // 매칭되는 dur 데이터가 없을 경우
                return new DetailResponseDto(safe, mdfee, null, ingredientList, mbList);
            } else if(dur != null) {    // 매칭되는 dur 데이터 존재
                return new DetailResponseDto(safe, mdfee, dur, ingredientList, mbList);
            }
        }
        return null;
    }

    public String KMPSearch(String pat, String txt) {
        int M = pat.length();
        int N = txt.length();
        int lps[] = new int[M];
        for(int a = 0;a<M;a++) {
            lps[a] = 0;
        }
        computeLPS(pat, lps);
        int i = 0;
        int j = 0;
        while (i < N){
            if (pat.charAt(j) == txt.charAt(i)) {
                i += 1;
                j += 1;
            }
            else if (pat.charAt(j) != txt.charAt(i)) {
                if (j != 0)
                    j = lps[j-1];
                else
                    i += 1;
            }
            if (j == M) {
                return txt;
            }
        }
        return "";
    }

    public void computeLPS(String pat, int[] lps) {
        int leng = 0;
        int i = 1;
        while(i < pat.length()) {
            if(pat.charAt(i) == pat.charAt(leng)) {
                leng += 1;
                lps[i] = leng;
                i += 1;
            }
            else {
                if(leng != 0)
                    leng = lps[leng-1];
                else {
                    lps[i] = 0;
                    i += 1;
                }
            }
        }
    }

    public ArrayList<String> search(String val, List<String> mdBooks) {
        ArrayList<String> list = new ArrayList<String>();
        boolean flag = true;
        String[] sp = val.split(" ");
        for(String pat : sp) {
            if(pat == "")
                continue;
            if(flag) {
                for (String txt : mdBooks) {
                    String text = KMPSearch(pat, txt);
                    if(text.compareTo("") != 0)
                        list.add(text);
                }
                if(list.size() == 0)
                    continue;
                flag = false;
            }
            else {
                ArrayList<String> temp = new ArrayList<>(list);
                list.clear();
                for(String txt : temp) {
                    String text = KMPSearch(pat, txt);
                    if(text.compareTo("") != 0) {
                        list.add(text);
                    }
                }
                if(list.size() == 0)
                    return temp;

            }
        }
        return list;
    }

    public int match(String str1, String str2) {
        int n = str1.length();
        int m = str2.length();
        int[][] dp = new int[n + 1][m + 1];
        for(int i = 1; i < n+1; i++)
            dp[i][0] = i;
        for(int j = 1; j < m+1; j++)
            dp[0][j] = j;
        for(int i = 1; i < n+1; i++) {
            for(int j = 1; j < m+1; j++) {
                if(str1.charAt(i - 1) == str2.charAt(j - 1))
                    dp[i][j] = dp[i - 1][j - 1];
                else
                    dp[i][j] = min(dp[i][j - 1], dp[i - 1][j - 1], dp[i - 1][j]) + 1;
            }
        }
        return dp[n][m];
    }

    public int min(int i, int j, int k) {
        int temp = i < j ? i : j;
        return temp < k ? temp : k;
    }

}
