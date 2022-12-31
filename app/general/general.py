from flask import Blueprint,session,render_template,redirect,url_for,request
from app.models import mydb

general=Blueprint("general",__name__,static_folder="static",template_folder="templates")

cursor = mydb.cursor(dictionary=True)



@general.route("/")
@general.route("/home")
@general.route("/index")
def index():
    if 'email' in session:
        print(request.args)
        page_number = request.args.get('page', 0)
        offset=6*int(page_number)
        print("off",offset)
       #cursor.execute("select * from prod")
        cursor.execute("SELECT * FROM prod ORDER BY id LIMIT 6 OFFSET %s",[offset])
        user=cursor.fetchall()
        print(len(user))
        cursor.execute("select count(id) from prod")
        count=cursor.fetchall()[0].get('count(id)')
        print("count-",count)
        maxpage=int(count / 6)
        email = session['email']
        name = email[0:6].upper()  # hardcoded get the name from the email
       # print("in index page " ,session['id'])
        return render_template("index.html",  rows=user, name=session['username'],maxpage=maxpage+1)
    else:
        return redirect(url_for("auth.login"))



@general.route("/search")
def search():
    if 'email' in session:
     q=request.args.get("q")
     select_stmt = f'''SELECT * FROM prod WHERE prod_type like '%{q}%' '''     #working search by name
     cursor.execute(select_stmt)
     rows = cursor.fetchall();
     email = session['email']        #ye isliye taki
     name = email[0:6].upper()       #naam dikha ske hr page pe(hardcoded)
     return render_template("search.html", rows=rows,name=session['username'])
    else:
        return redirect(url_for("auth.login"))

