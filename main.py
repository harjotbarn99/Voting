import bottle
import json
import p_database as db
import eventlet
import eventlet.wsgi
import help
import p_authentication as ath
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode


def get_cypher(key_filename):
    with open(key_filename) as f:
        data = f.read()
    key = RSA.importKey(data,"Barn1999")
    cipher = PKCS1_OAEP.new(key)
    return cipher

cipher = get_cypher("pemFiles/private-attend-app.pem")
cipher_verify = get_cypher("pemFiles/private-attend-app-token.pem")
cipher_sign = get_cypher("pemFiles/public-attend-app-token.pem")


def decryptt(cyphertext, verify=False):
    content = b64decode(cyphertext)
    if verify:
        content = cipher_verify.decrypt(content).decode()
    else:
        content = cipher.decrypt(content).decode()
    return content

def sign(text):
    cyphertext = cipher_sign.encrypt(text.encode())
    cyphertext = b64encode(cyphertext).decode()
    return cyphertext

def get_username():
    username = bottle.request.get_cookie("token")
    if not username:
        return None
    return decryptt(username, True)



#  requestes for communication ( admin )

@bottle.post("/login")
def loginAttempt():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    loginDetails=json.loads(content)
    # print(loginDetails)
    message = ath.authenticate(loginDetails)
    if message['authenticated']:
        bottle.response.set_cookie("username", loginDetails["username"])
        bottle.response.set_cookie("token", sign(loginDetails["username"]))
    return json.dumps(message)

@bottle.post("/signUp")
def reg():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    # print(cred)
    message = ath.add_user(cred)
    return message

@bottle.post("/rigisterCandidate")
def RC():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        # print(cred)
        data  = db.addCandidate(cred)
        return json.dumps(data)
    return json.dumps("problem with authentication")

@bottle.route("/makeVotesZero")
def mvz():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        liOfLi = db.clearAllVotes()
        # print(liOfLi)
        return json.dumps(liOfLi)
    return json.dumps("problem setting votes to zero")

@bottle.route("/sendCandidates")
def sc():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        print("sending candidates")
        liOfLi = db.allCandidates()
        # print(liOfLi)
        return json.dumps(liOfLi)
    return json.dumps("problem sending candidates")

@bottle.route("/sendSortedCandidates")
def ssc():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        print("sending sorted candidates")
        dict = db.sortedCandidates()
        # print(liOfLi)
        return json.dumps(dict)
    return json.dumps("problem sending sorted candidates")

@bottle.post("/deleteCandidate")
def DC():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        # print("delete " + cred )
        data  = db.deleteCandidate(cred)
        return json.dumps(data)
    return json.dumps("problem with authentication")

@bottle.route("/deleteAllCandidates")
def dac():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        print("deleteing candis")
        mess = db.deleteAllCandidates()
        return json.dumps(mess)
    return json.dumps("problem deleting candidates")


@bottle.post("/makeVoteCodes")
def MV():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        print("make " + cred )
        data  = db.makeVoteCodes(cred)
        return json.dumps(data)
    return json.dumps("problem with authentication")

@bottle.route("/sendVoteCodes")
def svc():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        print("sending vote codes")
        liOfLi = db.allVoteCodes()
        print(liOfLi)
        return json.dumps(liOfLi)
    return json.dumps("problem loading log")

@bottle.route("/deleteAllVoteCodes")
def davc():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        print("deleteing vote codes")
        mess = db.deleteAllVoteCodes()
        return json.dumps(mess)
    return json.dumps("problem loading log")

@bottle.post("/deleteVoteCode")
def dvc():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        print("delete " + cred )
        data  = db.deleteVoteCode(cred)
        return json.dumps(data)
    return json.dumps("problem with authentication")

# for public
@bottle.route("/getCandidatesForVoting")
def cfv():
    print("on pages")
    mess = db.candidatesForVotingPage()
    return json.dumps(mess)

@bottle.post("/vote")
def vote():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    print(cred)
    ret = db.vote(cred)
    return json.dumps(ret)

# voting status change and check
@bottle.route("/votingStatus")
def vs():
    stat = help.votingStatus
    print(stat)
    return stat

@bottle.route("/changeVotingStatus")
def cvs():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        va = help.changeVotingStat()
        print(va)
        return va
    return json.dumps("user not recognized")

#  static files

@bottle.route("/")
def login_page():
    return bottle.static_file("frontend/adminLogin.html", root=".")

@bottle.route("/adminLoginJs.js")
def login_page():
    return bottle.static_file("frontend/adminLoginJs.js", root=".")

@bottle.route("/communication.js")
def login_page():
    return bottle.static_file("frontend/communication.js", root=".")

@bottle.route("/votingPage.html")
def login_page():
    return bottle.static_file("frontend/votingPage.html", root=".")

@bottle.route("/votingPageJS.js")
def login_page():
    return bottle.static_file("frontend/votingPageJS.js", root=".")

@bottle.route("/<filename>")
def dashboard_page(filename):
    username = get_username()
    retval = db.check_username(username)
    print(filename, "jhv")
    if username and retval:
        print(filename, "jhv")
        return bottle.static_file("frontend/"+filename, root=".")
    return None


# key to client

@bottle.route('/key')
def key():
    with open("pemFiles/public-attend-app.pem") as f:
        data = f.read()
    response = {'key': data}
    print(response)
    return json.dumps(response)



eventlet.wsgi.server(eventlet.listen(('', 8089)), bottle.default_app())
bottle.run(host='0.0.0.0' , port = '8089' , debug = True)