window.onload = function () {
    var guide = document.getElementById("guide");
    guide.onclick = showTip;
    var search_btn = document.getElementById("search_btn");
    search_btn.onclick = search;
}

var tipOpen = false;
function showTip(){
    var guide = document.getElementById("guide");
    if(!tipOpen){
        guide.innerHTML = 
        "<p>검색 방법</p>"+
        "<p>1. 약품 검색<br>&nbsp&nbsp&nbspa. 현재 아픈 증상(복통, 두통 등)을 간결하게 검색한다.<br>&nbsp&nbsp&nbspb. 궁금한 효능/효과를 검색한다.</p>"+
        "<p>2. 약품 검색<br>&nbsp&nbsp&nbspa. 궁금한 약품명을 검색한다.<br>&nbsp&nbsp&nbspb. 궁금한 성분명을 검색한다.</p>";
        guide.style.textAlign = "left";
        guide.style.textDecoration ="none";
        guide.style.color = "black";
        guide.style.fontSize = "15px";
        tipOpen = true;
    }
    else {
        guide.innerHTML = "검색 방법(클릭)";
        guide.style.textAlign = "center";
        guide.style.textDecoration ="underline";
        guide.style.color = "gray";
        guide.style.fontSize = "12px";
        tipOpen = false;
    }
}

function search(){
    var input = document.getElementById("search_input").value;
    var select = document.getElementById("category");
    var category = select.options[select.selectedIndex].text; //text값으로 param 넘김. index값으로 넘기려면 .value로 수정
    var url = "search.html?category=" + category + "&input=" + input;
    document.location.href=url;
}

function enter(){ //검색창에서 엔터키 눌렀을 때 처리
    if(window.event.keyCode == 13){
        search()
    }
}