var server_public_key;
let user = getUsername();
let welc = "welcome " + user;
console.log(welc);


function di(){
    console.log("di ");
    document.getElementById("message1").innerHTML = welc;
}




function controlVoters() {
    window.location.replace("controlVoters.html")
}

function candidateRegister() {
    let category = radioCategory("candidateCategory");
    let name = getValAndClear("candidateName");
    let venture = getValAndClear("candidateVenture");
    let ventureDetails = getValAndClear("candidateVentureDetails");
    let dic = {"category": category , "name":name , "venture" : venture, "ventureDetails": ventureDetails};
    console.log(dic);
    encryptedAjaxPostRequest("/rigisterCandidate",JSON.stringify(dic),display);
    getCandidates()
}

function radioCategory() {
    let val = "";
    const nameRadio =  ["Social","General","Technology"]
    for ( let one of nameRadio){
        one = document.getElementById(one);
        if ( one.checked){
            console.log(one.value);
            val = one.value;
            break;
        }
    }
    return val
}


function getCandidates() {
    console.log("getcandidates ");
    ajaxGetRequest("/sendCandidates",gotCandidates)
}

function gotCandidates(Jdata) {
    liOfLi = JSON.parse(Jdata);
    let Final = "";
    for (let li of liOfLi){
        let Sli = li.toString(li);
        Final = Final + Sli + "<br>"
    }
    console.log(Final);
    document.getElementById("candidates").innerHTML = Final;
}

function deleteCandidates() {
    let nameVen = getValAndClear("deleteName");
    encryptedAjaxPostRequest("/deleteCandidate",JSON.stringify(nameVen),display);
    getCandidates()

}

function votingStatus() {
    ajaxGetRequest("/votingStatus",displayVotingStatus)

}
function displayVotingStatus(js) {
    document.getElementById("votingStatus").innerHTML = js;
}
function changeVotingStatus() {
    ajaxGetRequest("/changeVotingStatus",display);
    votingStatus()
}

function votesZero() {
    ajaxGetRequest("/makeVotesZero",display);
    getCandidates()
}

function getSortedCandidates() {
        ajaxGetRequest("/sendSortedCandidates",sortedCandidatesDisplay)
}


function sortedCandidatesDisplay(json) {
    let dicti = JSON.parse(json);
    console.log(dicti)
    let st = "";
    for (let cat of Object.keys(dicti) ){
        st = st + cat + "    <br>";
        let candisLi = dicti[cat];
        for (let candi of candisLi){
            st = st + candi.toString()  + "<br>"
        };
        st = st + " <br><br>"
    }
    document.getElementById("sortedCandidates").innerHTML = st;
}

function deleteAllCandidates() {
    ajaxGetRequest("/deleteAllCandidates",display)
    getCandidates()
}
