var server_public_key;

let user = getUsername();
let welc = "welcome " + user;
console.log(welc);

function di(){
    console.log("di ")
    document.getElementById("message1").innerHTML = welc;
}
function controlCandidates() {
    window.location.replace("controlCandidates.html")
}


function makeVoteCodes(){
    let no = getValAndClear("numberOfVoteCodes");
    encryptedAjaxPostRequest("/makeVoteCodes",JSON.stringify(no),display)
    getVoteCodes()
}

function getVoteCodes(){
    ajaxGetRequest("/sendVoteCodes",displayVotiCodes)
}

function displayVotiCodes(Jdata) {
    // console.log(Jdata)
    let li = JSON.parse(Jdata);
    let st = ""
    for (i = 0; i < li.length ; i++){

        st += li[i] + "<br><br>"
    }
     console.log(st);
    document.getElementById("voteCodes").innerHTML = st;

}

function deleteAllVoteCodes() {
    ajaxGetRequest("/deleteAllVoteCodes",display)
    getVoteCodes()
}

function deleteVoteCode() {
    let code = getValAndClear("voteCodeToDelete");
    encryptedAjaxPostRequest("/deleteVoteCode",JSON.stringify(code),display)
    getVoteCodes()
}

