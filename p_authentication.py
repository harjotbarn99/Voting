import p_database as db 
import csv
from datetime import date
from datetime import datetime
import html
import bottle

# code used for signing up
codeOrg = "999"

# registers a user
def add_user(dic):
  for i in dic.values():
    if i =="":
      return "Any Field can not be left empty"
  username = html.escape(dic["username"])
  password = html.escape(dic["password"])
  code = html.escape(dic["accessCode"])
  if db.check_username(username):
    return "username \""+username+ "\" already exists"
  if code != codeOrg:
    return "wrong access code"
  db.add_creds(username,password)
  return username + " registered"
  
# authenticate user
def authenticate(dic):
  resp = {"authenticated":False,"message":"Username and Password can not be left empty"}
  username = html.escape(dic["username"])
  password = html.escape(dic["password"])
  if username == "" or password =="":
    return resp
  #login_atmpt(username)
  if not db.check_username(username):
    resp["message"]= "username \""+username+"\" does not exist"
    return resp
  elif db.validate_creds(username,password):
    resp = {"authenticated":True,"message":"welcome "+username}
    return resp
  else:
    resp = {"authenticated":False,"message":" password incorrect"}
    return resp

# registers login attempts uncomment line 33 to use this function
def login_atmpt(user):
  ipAddress = bottle.request.environ.get('REMOTE_ADDR')
  today = date.today()
  now = datetime.now()
  li = [user,today,now,ipAddress]
  with open("loginAttempts.csv","a") as l:
    write = csv.writer(l)
    write.writerow(li)
    l.close()
  return "ok"



