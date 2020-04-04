import pymongo
from PyQt5 import QtWidgets,uic,QtCore,QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from pymongo import MongoClient
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import pymongo
gkey=''
passkey=''
def conn():
    # Create MONGO_SUPERUSER and MONGO_SUPERPASS global varaible in local environment for MongoDB
    connection = MongoClient(
        f"mongodb://localhost:27017/?authSource=admin&readPreference=primary&ssl=false",
        socketTimeoutMS=900000)
    return connection

def keygen (i,j): 
    # Here i is the string for which key is being genrated(password)
    # j is the string using which key for i is generated(username)
    i=i.encode()
    salt=j.encode()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(i)) # Can only use kdf once
    return key



def add_urlpass():
    global gkey
    client =conn()
    db = client.Database.customers
    f = Fernet(gkey)
    db.update_one({'_id':str(gkey)},{'$push':{'url':str(f.encrypt(pui.Url.text().encode()))}},upsert=True)
    db.update_one({'_id':str(gkey)},{'$push':{'user':str(f.encrypt(pui.U_Eid.text().encode()))}},upsert=True)
    db.update_one({'_id':str(gkey)},{'$push':{'pass':str(f.encrypt(pui.PassUrl.text().encode()))}},upsert=True)
    client.close()
    pui.Url.setText("")
    pui.U_Eid.setText("")
    pui.PassUrl.setText("")

def prnt_rec():
    pui.stack.setCurrentIndex(0)
    global gkey
    client =conn()
    db = client.Database.User_data
    p=db.find_one({'_id':gkey})
    urlis=p['url']
    uslis=p['user']
    plis=p['pass']
    f = Fernet(gkey)
    pui.table.setColumnCount(3)
    pui.table.setRowCount(len(urlis))
    i=0
    while(i<len(urlis)):
        pui.table.setItem(i, 0, QtWidgets.QTableWidgetItem(f.decrypt(urlis[i].decode()).decode()))
        pui.table.setItem(i, 1, QtWidgets.QTableWidgetItem(uslis[i]))
        pui.table.setItem(i, 2, QtWidgets.QTableWidgetItem(plis[i]))
        i+=1

def add_ent():
    username=ui.UserlineEdit.text()
    password=ui.PasslineEdit.text()
    key=keygen(password,username)
    #enc_cred = Fernet(gkey).encrypt(username+password)
    client =conn()
    db = client.Database.customers
    db.insert_one({'_id':str(key)})

def chek_ent():
    global gkey
    pui.stack.setCurrentIndex(1)
    username=ui.UserlineEdit.text()
    password=ui.PasslineEdit.text()
    key=keygen(password,username)
    client =conn()
    db = client.Database.customers
    item = db.find_one({'_id':str(key)})
    print(item)
    try:
        if(not item==None):
            print("sucess")
            gkey=key
            print(gkey)
            pui.show()
            ui.close()
    except:
        QMessageBox.about( ui,"Warning", "Wrong Username or Password")


app=QtWidgets.QApplication([])
ui=uic.loadUi("logincred.ui")
pui=uic.loadUi("data.ui")


ui.supButton.clicked.connect(add_ent)
ui.sinButton.clicked.connect(chek_ent)
pui.AddButton.clicked.connect(add_urlpass)
pui.VSPButton.clicked.connect(prnt_rec)
#ui.setWindowIcon(QtGui.QIcon("download.png"))
#ui.setWindowTitle("Our calculator")

ui.show()
app.exec_()

