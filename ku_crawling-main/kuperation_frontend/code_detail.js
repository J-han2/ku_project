function getURLParams(url) {
    var result = {};
    url.replace(/[?&]{1}([^=&#]+)=([^&#]*)/g, function(s, k, v) { result[k] = decodeURIComponent(v); });
    return result;
}

var params = getURLParams(location.search);//url 파싱해서 parameter 추출

window.onload = function () {
    //alert 나중에 주석처리 해 주세요
    //window.alert("약품명 : " + params["name"] +"\n제조회사 : "+ params["company"] + 
                //"\n성분 : " + params["ingredient"] +"\n효능 효과 : "+ params["effect"]);
    //params["태그 이름"]으로 가져다 쓸 수 있습니다! 
    var back = document.getElementById("back");
    back.onclick = showList;
    document.getElementById("m_name").innerHTML = params["name"];
    document.getElementById("basic").getElementsByClassName("info_contents")[0].innerHTML = 
    "<p>제조 회사 : " + params["company"] + "</p>" + 
    "<p>성분 : " + params["ingredient"] + "</p>" + 
    "<p>효능/효과 : " + params["effect"] + "</p>";
}

function showList(){
    window.history.back();
}