from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from app.auth.forms import RegistrationForm,LoginForm
from app.func import checkLoginCredientials,checkIfUserPrevExists,isUserLoggedIn
import random
from datetime import date
#import mysql.connector
from app.models import mydb


auth=Blueprint("auth",__name__,static_folder="static",template_folder="templates")

'''
mydb = mysql.connector.connect(                #works after giving auth_login
  host="localhost",
  user="root",
  password="admin123",
  auth_plugin='mysql_native_password',
  database="myproject"
)'''

cursor = mydb.cursor(dictionary=True)


@auth.route("/signup",methods=["GET","POST"])
def signup():
    form = RegistrationForm()
    if request.method=="POST" and form.validate_on_submit():
        username = form.username.data
        username = username.strip()      #taki aage peche ka agr koi space hai to ht jaye
        email = form.email.data
        password = form.password.data
        if checkIfUserPrevExists(email):
            flash("user already exists so  go to login page ",'danger')
            return render_template("signup.html", title="signup", form=form)
        else :
           cursor.execute("insert into user (username,email,password)  VALUES (%s,%s,%s)", (username,  email, password))
           mydb.commit()
           flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("auth.login"))
    return render_template("signup.html", title="signup", form=form)    #get request


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method=="POST" and form.validate_on_submit():
        email   =form.email.data
        password=form.password.data
        if checkLoginCredientials(email,password):
           session['email']=email
           cursor.execute("select * from user where email =%s and password=%s",(email,password))
           record=cursor.fetchone()    #bcz records is unique   ,dict form me aaiga
           session['id']=record['id']
           session['username']=record['username']
        #   print("in login func", type(record))
       #    print("in login func", session['id'])
          # print(record['ID'], record['email'],record['password'],record['username'])
           flash('You have been logged in!', 'success')
           return  redirect(url_for("general.index"))     #valid credientials
        else:
            flash('Invalid email and password!', 'danger')
            return render_template("login.html", title="login",form=form)
    else:
        if 'email' in session:    #means if user logged in
            return redirect(url_for("general.index"))
        else:
          return render_template("login.html", title="login",form=form)





@auth.route("/logout")
def logout():
    if 'email' in session:
     print("in logout page", session['id'])
     print("in logout  page", session['email'])
     session.pop('id', None)       #session changes
     session.pop('email', None)
     session.pop('username',None)
    return redirect(url_for("auth.login"))












"""
#general
@second.route("/")
@second.route("/home")
@second.route("/index")
def index():
    if 'email' in session:
        cursor.execute("select * from prod")
        user=cursor.fetchall()
        email = session['email']
        name = email[0:6].upper()  # hardcoded get the name from the email
       # print("in index page " ,session['id'])
        return render_template("index.html",  rows=user, name=name)
    else:
        return redirect(url_for("second.login"))
"""

"""
#general
@second.route("/search")
def search():
    q=request.args.get("q")
    select_stmt = f'''SELECT * FROM prod WHERE prod_type like '%{q}%' '''     #working search by name
    cursor.execute(select_stmt)
    rows = cursor.fetchall();
    email = session['email']        #ye isliye taki
    name = email[0:6].upper()       #naam dikha ske hr page pe(hardcoded)
    return render_template("search.html", rows=rows,name=name)
"""

"""
#cart
arr = []
@second.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        arr.append(request.form.get('id'))
        print(request.form.get('id'),request.form.get('prod_id'))
        prod_id=request.form.get('prod_id')
        cursor.execute('SELECT * FROM prod WHERE prod_id=%s', [prod_id])  #we know ke hmesha ek product aaiga kyuki prod_id unique hai
        rows=cursor.fetchall()                                             #vaise list of dict aaigi,but row ek he hogi or we can use fetchone()
        print(len(rows))
        print(type(rows[0]))
        print(rows[0]['title'],rows[0]['img_src'])
        img_src=rows[0]['img_src']
        title=rows[0]['title']
        descript=rows[0]['descript']
       # user_id=1                     #session changes
        user_id=session['id']          #session changes
        price=rows[0]['price']
        prod_type=rows[0]['prod_type']
        prod_id=rows[0]['prod_id']
        type_del=rows[0]['type_del']
        counts=1

        cursor.execute("select * from cart where user_id= %s and prod_id = %s ",[user_id,prod_id])
        result=cursor.fetchall()
        print(type(result))
        print(len(result))
        if len(result)==0:
            cursor.execute("insert into cart (img_src,title,descript,user_id,price,prod_type,prod_id,type_del,counts)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",  (img_src, title, descript, user_id, price, prod_type, prod_id, type_del, counts))
            mydb.commit()
        else:
            cursor.execute("select * from cart where user_id= %s and prod_id = %s ", [user_id, prod_id])   #hmne aese insert kre hai ke ek record aaiga
            rows = cursor.fetchall()
            counts = rows[0]['counts']
            print("counts =", counts)
            cursor.execute("update cart set counts=%s  where user_id = %s and prod_id=%s",(counts + 1, user_id, prod_id))
            mydb.commit()
        return ('', 204)
       # return redirect(url_for("home"))
       # return redirect(url_for("index"))

    else :
       # user_id = 1      #session changes
      #  cursor.execute('SELECT * FROM cart WHERE user_id=%s', [user_id])
        user_id=session['id']
        cursor.execute('SELECT * FROM cart WHERE user_id=%s', [user_id])    #yha tk session changes
        user=cursor.fetchall()
        amount=0
        for usr in user:
            amount+=usr['price']*usr['counts']
        print(amount)
        email = session['email']
        name = email[0:6].upper()
        print("in cart page", session['id'])
    #return render_template("cart.html", arr=user,amount=amount,name=name,user_id=user_id)     #session changes
    return render_template("cart.html", arr=user, amount=amount, name=name, user_id=session['id'])    #session changes
"""

