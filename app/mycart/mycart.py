from flask import Blueprint,render_template,request,session,redirect,url_for
from app.models import mydb

mycart=Blueprint("mycart",__name__,static_folder="static",template_folder="templates")
cursor = mydb.cursor(dictionary=True)

arr = []
@mycart.route("/cart", methods=["GET", "POST"])
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
        if 'email' in session:
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
         return render_template("cart.html", arr=user, amount=amount, name=session['username'], user_id=session['id'])    #session changes
        else:
           return redirect(url_for("auth.login"))




@mycart.route("/editcart",methods=["POST"])
def editcart():
     print(request.form.get('user_id'), request.form.get('prod_id'),request.form.get('task'))
     user_id=request.form.get('user_id')
     prod_id=request.form.get('prod_id')
     task=request.form.get('task')
     cursor.execute("select * from cart where user_id =%s and prod_id=%s",(user_id,prod_id))
     row=cursor.fetchone()                #fetchone - me phla result aaiga to vo dict ka he hoga,fetchall()-me list aati hai dict type ke
     print(type(row))
     counts =row['counts']
     print("counts = ",counts)
    # print("counts = ",row['counts'])
     '''
     if counts == 1 :   #agr ek hai to delete
         cursor.execute("delete from cart  where user_id = %s and prod_id=%s", ( user_id, prod_id))
     else :    #agr se jyada hai to count km krdo
         cursor.execute("update cart set counts=%s  where user_id = %s and prod_id=%s", (counts - 1, user_id, prod_id))
     mydb.commit()'''

     if task=='rem':
         cursor.execute("delete from cart  where user_id = %s and prod_id=%s", (user_id, prod_id))
     elif task=='neg' and counts > 1:
         cursor.execute("update cart set counts=%s  where user_id = %s and prod_id=%s", (counts - 1, user_id, prod_id))
     elif task=='pos':
         cursor.execute("update cart set counts=%s  where user_id = %s and prod_id=%s", (counts + 1, user_id, prod_id))
     mydb.commit()
     return redirect(url_for("mycart.cart"))      #isi module me hai , get request pe call
     #return render_template("cart.html")