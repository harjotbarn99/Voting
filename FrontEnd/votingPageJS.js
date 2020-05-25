function getCandidatesForVoting() {
    ajaxGetRequest("/getCandidatesForVoting", makeIt)
}
var server_public_key;
let user = getUsername();
let liOfCategories = [];



function makeIt(json) {
    let dicti = JSON.parse(json);
    console.log(dicti)
    let st = "";
    for (let cat of Object.keys(dicti) ){
        liOfCategories.push(cat)
        st = st + cat + "    ";
        let candisLi = dicti[cat];
        st = st + "<select id =" + cat +">";
        st = st + "<option value='none'> Select a candidate </option>";
        for (let candi of candisLi){
            st = st + "<option value = "+candi[0].replace(/ /g,"~space~")+">"+ candi.toString() +"</option>"
        };
        st = st + "</select> <br><br>"
    }
    document.getElementById("avalibleCandidates").innerHTML = st;
    votingStatus()
}

function vote() {
    let li = [];
    let code = getValAndClear("voteCode");
    for(let c of liOfCategories){
        let voted = document.getElementById(c).value;
        li.push(voted.replace(/~space~/g," "))
    }
    let dic = {"code" : code, "li" : li};
    encryptedAjaxPostRequest("/vote",JSON.stringify(dic),display)
    votingStatus()

}

function votingStatus() {
    ajaxGetRequest("/votingStatus",displayVotingStatus)

}
function displayVotingStatus(js) {
    document.getElementById("votingStatus").innerHTML = js;
}