package search;

import java.util.ArrayList;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class testMain {
    public static ArrayList<String> list1= new ArrayList<String>();
    public static ArrayList<String> list2= new ArrayList<String>();
	
	public static String KMPSearch(String pat, String txt) {
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
	
	public static void computeLPS(String pat, int[] lps) {
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
	
	public static ArrayList<String> search(String val) {
		ArrayList<String> list = new ArrayList<String>();
	    boolean flag = true;
	    String[] sp = val.split(" ");
	    for(String pat : sp) {
	        if(pat == "")
	            continue;
	        if(flag) {
	            for (String txt : list1) {
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
	
	public static int match(String str1, String str2) {
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

	public static int min(int i, int j, int k) {
		int temp = i < j ? i : j;
		return temp < k ? temp : k;
	}

	public static void main(String[] args) {
		String db_hostname = "49.50.175.105";
        int db_portnumber = 3306;
        String db_database = "kuperation";
        String db_charset = "utf-8";
        String db_username = "kuperation";
        String db_password = "kuperation2022^^";

        Connection conn = null;

        String urlFormat = "jdbc:mysql://%s:%d/%s?characterEncoding=%s&serverTimezone=UTC";
        String url = String.format(urlFormat, db_hostname, db_portnumber, db_database, db_charset);

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");

            conn = DriverManager.getConnection(url, db_username, db_password);

            // 성공시 메시지 출력
            System.out.println("=== DATABASE Connerct Success ===");
            try {
	            String sql = "select 영문명 from mdbook";
	            PreparedStatement ps = conn.prepareStatement(sql);
	            ResultSet rs = ps.executeQuery();
	            while(rs.next()) {
	            	String temp = rs.getString("영문명").toLowerCase();
	            	list1.add(temp);
	            }
	            sql = "select 일반명 from ingredient";
	            ps = conn.prepareStatement(sql);
	            rs = ps.executeQuery();
	            while(rs.next()) {
	            	String temp = rs.getString("일반명").toLowerCase();
	            	list2.add(temp);
	            }
            }catch(SQLException e) {
            	e.printStackTrace();
            }
            int count = 0;
            for(String val : list2) {
            	ArrayList<String> ans = search(val);
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
                	System.out.println(val + " : " + fit);
                    count += 1;
                }
                else if(ans.size() == 1) {
                	System.out.println(val + " : " + ans.get(0));
                    count += 1;
                }
                else
                	System.out.println(val + " : " + "No Match");
            }
            System.out.println("총 " + list2.size() + "개의 data 중, " + count + "개의 data가 매칭");
        } catch (ClassNotFoundException e) {
            System.out.println("=== DATABASE Connerct Fail ===");
            System.out.println(e.getMessage());

        } catch (SQLException e) {
            System.out.println("=== DATABASE Connect Fail ===");
            System.out.println(e.getMessage());
        }

        try {
            conn.close();
            System.out.println(" === DATABASE Disconnect Success ===");
        } catch (Exception e) {
            System.out.println(" === DATABASE Disconnect Fail ===");
            System.out.println(e.getMessage());
        }
        conn =null;
	}

}
