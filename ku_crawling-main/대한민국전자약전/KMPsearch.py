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


df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')
df = pd.read_csv('data.csv', encoding='cp949')
data1 = df1['영문명'].str.lower()
data2 = df2['영문명'].str.lower()
data = df['일반명'].str.lower()


count = 0
for val in data.values:
    ans = search(val)
    print(val, ans)
    if len(ans) >= 1:
        count+=1

print("총 ", len(data), "개의 data 중, ", count, "개의 data가 매칭")
