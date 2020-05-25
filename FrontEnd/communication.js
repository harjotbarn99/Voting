function ajaxGetRequest(path, callback){
    let request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState===4&&this.status ===200){
            callback(this.response);
        }
    };
    request.open("GET", path);
    request.send();
}



function encrypt(message) {
    var encrypted_message = server_public_key.encrypt(message, 'RSA-OAEP');
    encrypted_message = btoa(encrypted_message);
    return encrypted_message;
}


function encryptedAjaxPostRequest(path, data, callback){
    var encryptedData = encrypt(data);
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState === 4 && this.status === 200){
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(encryptedData);
}



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


function display(jData) {
    // console.log(jData)
    document.getElementById("message").innerHTML = JSON.parse(jData);
};


function getValAndClear(id){
    let value = document.getElementById(id).value;
    document.getElementById(id).value="";
    return value;

};

function getKey(){
    ajaxGetRequest("key", gotKey);
};

function gotKey(response){
    var content = JSON.parse(response);
    var pk = content['key'];
    server_public_key = forge.pki.publicKeyFromPem(pk);

};

// part of every page
// document.getElementById("welcome").innerHTML = "hi " + user
// var server_public_key;
// let user = getUsername();
//
//
// function getKey(){
//     ajaxGetRequest("key", gotKey);
// }
//
// function gotKey(response){
//     var content = JSON.parse(response);
//     var pk = content['key'];
//     server_public_key = forge.pki.publicKeyFromPem(pk);
//
// }