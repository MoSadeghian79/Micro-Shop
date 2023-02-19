import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123mrsl123",
  database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE product (Price INT NOT NULL,Inventory INT NOT NULL,Name varchar(64),Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY); ")