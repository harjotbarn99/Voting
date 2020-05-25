import sqlite3
import html
import help
import bcrypt

# need to make it presist after restart

db="z_Database1.db"
conn=sqlite3.connect(db)
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (username,password) ")
cur.execute("CREATE TABLE IF NOT EXISTS voteCodes (code) ")
cur.execute("CREATE TABLE IF NOT EXISTS candidates (category,venture , nameParticipant , ventureDetails, votes) ")


def add_creds(username,password):
  password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
  cur.execute(" INSERT INTO users VALUES (?,?) ",(username,password_hash))
  conn.commit()
  return None


def check_username(username):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    return True



def validate_creds(username,password):
  for user in cur.execute("SELECT * FROM users WHERE username = ? ",(username,)):
    encodedPass = password.encode('utf8')
    return bcrypt.checkpw(encodedPass, user[1])
  return False



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

def allCandidates():
  retLi = []
  for can in cur.execute("SELECT * FROM candidates"):
    li =[]
    for i in can:
      li.append(i)
    retLi.append(li)
  return retLi

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

def sortHelper(tup):
  return tup[2]

def sortedCandidates():
  dic = candidatesForSorting()
  for cate in dic:
    li = dic[cate]
    li.sort(key = sortHelper, reverse= True)
    dic[cate] = li
  return dic
sortedCandidates()


# chcke if name is empty or does not exist
def deleteCandidate(name):# deletes all by that name
  if name =="":
    return "name to delete is empty"
  nameEscaped = html.escape(name)
  li = list(cur.execute("SELECT * FROM candidates where venture = ?",(nameEscaped,)))
  if len(li) < 1 :
    return "no such person"
  cur.execute("DELETE FROM candidates where venture = ?",(nameEscaped,))
  conn.commit()
  return "deleted" + html.escape(name)

def deleteAllCandidates():
  cur.execute("DELETE FROM candidates")
  conn.commit
  return "Deleted all candidates"


def makeVoteCodes(numSt):
  num = int(numSt)
  for i in range(num):
    cur.execute("INSERT INTO voteCodes VALUES (?)",(help.randomCode(4,2),))
    conn.commit
  conn.commit()
  return " voter added :" + str(num)


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
  conn.commit
  return "deleted " + html.escape(code)


def deleteAllVoteCodes():
  cur.execute("DELETE FROM voteCodes")
  conn.commit
  return "all codes deleted"


# cast a vote

def vote(dict):
  code = dict.get("code","")
  if help.votingStatus == "Voting is disabled":
    return "voting has been disabled ..."
  if code == "":
    return "please enter code"
  ifCode = deleteVoteCode(code)
  if (ifCode == "the entered code does not exist"):
    return "wrong code"
  elif (ifCode == "deleted " + html.escape(code)):
    listTovote = dict.get("li","")
    for i in listTovote:
      escapedVenture = html.escape(i)
      candi = list(cur.execute("SELECT votes FROM candidates WHERE venture = ?",(escapedVenture,)))
      votesPlus1 = candi[0][0] + 1
      cur.execute("UPDATE candidates SET votes = ? WHERE venture = ?",(votesPlus1,escapedVenture))
      conn.commit()
    print(allCandidates())
    return "voted"
  return "nnnnnn"

# clear all votes

def clearAllVotes():
  cur.execute("UPDATE candidates SET votes = 0")
  conn.commit()
  return "Votes set to Zero!"


