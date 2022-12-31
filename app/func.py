from flask import Flask,session
from app.models import mydb

cursor = mydb.cursor(dictionary=True)

def isUserLoggedIn():
    if 'email' in session:
        return  True
    else:
        return False

def checkIfUserPrevExists(email):
    cursor.execute("select * from user")
    rows=cursor.fetchall()
    for row in rows:
        if row['email']==email:
             return True

    return False



def checkLoginCredientials(email,password):   #for login
    cursor.execute("select * from user")
    rows = cursor.fetchall()
    for row in rows:
        if row['email'] == email and row['password'] == password:
            return True

    return False
