import string
import random




def randomCode(numAlph,numNum):
    code =""
    for i in range(numAlph):
        code += random.choice(string.ascii_uppercase)

    for i in range(numNum):
        code += random.choice(string.digits)

    finalCode = ""
    for i in random.sample(code,len(code)):
        finalCode += i
    return finalCode


votingStatus = "Voting is disabled"

def disableVoting():
    global votingStatus
    votingStatus = "Voting is disabled"
    return

def enableVoting():
    global votingStatus
    votingStatus = "Voting is enabled"
    return

def changeVotingStat():
    global votingStatus
    if votingStatus == "Voting is enabled":
        disableVoting()
        return "voting disabled"
    elif votingStatus == "Voting is disabled":
        enableVoting()
        return "Voting enabled"
    return "problem changing status"





