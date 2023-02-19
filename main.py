from tkinter import *
from tkinter import ttk
import mysql.connector
import serial
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123mrsl123",
    database="mydatabase"
)

Xlistbox = 10
Ylistbox = 10
Hlistbox = 5
Wlistbox = 30
Xlistbox2= 20
Ylistbox2 = 10
Hlistbox2 = 5
Wlistbox2 = 30
XText = 10
YText = 10
HText = 50
WText = 30


def sync(name , val):
    ser = serial.Serial('COM2', 9600)

    ser.timeout = 1
    lenght = str(len(val))
    ser.write(lenght.encode())
    ser.write('-'.encode())
    tmp = []

    for i in val:

        tmp = [str(i[0]),str(i[1])]
        ser.write(tmp[0].encode())
        ser.write('-'.encode())
        ser.write(tmp[1].encode())
        ser.write('-'.encode())


    #ser.write('hello world'.encode())
    time.sleep(0.5)
    ser.read()


class Product:
    choos = False
    def __init__(self, ID , name, price , Inventory ):
        self.ID = ID
        self.name = name
        self.price = price
        self.inventory = Inventory

'''#sample
products = [Product(1 , "chips" , 2400, 8) ,
            Product(2 , "pofak" , 3600, 15) ,
            Product(3 , "bastani" , 4800,18),
            Product(4 , "adams" , 5000,20),]
'''
products = []
selected = []
total = 0
viewSelcted = []
def ReadFromDB():
    global products
    products = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM product")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
        products.append(Product(x[3] , x[2] , x[0] , x[1] ))

ReadFromDB()
def UpdateDB():
    mycursor = mydb.cursor()

    sql = "UPDATE product SET Inventory = %s WHERE Id = %s"
    val =[]
    syncval = []
    for i in selected:
        val.append((products[i[0]].inventory - i[1] , products[i[0]].ID))
        syncval.append([products[i[0]].ID , i[1]])

    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")


    ReadFromDB()
    listbox1.delete(0,END)
    b = 0
    for i in products:
        listbox1.insert(b, i.name + " - " + str(i.price) + " - " + str(i.inventory))
        b = b + 1

    sync("ali" , syncval)


def sendpopup(massage):
    popup = Tk()
    popup.wm_title("ERROR")
    label = ttk.Label(popup, text=massage)
    label.pack(side="top", fill="x", pady=10, padx=5)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack(pady=5)
    popup.mainloop()

win = Tk()
win.title("SHOP")
#______________________________________
label1 = Label(master=win, text="Products")
label1.grid(row=0,column=0, pady=5)
#______________________________________
listbox1 = Listbox(win, height=Hlistbox,
                  width=Wlistbox,
                  bg="white",
                  activestyle='dotbox',
                  font="Helvetica",
                  fg="black")
b = 0
for i in products:
    listbox1.insert(b, i.name + " - " +str(i.price) + " - " + str(i.inventory))
    b = b+1

listbox1.grid(row=1, column=0)#place(x=Xlistbox, y=Ylistbox)
#_____________________________________________
label2 = Label(master=win, text="basket")
label2.grid(row=2,column=0, pady=5)
#______________________________________
listbox2 = Listbox(win, height=Hlistbox2,
                  width=Wlistbox2,
                  bg="white",
                  activestyle='dotbox',
                  font="Helvetica",
                  fg="black")

listbox2.grid(row=3, column=0)
#______________________________________
E1 = Entry(win, bd =2 , width = 10 )
E1.grid(row=0, column=1 ,pady = 5,padx = 5)
#______________________________________

def ButtonAdd():
    number = E1.get()
    try:
        number = int(number)
    except:
        sendpopup("input valu is not valid")
        return
    if number < 1:
        sendpopup("valu must biger than 0")
        return
    choos = listbox1.curselection()
    if len(choos) == 0:
        sendpopup("pleas choos from listbox")
        return
    index = listbox1.curselection()[0]
    if products[index].inventory<number:
        sendpopup("Insufficient inventory")
        return
    if products[index].choos:
        sendpopup("You choos this before")
        return

    print(products[index].choos)
    products[index].choos = True
    print(products[index].choos)
    listbox2.insert(1000, products[index].name + " - " + str(number) +" * " + str(products[index].price) + " - "+str(products[index].price * number))
    selected.append((index, number , products[index].price))
    viewSelcted.append(products[index].name + " - " + str(number) +" * " + str(products[index].price) + " - "+str(products[index].price * number))
Badd = Button(win, text ="+", command = ButtonAdd)
Badd.grid(row=1, column=1 ,pady = 5,padx = 5)
#______________________________________

def Buttondel():
    choos = listbox2.curselection()
    if len(choos) == 0:
        sendpopup("pleas choos from listbox")
        return
    choos = choos[0]
    name = listbox2.get(choos).split('-')[0][:-1]
    for i in products:
        if i.name == name:
            i.choos = False
    selected.pop(choos)
    listbox2.delete(choos)
    viewSelcted.pop(choos)
Bdic = Button(win, text ="-", command = Buttondel)
Bdic.grid(row=2, column=1 ,pady = 5,padx = 5)
#______________________________________
def ButtonCalc():
    print(selected)

    popup = Tk()
    popup.wm_title("verify")

    listbox3 = Listbox(popup, height=Hlistbox,
                       width=Wlistbox,
                       bg="white",
                       activestyle='dotbox',
                       font="Helvetica",
                       fg="black")
    for i in viewSelcted:
        listbox3.insert(1000, i)
    listbox3.grid(row=0, column=0, pady=5, padx=5)
    total = 0
    for i in selected:
        total = total + i[1] * i[2]
    label10 = Label(master=popup, text="total= " + str(total))
    label10.grid(row=1, column=0, pady=5)

    B1 = ttk.Button(popup, text="continu shoping", command=popup.destroy)
    B1.grid(row=0, column=1, pady=5)

    B2 = ttk.Button(popup, text="buy", command=UpdateDB)
    B2.grid(row=1, column=1, pady=5)
    popup.mainloop()
#______________________________________
Bcalc = Button(win, text ="calc", command = ButtonCalc)
Bcalc.grid(row=3, column=1 ,pady = 5,padx = 5)

win.mainloop()
