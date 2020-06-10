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

# reads a pem file and gives a cipher for encryption, decryption and signing.
def get_cypher(key_filename):
    with open(key_filename) as f:
        data = f.read()
    key = RSA.importKey(data,"Barn1999")
    cipher = PKCS1_OAEP.new(key)
    return cipher

# ciphers
cipher = get_cypher("pemFiles/private-attend-app.pem")
cipher_verify = get_cypher("pemFiles/private-attend-app-token.pem")
cipher_sign = get_cypher("pemFiles/public-attend-app-token.pem")

# decrypt info from frontend or cookie text
def decryptt(cyphertext, verify=False):
    content = b64decode(cyphertext)
    if verify:
        content = cipher_verify.decrypt(content).decode()
    else:
        content = cipher.decrypt(content).decode()
    return content

# make an encripted string for cookie
def sign(text):
    cyphertext = cipher_sign.encrypt(text.encode())
    cyphertext = b64encode(cyphertext).decode()
    return cyphertext

# requests cookie from client and verifies if the user is valid
def get_username():
    username = bottle.request.get_cookie("token")
    if not username:
        return None
    return decryptt(username, True)



#  requestes for communication ( admin )
# login handled here - use db to confirm user and set cookie
@bottle.post("/login")
def loginAttempt():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    loginDetails=json.loads(content)
    message = ath.authenticate(loginDetails)
    if message['authenticated']:
        bottle.response.set_cookie("username", loginDetails["username"])
        bottle.response.set_cookie("token", sign(loginDetails["username"]))
    return json.dumps(message)


# sign up
@bottle.post("/signUp")
def reg():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    message = ath.add_user(cred)
    return message

# Take the candidate details and add them in database
@bottle.post("/rigisterCandidate")
def RC():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        credentials=json.loads(content)
        data  = db.addCandidate(credentials)
        return json.dumps(data)
    return json.dumps("problem with authentication")

# make all the votes 0
@bottle.route("/makeVotesZero")
def mvz():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        message = db.clearAllVotes()
        return json.dumps(message)
    return json.dumps("problem setting votes to zero")

# read the database and send all the candidates in the database
@bottle.route("/sendCandidates")
def sc():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        message = db.allCandidates()
        return json.dumps(message)
    return json.dumps("problem sending candidates")

# read the database and send all the candidates in the database in a sorted order to select the winners
@bottle.route("/sendSortedCandidates")
def ssc():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        dictOfcandidatesCategorizedSorted = db.sortedCandidates()
        return json.dumps(dictOfcandidatesCategorizedSorted)
    return json.dumps("problem sending sorted candidates")

# delete a candidates in the database with a venture name sent from frontend
@bottle.post("/deleteCandidate")
def DC():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        message = db.deleteCandidate(cred)
        return json.dumps(message)
    return json.dumps("problem with authentication")

# delete all candidates in the database
@bottle.route("/deleteAllCandidates")
def dac():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        message = db.deleteAllCandidates()
        return json.dumps(message)
    return json.dumps("problem deleting candidates")

# take a number from frontend and make random strings
@bottle.post("/makeVoteCodes")
def MV():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        message = db.makeVoteCodes(cred)
        return json.dumps(message)
    return json.dumps("problem with authentication")

# read the votecodes from DB and send all the codes to frontend
@bottle.route("/sendVoteCodes")
def svc():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        liOfVoteCodes = db.allVoteCodes()
        return json.dumps(liOfVoteCodes)
    return json.dumps("problem loading log")

# delete all the voteCodes
@bottle.route("/deleteAllVoteCodes")
def davc():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        message = db.deleteAllVoteCodes()
        return json.dumps(message)
    return json.dumps("problem loading log")

# delete a particular voteCode
@bottle.post("/deleteVoteCode")
def dvc():
    username = get_username()
    userInDB = db.check_username(username)
    if username and userInDB:
        content = bottle.request.body.read().decode()
        content = decryptt(content)
        cred=json.loads(content)
        message = db.deleteVoteCode(cred)
        return json.dumps(message)
    return json.dumps("problem with authentication")

# voting status check
@bottle.route("/votingStatus")
def vs():
    stat = help.votingStatus
    return stat

# voting status change
@bottle.route("/changeVotingStatus")
def cvs():
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        va = help.changeVotingStat()
        print(va)
        return va
    return json.dumps("user not recognized")


# for public
# send all the candidates to frontend for voting
@bottle.route("/getCandidatesForVoting")
def cfv():
    liOfTuplesOfCandidates = db.candidatesForVotingPage()
    return json.dumps(liOfTuplesOfCandidates)

# cast a vote
@bottle.post("/vote")
def vote():
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    message = db.vote(cred)
    return json.dumps(message)


#  static files

@bottle.route("/")
def login_page():
    return bottle.static_file("FrontEnd/adminLogin.html", root=".")

@bottle.route("/adminLoginJs.js")
def login_page():
    return bottle.static_file("FrontEnd/adminLoginJs.js", root=".")

@bottle.route("/communication.js")
def login_page():
    return bottle.static_file("FrontEnd/communication.js", root=".")

@bottle.route("/votingPage.html")
def login_page():
    return bottle.static_file("FrontEnd/votingPage.html", root=".")

@bottle.route("/votingPageJS.js")
def login_page():
    return bottle.static_file("FrontEnd/votingPageJS.js", root=".")

# send any static file requested but after authentication
@bottle.route("/<filename>")
def dashboard_page(filename):
    username = get_username()
    retval = db.check_username(username)
    if username and retval:
        return bottle.static_file("FrontEnd/"+filename, root=".")
    return None


# PublicKey for the clients to send encripted info
@bottle.route('/key')
def key():
    with open("pemFiles/public-attend-app.pem") as f:
        data = f.read()
    response = {'key': data}
    return json.dumps(response)


eventlet.wsgi.server(eventlet.listen(('', 8089)), bottle.default_app())
bottle.run(host='0.0.0.0' , port = '8089' , debug = True)