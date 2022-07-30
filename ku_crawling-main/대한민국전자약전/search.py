import pandas as pd


def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
    lps = [0]*M
    computeLPS(pat, lps)
    i = 0
    j = 0
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
        elif pat[j] != txt[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
        if j == M:
            return txt

def computeLPS(pat, lps):
    leng = 0
    i = 1
    while i < len(pat):
        if pat[i] == pat[leng]:
            leng += 1
            lps[i] = leng
            i += 1
        else:
            if leng != 0:
                leng = lps[leng-1]
            else:
                lps[i] = 0
                i += 1


def search(val):
    list = []
    flag = True
    sp = val.split(' ')
    for pat in sp:
        if pat == '':
            continue
        if flag:
            for txt in data1.values:
                text = KMPSearch(str(pat), str(txt))
                if text is not None:
                    list.append(text)
            for txt in data2.values:
                text = KMPSearch(str(pat), str(txt))
                if text is not None:
                    list.append(text)
            if len(list) == 0:
                continue
            flag = False
        else:
            temp = list
            list = []
            for txt in temp:
                text = KMPSearch(str(pat), str(txt))
                if text is not None:
                    list.append(text)
            if len(list) == 0:
                return temp
    return list


def match(str1, str2):
    n = len(str1)
    m = len(str2)
    dp = [[0] * (1 + m) for _ in range(1 + n)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i][j - 1], dp[i - 1][j - 1], dp[i - 1][j]) + 1
    return dp[n][m]


df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')
df = pd.read_csv('data.csv', encoding='cp949')
data1 = df1['영문명'].str.lower()
data2 = df2['영문명'].str.lower()
data = df['일반명'].str.lower()
data3 = df['제형구분명']


'''list1 = []
for i in data3.values:
    temp = i.split(',')
    for j in temp:
        if j not in list1:
            list1.append(j)
for i in list1:
    print(i)'''

count = 0
for val in data.values:
    ans = search(val)
    fit = ""
    minN = 9999999
    if len(ans) > 1:
        for i in ans:
            num = match(i, val)
            if num < minN:
                minN = num
                fit = i
        print(val, ":", fit)
        count += 1
    elif len(ans) == 1:
        print(val, ":", ans[0])
        count += 1
    else:
        print(val, ":", "No Match")
print("총 ", len(data), "개의 data 중, ", count, "개의 data가 매칭")
