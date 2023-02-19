import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123mrsl123",
    database="mydatabase"
)

mycursor = mydb.cursor()

sql =  "INSERT INTO product (Price, Inventory ,Name) VALUES (%s, %s,%s)"
val=[]
n = int(input("tedad: "))
print("price" , "Inventory" , " name")
for i in range(n):
    data = input().split(" ")
    val.append((int(data[0]) , int(data[1]) , data[2] ))

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")