import mysql.connector


mydb = mysql.connector.connect(                #works after giving auth_login
  host="localhost",
  user="root",
  password="admin123",
  auth_plugin='mysql_native_password',
  database="myproject"
)
cursor = mydb.cursor(dictionary=True)