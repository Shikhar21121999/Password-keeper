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

def bk ():
    global gkey
    gkey=''
    print('s',gkey)
    ui.UserlineEdit.setText("")
    ui.PasslineEdit.setText("")
    pui.hide()
    ui.show()
    
def addmore():
    pui.stack.setCurrentIndex(1)

def add_urlpass():
    global gkey
    pui.stack.setCurrentIndex(1)
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
    print(gkey)
    client =conn()
    db = client.Database.customers
    p=db.find_one({'_id':str(gkey)})
    print(p)
    try:
        urlis=p['url']
        uslis=p['user']
        plis=p['pass']
        f = Fernet(gkey)
        pui.table.setColumnCount(3)
        pui.table.setRowCount(len(urlis))
        i=0
        pui.table.setHorizontalHeaderLabels(['Url', 'Username', 'Password'])

        while(i<len(urlis)):
            p=urlis[i]
            q=uslis[i]
            r=plis[i]
            p=(f.decrypt(p[2:len(p)].encode())).decode()
            q=(f.decrypt(q[2:len(q)].encode())).decode()    
            r=(f.decrypt(r[2:len(r)].encode())).decode()
            pui.table.setItem(i, 0, QtWidgets.QTableWidgetItem(p))
            pui.table.setItem(i, 1, QtWidgets.QTableWidgetItem(q))
            pui.table.setItem(i, 2, QtWidgets.QTableWidgetItem(r))
            i+=1
    except:
        QMessageBox.about( ui,"Warning", 'Nothing To Display')

def add_ent():
    username=ui.UserlineEdit.text()
    password=ui.PasslineEdit.text()
    if(len(username)<7 or len(password)<6):
        QMessageBox.about( ui,"Warning", "Unacceptable username or password")
    else:
        key=keygen(password,username)
        client =conn()
        db = client.Database.customers
        try:
            db.insert_one({'_id':str(key)})
        except:
            QMessageBox.about( ui,"Username Taken", "Either sign in or take other username")

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
    if(not item==None):
        print("sucess")
        gkey=key
        print(gkey)
        pui.show()
        ui.hide()
    else:
        QMessageBox.about( ui,"Warning", "Wrong Username or Password")


app=QtWidgets.QApplication([])
ui=uic.loadUi("logincred.ui")
pui=uic.loadUi("data.ui")
ui.setWindowIcon(QtGui.QIcon("image.jpg"))
ui.setWindowTitle("Password Keeper")
pui.setWindowTitle("Password Keeper")
#493a27;
stylesheet = """

QMainWindow{
    Background-color : #c47806;
}
QPushButton{
    color:#88ac1a;
    background-image: url(button.jpeg);
}
QLabel{
    Background-color:#25120a;
    color:#dc4301;
    padding: 2px;
    text-align: center;
}
QLineEdit{
    Background-color:#e8a357;
}
"""
app.setStyleSheet(stylesheet)
ui.supButton.clicked.connect(add_ent)
ui.sinButton.clicked.connect(chek_ent)
pui.AddButton.clicked.connect(add_urlpass)
pui.VSPButton.clicked.connect(prnt_rec)
pui.SignoutButton.clicked.connect(bk)
pui.Signout1Button.clicked.connect(bk)
pui.AddmoreButton.clicked.connect(addmore)

#ui.setWindowTitle("Our calculator")
ui.show()
app.exec_()

