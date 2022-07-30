
const searchParams = new URL(location.href).searchParams;
var category = searchParams.get('category');
const pageNum = parseInt(searchParams.get('pageNum'));
const word = searchParams.get('word');
console.log(category, pageNum, word);

var cate_text = "";
var totalPage;

var paramName = "";
if (category=="item"){ paramName = "itemName"; cate_text="약품명"; }
else if (category=="ingredient") { paramName = "ingredientName"; cate_text="성분"; }
else if (category=="symptom") { paramName = "symptom"; cate_text="증상"; }

var fetchurl;
var innerTitleText;
if (word=="" || category=="allitem") {
    category = "allitem";
    fetchurl = `/search/allitem?pageNum=${pageNum}`;
    innerTitleText = `모든 약품 검색 결과`;
} else {
    fetchurl = `/search/${category}?${paramName}=${word}&pageNum=${pageNum}`;
    innerTitleText = `"${word}" 에 대한 ${cate_text} 검색 결과`;
}

var result;
fetch(fetchurl, {method: "GET"})
.then((response) => {
    console.log("response:", response);
    return response.json();
})
.then((data)=>{
    console.log("data:", data);
    
    result = data;
    printList(result);
})
.catch((error) => {
    console.log("error:", error);
});

var table;
var input;
var total;
window.onload = ()=> {
    table = document.getElementById("tBody");
    input = document.getElementById("input");
    total = document.getElementById("total");
    document.getElementById("contents").style.visibility ='hidden';
    document.getElementById("footer").style.visibility = "hidden";
    // printList(result);
}

function printList(data) {
    document.getElementById("contents").style.visibility = 'visible';
    document.getElementById("footer").style.visibility = "visible";
    input.innerText = innerTitleText;

    total.innerText = data.total;
    totalPage = Math.ceil(data.total/10);
    console.log("totalPage: ", totalPage);

    var itemList = data.searchDataReslst;
    for(var i=0; i<itemList.length; i++) {
        var item = itemList[i];
        console.log(item)
        var tr = document.createElement("tr");
        var td = document.createElement("td");
        td.innerText = i+1 + (pageNum-1)*10;
        tr.appendChild(td);

        var td = document.createElement("td");
        var a = document.createElement("a");
        a.setAttribute("href", `/detail?itemName=${item["item"]}&permitDate=${item["permitDate"]}`);
        a.setAttribute("target", " _blank");
        a.innerText = item["item"];
        td.appendChild(a);
        tr.appendChild(td);

        var td = document.createElement("td");
        td.innerText = item["company"];
        tr.appendChild(td);

        var td = document.createElement("td");
        var ingred = item["ingredient"];
        ingred = ingred.trim()
        ingred = ingred.replace("유효성분 : ", "");
        if (ingred=="") {
            ingred = "성분 없음"
        }
        td.innerText = ingred;
        tr.appendChild(td);

        //효능/효과 출력 처리
        var td = document.createElement("td");
        var efficacy = item["efficacy"];
        if (category=="symptom") {
            var sympList = word.split(" ");
            console.log(sympList);
            var symp = sympList[0];
            var sympIdx = efficacy.indexOf(symp);
            var start = efficacy.lastIndexOf(">", sympIdx);
            var end = efficacy.indexOf("<", sympIdx);
            efficacy = efficacy.substring(start+1, end);

            for (symptom of sympList) {
                sympIdx = efficacy.indexOf(symptom);
                console.log(symptom, sympIdx);
                if (sympIdx > -1) {
                    efficacy = efficacy.substring(0, sympIdx+symptom.length) + "</strong>" + efficacy.substring(sympIdx+symptom.length);
                    efficacy = efficacy.substring(0, sympIdx) + "<strong>" + efficacy.substring(sympIdx);
                }
            }
        } else {
            efficacy = efficacy.substring(0,200);
            for (var j=0; j<10; j++) {
                var start = efficacy.indexOf("<");
                if (start<0) { break; }
                var end = efficacy.indexOf(">");
                efficacy = efficacy.substring(0, start) + efficacy.substring(end+1);
    
                efficacy = efficacy.replace("</p><div>", " ");
                efficacy = efficacy.replace("</p><p", ", <p");
            }
        }
        if (efficacy.search(/[-･○]/)==0) {
            efficacy = efficacy.substring(1);
        }
        
        td.innerHTML = efficacy;
        tr.appendChild(td);
        table.appendChild(tr);
    }

    // 총 데이터 개수에 따른 pagenation
    if (totalPage==0){
        var tr = document.createElement("tr");
        var td = document.createElement("td");
        td.setAttribute("colspan", "5");
        td.innerHTML = `검색 결과가 없습니다`;
        tr.appendChild(td);
        table.appendChild(tr);

    } else {
        // 이전/다음/처음/마지막 페이지 버튼
        document.getElementById("pageNow").childNodes[0].innerText = pageNum;
        var last = document.getElementById("pageLast").childNodes[1];
        console.log("last: ", last);
        last.setAttribute("href", `/searchList?category=${category}&pageNum=${totalPage}&word=${word}`);
        document.getElementById("pageFirst").childNodes[1].setAttribute("href", `/searchList?category=${category}&pageNum=1&word=${word}`);
        if (pageNum!=1) {
            document.getElementById("pagePrev").childNodes[0].setAttribute("href", `/searchList?category=${category}&pageNum=${pageNum-1}&word=${word}`);
        }
        if (pageNum != totalPage) {
            document.getElementById("pageNext").childNodes[0].setAttribute("href", `/searchList?category=${category}&pageNum=${pageNum+1}&word=${word}`);
        }
        for (var i=1; i<=3; i++) {
            if (pageNum-i<1) {
                break;
            }
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = `/searchList?category=${category}&pageNum=${pageNum-i}&word=${word}`;
            a.innerText = pageNum-i;
            li.appendChild(a);

            var pagePrev = document.getElementById("pagePrev");
            pagePrev.insertAdjacentElement('afterend', li);
        }

        console.log(pageNum, totalPage)
        for (var i=1; i<=3; i++){
            if (pageNum+i>totalPage) {
                break;
            }
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.href = `/searchList?category=${category}&pageNum=${pageNum+i}&word=${word}`;
            a.innerText = pageNum+i;
            li.appendChild(a);

            var pageNext = document.getElementById("pageNext");
            pageNext.insertAdjacentElement('beforebegin', li);
        }
    }

}