"""
#cart
@second.route("/editcart",methods=["POST"])
def editcart():
     print(request.form.get('user_id'), request.form.get('prod_id'))
     user_id=request.form.get('user_id')
     prod_id=request.form.get('prod_id')
     cursor.execute("select * from cart where user_id =%s and prod_id=%s",(user_id,prod_id))
     row=cursor.fetchone()                #fetchone - me phla result aaiga to vo dict ka he hoga,fetchall()-me list aati hai dict type ke
     print(type(row))
     counts =row['counts']
     print("counts = ",counts)
    # print("counts = ",row['counts'])
     if counts == 1 :   #agr ek hai to delete
         cursor.execute("delete from cart  where user_id = %s and prod_id=%s", ( user_id, prod_id))
     else :    #agr se jyada hai to count km krdo
         cursor.execute("update cart set counts=%s  where user_id = %s and prod_id=%s", (counts - 1, user_id, prod_id))
     mydb.commit()
     return redirect(url_for("second.cart"))
     #return render_template("cart.html")
"""

"""
#order
@second.route("/placeorder",methods=["POST"])
def placeorder():
      print("user id in placeorder from cart html ",request.form.get('user_id'))
     # user_id=request.form.get('user_id')                 #session changes
      user_id = session['id']                              #session changes
      cursor.execute("select * from cart where user_id=%s",[user_id])
      rows=cursor.fetchall()

      today = date.today()

      # Textual month, day and year
      today_date = today.strftime("%b %d, %Y")  # %B=for full month name
      print("today_date =", today_date, type(today_date))   # give today date for order date

      x = random.randrange(0, 10000000)  # generate random number for order id
      order_id = '#' + str(x)

      for row in rows:
          print(row['ID'],row['img_src'])               #neeche line me session changes
          #cursor.execute("insert into orders(ord_date, user_id, img_src, prod_id, prod_type, price, counts, title, descript, order_id)   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (today_date ,  1, row['img_src'], row['prod_id'], row['prod_type'], row['price'] ,row['counts'], row['title'], row['descript'], order_id))
          cursor.execute("insert into orders(ord_date, user_id, img_src, prod_id, prod_type, price, counts, title, descript, order_id)   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (today_date , session['id'], row['img_src'], row['prod_id'], row['prod_type'], row['price'] ,row['counts'], row['title'], row['descript'], order_id))
          #  insert into orders() values()
          # cursor.execute(    "insert into cart (img_src,title,descript,user_id,price,prod_type,prod_id,type_del,counts)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (img_src, title, descript, user_id, price, prod_type, prod_id, type_del, counts))
          # yha phle  mycart table me product add krvane hai

      cursor.execute("delete from cart where user_id =%s ", [user_id])
      mydb.commit()
      flash("Your order has been placed successfully", "success")
      return ('', 204)

#order
@second.route("/myorder",methods=["GET"])
def myorder():
    #user_id=1  #session changes
   # cursor.execute('SELECT * FROM orders WHERE user_id=%s   order by id desc ', [user_id])    #session changes
    cursor.execute("select * from orders  where user_id = %s order by id desc", [session['id']])
    user = cursor.fetchall()
    email = session['email']
    name = email[0:6].upper()
    return render_template("myorder.html",arr=user,name=name)
"""

#----------------------------------------------------------------------------------------------------------------#
'''
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
    '''
