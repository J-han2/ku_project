const searchParams = new URL(location.href).searchParams;
const itemName = searchParams.get('itemName');
const permitDate = searchParams.get('permitDate');
console.log(itemName, permitDate);

const colName = {'name':'제품명', 'appearance': '성상', 'shape':'모양', 'company':'업체명', 'speciality':'전문/일반', 'permitDate':'허가일', 'drugClassification':'마약류구분', 'cancelClassification':'취소/취하구분', 'etc':'기타식별표시', 'modelName':'모델명', 'rawGradient':'원료약품', 'efficacy':'효능효과', 'dosage':'용법용량', 'caution':'주의사항', 'store':'저장방법', 'duration':'사용기간', 'packaging':'포장정보', 'ageTaboo':'연령금기', 'pragTaboo':'임부금기', 'stopUsing':'사용중지', 'capacityWarning':'용량주의', 'dosingPeriodWarning':'투여기간주의', 'elderWarning':'노인주의', 'ingreList':'의약품성분약효', 'dosingRoute':'투여경로명', 'specName':'규격명', 'alterClassName':'대체가능', 'mdfeeUnit':'단위', 'mbList':'전자약전' }; //29
const ingreListName = {'commonName':'성분명', 'content':'함량', 'ingredientUnit':'단위'};
const mbListName = {'config':'구성', 'pharmAppearance':'성상', 'manufacturingMethod':'제법', 'confirmTest':'확인시험', 'quantification':'정량법', 'saveMethod':'저장법'}

const basicList = ['name', 'company', 'appearance', 'shape', 'modelName', 'efficacy', 'rawGradient', 'dosage', 'specName', 'mdfeeUnit', 'dosingRoute', 'permitDate', 'cancelClassification', 'speciality', 'alterClassName', 'drugClassification', 'etc', 'store', 'duration', 'packaging'];
const cautionList = ['caution', 'ageTaboo', 'pragTaboo', 'stopUsing', 'capacityWarning', 'dosingPeriodWarning', 'elderWarning'];
const ingreList = ['ingreList', 'mbList'];

var result;
var basicTable;
var basicOpenList = [];
var ingreTableList = [];
var ingreOpenList = [];
var cautionOpenList = [];
fetch(`/detailPage/product`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
        "name": itemName,
        "permitDate": permitDate
    }),
})
.then((response) => {
    console.log("response:", response);
    return response.json();
})
.then((data)=>{
    console.log("data:", data);
    
    result = data;
    printDetail(result);

    var basic_open = document.getElementById("basic_open");
    for (var i=6; i<20; i++) {
        var tr = basicTable.children[i];
        if (tr.style.display == "") {
            basicOpenList.push(tr);
        }
    }
    basic_open.addEventListener("click", basicOpen);
    basicOpen();

    var caution_open = document.getElementById("caution_open");
    for (var p of document.getElementById("cautionTable").children[0].children[0].children[1].children) {
        cautionOpenList.push(p);
    }
    for (var i=0; i<2; i++) {
        if (cautionOpenList.length<2) break;
        cautionOpenList.shift();
    }
    caution_open.addEventListener("click", cautionOpen);
    cautionOpen();

    var ingre_open = document.getElementById("ingre_open");
    ingreTableList = document.getElementsByClassName("ingreTables");
    for (var table of ingreTableList){
        table = table.children[1];
        for (var i=2; i<8; i++) {
            var tr = table.children[i];
            if (tr.style.display == "") {
                ingreOpenList.push(tr);
            }
        }
    }
    console.log(ingreOpenList);
    ingre_open.addEventListener("click", ingreOpen);
    ingreOpen();
})
.catch((error) => {
    console.log("error:", error);
});

var div;
window.onload = () =>{
    div = document.getElementById('temp_content');
    document.getElementById("contents").style.visibility = "hidden";
    document.getElementById("footer").style.visibility = "hidden";

}

