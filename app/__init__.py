from flask import Flask
from app.auth.auth import auth
from app.general.general import general
from app.mycart.mycart import mycart
from app.order.order import order

app=Flask(__name__)
app.secret_key = "hello"



app.register_blueprint(auth,url_prefix="")
app.register_blueprint(general,url_prefix="")
app.register_blueprint(mycart,url_prefix="")
app.register_blueprint(order,url_prefix="")
