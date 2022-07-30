function getURLParams(url) {
    var result = {};
    url.replace(/[?&]{1}([^=&#]+)=([^&#]*)/g, function(s, k, v) { result[k] = decodeURIComponent(v); });
    return result;
}

var params = getURLParams(location.search);//url 파싱해서 parameter 추출

window.onload = function () {
    //alert 나중에 주석처리 해 주세요
    window.alert("카테고리 : " + params["category"] +"\n입력값 : "+ params["input"]);
    //params["category"], params["input"]으로 가져다 쓸 수 있습니다! 

    var input = document.getElementById("input");
    var input_text = params["input"];
    if(input_text == "") //input이 비어있는 경우 모든 약품에 대한 결과 보여줌
        input_text = "모든 약품";

    input.innerText = input_text + "에 대한 " + params["category"] + " 검색 결과"; //patameter 값에 따라 텍스트 삽입.

    var all = document.getElementById("all");
    all.onclick = showAll;
    var results = document.getElementsByClassName("result");
    for(var i=0; i<results.length; i++){
        results.item(i).onclick = trClick;
    }
}

function showAll(){
    var url = "search.html?category=" + params["category"] + "&input=";
    document.location.href=url;
}



function trClick(){
    var name = this.cells[1].innerHTML
    var company = this.cells[2].innerHTML
    var ingredient = this.cells[3].innerHTML
    var effect = this.cells[4].innerHTML
    var url = "detail.html?category=" + "&name=" + name + "&company=" + company + "&ingredient=" + ingredient + "&effect=" + effect;
    document.location.href=url;
}