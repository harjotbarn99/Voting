import string
import random


# generates a random string with numAlph alphabets and numNum  numbers
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

# Voting status

votingStatus = "Voting is disabled"

# disable voting
def disableVoting():
    global votingStatus
    votingStatus = "Voting is disabled"
    return

# enable voting
def enableVoting():
    global votingStatus
    votingStatus = "Voting is enabled"
    return

# Change voting status
def changeVotingStat():
    global votingStatus
    if votingStatus == "Voting is enabled":
        disableVoting()
        return "voting disabled"
    elif votingStatus == "Voting is disabled":
        enableVoting()
        return "Voting enabled"
    return "problem changing status"





