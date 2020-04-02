import pymongo
from PyQt5 import QtWidgets,uic,QtCore,QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox


def add_user(i):
    with pymongo.MongoClient("mongodb://localhost:27017/") as client:
        db = client["Database"]
        item = db["customers"].insert_one(i)
        return item.inserted_id

def valte_user(i):
    with pymongo.MongoClient("mongodb://localhost:27017/") as client:
        db = client["Database"]
        item = db["customers"].find_one(i["key"])
        try:
            if(item["key"]==i["key"]):
                print("sucess")
                pui.show()
        except:
            QMessageBox.about( ui,"Warning", "Wrong Username or Password")

def add_ent():
    print("btn conn")
    username=ui.UserlineEdit.text()
    print(username)
    password=ui.PasslineEdit.text()
    print(password)
    ke=username+password
    cred={"User":username,"Pass":password,"key":ke}
    print(add_user(cred))
#my_dict={"name":"James Bond","address":"Gzb"} 

#x=mycol.insert_one(my_dict)

#print(x.inserted_id)

def chek_ent():
    print("btn conn sgb")
    username=ui.UserlineEdit.text()
    print(username)
    password=ui.PasslineEdit.text()
    print(password)
    cred={"key":username+password}
    print(cred["key"])
    valte_user(cred)

app=QtWidgets.QApplication([])
ui=uic.loadUi("logincred.ui")
pui=uic.loadUi("data.ui")


ui.supButton.clicked.connect(add_ent)
ui.sinButton.clicked.connect(chek_ent)
#ui.setWindowIcon(QtGui.QIcon("download.png"))
#ui.setWindowTitle("Our calculator")

pui.show()
ui.show()
app.exec_()
