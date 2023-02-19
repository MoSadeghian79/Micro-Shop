import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123mrsl123"
)

mycursor = mydb.cursor()
str = "CREATE DATABASE mydatabase"
mycursor.execute(str)
