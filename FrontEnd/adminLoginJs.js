// get AJAX

function getUsername(){
    console.log('getusername')
    for(var cookie of document.cookie.split(";")){
        var splits = cookie.trim().split("=");
        if(splits[0].trim() === "username"){
            return splits[1].trim();
        }
    }
    return "guest";
}


var server_public_key;
let user = getUsername();


function getKey(){
    ajaxGetRequest("key", gotKey);
}

function gotKey(response){
    var content = JSON.parse(response);
    var pk = content['key'];
    server_public_key = forge.pki.publicKeyFromPem(pk);

}


function login(){
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    document.getElementById("username").value =  "";
    document.getElementById("password").value = "";
    let data = {"username":username,"password":password};
    let toSend = JSON.stringify(data);
    console.log(toSend)
    encryptedAjaxPostRequest('/login', toSend ,loginAttempt);
}

function loginAttempt(j_data){
    let receieved = JSON.parse(j_data);
    console.log(receieved)
    document.getElementById("message").innerHTML=receieved.message;
    if (receieved.authenticated){
        window.location.replace("controlCandidates.html")
    }
}

function votingPage() {
    window.location.replace("votingPage.html")
}




function signUp(){
    let username = getValAndClear("usernameSignup");
    let password = getValAndClear("passwordSignup");
    let accessCode = getValAndClear("accessCode")
    let data = {"username":username,"password":password,"accessCode":accessCode};
    console.log(data)
    let toSend = JSON.stringify(data);
    encryptedAjaxPostRequest("/signUp",toSend,registered);
}






function registered(jdata){
    //let message = JSON.parse(jdata);
    console.log(jdata)
    document.getElementById("message").innerHTML = jdata;
}