const printDetail = (data)=> {
    document.getElementById("contents").style.visibility = "visible";
    document.getElementById("footer").style.visibility = "visible";
    document.getElementById("m_name").innerText = data["name"];
    basicTable = document.getElementById("basicTable").children[0];
    var basicTrList = basicTable.getElementsByTagName("tr");
    var cautionTable = document.getElementById("cautionTable").children[0];
    var cautionTrList = cautionTable.getElementsByTagName("tr");
    var ingre = document.getElementById("ingre");
    var ingreTable = document.getElementById("ingreTable1");
    var ingreTrList = ingreTable.children[1].getElementsByTagName("tr");

    for (var key in data) {
        if (basicList.indexOf(key) != -1) {
            var keyIndex = basicList.indexOf(key);
            basicTrList[keyIndex].lastElementChild.innerHTML = data[key];
        } else if (cautionList.indexOf(key) != -1) {
            var keyIndex = cautionList.indexOf(key);
            if (keyIndex == 2) {
                if (data[key] != "" && data[key] != null) {
                    var pregList = data[key].slice(2, -2).split("', '");
                    for (var preg of pregList) {
                        var p = document.createElement("p");
                        p.innerHTML = "- "+preg;
                        cautionTrList[keyIndex].lastElementChild.appendChild(p);
                    }
                }
            } else if (keyIndex == 5) {
                if (data[key] != "" && data[key] != null) {
                    cautionTrList[keyIndex].lastElementChild.innerHTML = data[key]+"일을 초과하여 복용하면 부작용이 우려됨";
                }
            }
            else {
                cautionTrList[keyIndex].lastElementChild.innerHTML = data[key];
            }
        }
    }

    console.log(data['ingreList'].length);
    if (data['ingreList'].length == 0) {
        document.getElementById("ingre").style.display = "none";
    } else if (data['ingreList'].length == 1) {
        var contentList = [...data['ingreList'][0], ...data['mbList'][0]];
        var name = contentList.shift();
        name = name.substring(name.indexOf(": ")+2);
        document.getElementById("ingreTable1").children[0].innerHTML = "성분명 : "+name;
        for (var i=0; i<8; i++) {
            var substrIndex = contentList[i].indexOf(": ");
            if (substrIndex== -1){
                substrIndex = -2;
            }
            content = contentList[i].substring(substrIndex+2);
            if (content == "None" || content == "null") {
                ingreTrList[i].style.display = "none";
            } else {
                ingreTrList[i].lastElementChild.innerHTML = content;
            }
        }
    } else {
        for (var i=0; i<data['ingreList'].length; i++) {
            if (i!=0) {
                newIngreTable = ingreTable.cloneNode(true);
                ingre.appendChild(newIngreTable);
                newIngreTable.setAttribute("id", `ingreTable${i+1}`);
                ingreTrList = newIngreTable.children[1].getElementsByTagName("tr");
                ingreTable = newIngreTable;
            }
            var contentList = [...data['ingreList'][i], ...data['mbList'][i]];
            var name = contentList.shift();
            name = name.substring(name.indexOf(": ")+2);
            document.getElementById(`ingreTable${i+1}`).children[0].innerHTML = "성분명 : "+name;
            for (var j=0; j<8; j++) {
                var substrIndex = contentList[j].indexOf(": ");
                if (substrIndex== -1){
                    substrIndex = -2;
                }
                content = contentList[j].substring(substrIndex+2);
                if (content == "None" || content == "null") {
                    ingreTrList[j].style.display = "none";
                } else {
                    ingreTrList[j].lastElementChild.innerHTML = content;
                }
            }
        }
    }

    for (var tr of basicTrList) {
        var td = tr.lastElementChild.innerHTML;
        if (td == "" || td == null) {
            tr.style.display = "none";
        }
    }
    for (var tr of cautionTrList) {
        var td = tr.lastElementChild.innerHTML;
        if (td == "" || td == null) {
            tr.style.display = "none";
        }
    }
}

var basicOpenFlag = true;
const basicOpen = () =>{
    console.log("basicOpen 실행", basicOpenFlag);
    if (basicOpenFlag) {
        for (var tr of basicOpenList) {
            tr.style.display = "none";
        }
        document.getElementById("basic_open").children[0].setAttribute("src", "./image/plus.png");
        basicOpenFlag = false;
    } else {
        for (var tr of basicOpenList) {
            tr.style.display = "table-row";
        }
        document.getElementById("basic_open").children[0].setAttribute("src", "./image/minus.png");
        basicOpenFlag = true;
    }
}

var cautionOpenFlag = true;
const cautionOpen = ()=> {
    if (cautionOpenFlag){
        for (var tr of cautionOpenList) {
            tr.style.display = "none";
        }
        document.getElementById("caution_open").children[0].setAttribute("src", "./image/plus.png");
        cautionOpenFlag = false;
    } else {
        for (var tr of cautionOpenList) {
            tr.style.display = "block";
        }
        document.getElementById("caution_open").children[0].setAttribute("src", "./image/minus.png");
        cautionOpenFlag = true;
    }
}

var ingreOpenFlag = true;
const ingreOpen = ()=> {
    console.log("ingreOpen 실행", ingreOpenFlag);
    if (ingreOpenFlag) {
        for (var tr of ingreOpenList) {
            tr.style.display = "none";
        }
        document.getElementById("ingre_open").children[0].setAttribute("src", "./image/plus.png");
        ingreOpenFlag = false;
    } else {
        for (var tr of ingreOpenList) {
            tr.style.display = "table-row";
        }
        document.getElementById("ingre_open").children[0].setAttribute("src", "./image/minus.png");
        ingreOpenFlag = true;
    }
}