from flask import Blueprint,session,request,flash,render_template,redirect,url_for
from datetime import date
import random
from app.models import mydb

order=Blueprint("order",__name__,static_folder="static",template_folder="templates")
cursor = mydb.cursor(dictionary=True)


@order.route("/placeorder",methods=["POST"])
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


@order.route("/myorder",methods=["GET"])
def myorder():
    if 'email' in session:
     #user_id=1  #session changes
    # cursor.execute('SELECT * FROM orders WHERE user_id=%s   order by id desc ', [user_id])    #session changes
     cursor.execute("select * from orders  where user_id = %s order by id desc", [session['id']])
     user = cursor.fetchall()
     email = session['email']
     name = email[0:6].upper()
     return render_template("myorder.html",arr=user,name=session['username'])
    else:
        return redirect(url_for("auth.login"))