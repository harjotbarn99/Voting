import sqlite3
import html
import help
import bcrypt

# establish connections and cursor
db="z_DatabaseTest.db"
conn=sqlite3.connect(db)
cur=conn.cursor()

#create tables
cur.execute("CREATE TABLE IF NOT EXISTS users (username,password) ")
cur.execute("CREATE TABLE IF NOT EXISTS voteCodes (code) ")
cur.execute("CREATE TABLE IF NOT EXISTS candidates (category,venture , nameParticipant , ventureDetails, votes) ")

# add users into DB and username and pass are escaped
def add_creds(username,password):
  password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
  cur.execute(" INSERT INTO users VALUES (?,?) ",(username,password_hash))
  conn.commit()
  return None

# checks if the username exists in the DB
def check_username(username):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    return True

# checks if a user with a specefic password exists in a DB , checks hashed pass
def validate_creds(username,password):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    encodedPass = password.encode('utf8')
    return bcrypt.checkpw(encodedPass, user[1])
  return False


# Candidates page
# add a candidate into DB
def addCandidate(dic):
  for i in dic.values() :
    if i == "":
      return "can not leave this empty"
  name = html.escape(dic["name"])
  venture = html.escape(dic["venture"])
  category = html.escape(dic["category"])
  ventureDetails = html.escape(dic["ventureDetails"])
  cur.execute(" INSERT INTO candidates VALUES (?,?,?,?,?) ",(category,venture,name,ventureDetails,0))
  conn.commit()
  return "candidate added"

# selects all candidates to send to the candidatesControl page
def allCandidates():
  retLi = []
  for can in cur.execute("SELECT * FROM candidates"):
    li =[]
    for i in can:
      li.append(i)
    retLi.append(li)
  return retLi

# Selects all the candidates and make a dictionary with keys as categories and values as list of tuples that are candidates
def candidatesForSorting():
  li = ["Social","General","Technology"]
  map = {}
  for i in li:
    candi = cur.execute("SELECT venture , nameParticipant, votes FROM candidates WHERE category = ?",(i,))
    liOfcandi = []
    for a in candi:
      liOfcandi.append(a)
    map[i] = liOfcandi
  return map

# used to get value at index 2 of a tuple to sort
def sortHelper(tup):
  return tup[2]

# sorts the candidates according to votes in the dictionary given by candidateForSorting().
def sortedCandidates():
  dic = candidatesForSorting()
  for cate in dic:
    li = dic[cate]
    li.sort(key = sortHelper, reverse= True)
    dic[cate] = li
  return dic

# check if venture name is empty or does not exist
def deleteCandidate(ventureName):# deletes all by that venture name
  if ventureName == "":
    return "name to delete is empty"
  ventureNameEscaped = html.escape(ventureName)
  li = list(cur.execute("SELECT * FROM candidates where venture = ?",(ventureNameEscaped,)))
  if len(li) < 1 :
    return "no such candidate registered"
  cur.execute("DELETE FROM candidates where venture = ?",(ventureNameEscaped,))
  conn.commit()
  return "deleted " + ventureNameEscaped

# deletes all candidates in the DB
def deleteAllCandidates():
  cur.execute("DELETE FROM candidates")
  conn.commit()
  return "Deleted all candidates"

# clear votes for all candidates
def clearAllVotes():
  cur.execute("UPDATE candidates SET votes = 0")
  conn.commit()
  return "Votes set to Zero!"


# voting page
# selects all the candidates for voting page but only selects venture and candidates name
def candidatesForVotingPage():
  li = ["Social","General","Technology"]
  map = {}
  for i in li:
    candi = cur.execute("SELECT venture , nameParticipant FROM candidates WHERE category = ?",(i,))
    liOfcandi = []
    for a in candi:
      liOfcandi.append(a)
    map[i] = liOfcandi
  return map

# cast a vote
def vote(dict):
  code = html.escape(dict.get("code",""))
  if help.votingStatus == "Voting is disabled":
    return "voting has been disabled ..."
  if code == "":
    return "please enter code"
  ifCode = deleteVoteCode(code)
  if (ifCode == "the entered code does not exist"):
    return "wrong code"
  elif (ifCode == "deleted " + html.escape(code)):
    listToVote = dict.get("li","")
    for candidate in listToVote:
      escapedVenture = html.escape(candidate)
      listOfCandidates = list(cur.execute("SELECT votes FROM candidates WHERE venture = ?",(escapedVenture,)))
      votesPlus1 = listOfCandidates[0][0] + 1
      cur.execute("UPDATE candidates SET votes = ? WHERE venture = ?",(votesPlus1,escapedVenture))
    conn.commit()
    return "voted"
  return "Something went wrong while voting"


# vote codes page
# makes random strings
def makeVoteCodes(numSt):
  num = int(html.escape(numSt))
  for i in range(num):
    cur.execute("INSERT INTO voteCodes VALUES (?)",(help.randomCode(4,2),))
  conn.commit()
  return " vote codes added : " + str(num)

# selects and sends all vote codes in DB in a list
def allVoteCodes():
  retLi = []
  for can in cur.execute("SELECT * FROM voteCodes"):
    li =[]
    for i in can:
      li.append(i)
    retLi.append(li)
  return retLi

# chcke if code is empty or does not exist
def deleteVoteCode(code):
  if code == "":
    return "please enter code to delete"
  escapedCode = html.escape(code).upper()
  li = list(cur.execute("SELECT * FROM voteCodes where code = ?",(escapedCode,)))
  if len(li) < 1:
    return "the entered code does not exist"
  cur.execute("DELETE FROM voteCodes where code = ?",(escapedCode,))
  conn.commit()
  return "deleted " + escapedCode

# delete all the vote codes
def deleteAllVoteCodes():
  cur.execute("DELETE FROM voteCodes")
  conn.commit()
  return "all codes deleted"







