# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
import random
import math
from sympy import isprime;
from textwrap import wrap
 

app =QtWidgets.QApplication([])
dlg = uic.loadUi("RSA.ui")

#generate a random integer between 10e16 and 10e17-1 
def Get_prime():
    a=random.randint(10**16,(10**17)-1)
    while (isprime(a)==False):
        a-=1
    return a
#generate d
def Get_d(e,phi):
     return pow(e,-1,phi)
#generate e
def Get_e(phi):
    e=random.randint(1,phi)
    while (math.gcd(e, phi)!=1) :
        e-=1
    return e
#generate all the key pairs (n and d , n and e)
def Generate_Key_pair():
    p=Get_prime()
    q=Get_prime()
    n=p*q
    phi = (p-1)*(q-1)
    e=Get_e(phi)
    d=Get_d(e, phi)
    dlg.lineEdit_Private_N.setText(str(n))
    dlg.lineEdit_Private_D.setText(str(d))
    dlg.lineEdit_Public_N.setText(str(n))
    dlg.lineEdit_Public_E.setText(str(e))
#Encrypt the plain text to cipher text
def Encrypt():
    dlg.textEdit_New_Text.setText("")
    dlg.label_Blablabla.setText("")
    message = dlg.textEdit_Type_Text.toPlainText()
    try :
        message_array=list(message)
        for x in range(len(message_array)) :
            message_array[x]='{0:08b}'.format(ord(message_array[x]))
        finished_array=[]
        for x in range(0,len(message_array),6):#7 is the step (each block is 7 char long)
            finished_array.append(message_array[x:x+6])
        message_ascii_array=[]
        temporary=""
        for x in range(len(finished_array)):               
            temporary+=(str(finished_array[x])).replace('[' ,'').replace(']' ,'').replace("'" ,'').replace(' ' ,'').replace(',' ,'')
            if(len(temporary)==48 or x-len(finished_array)<5):
                message_ascii_array.append(int(temporary,2))
                temporary=""
        new_text=""
        for x in range(len(message_ascii_array)):        
            new_text+=(str(pow(message_ascii_array[x],int(dlg.lineEdit_Public_E.text()),int(dlg.lineEdit_Public_N.text()))))+" "
            dlg.textEdit_New_Text.setText(new_text)
    except :
        dlg.label_Blablabla.setText("N and E should be numbers")
#Decrypt the cipher text into plain text
def Decrypt():
    dlg.textEdit_New_Text.setText("")
    message = dlg.textEdit_Type_Text.toPlainText()
    try:
        message_array = message.split()
        for x in range(len(message_array)):
            message_array[x]="{0:b}".format(pow(int(message_array[x]),int(dlg.lineEdit_Private_D.text()),int(dlg.lineEdit_Private_N.text())))
            while(len(message_array[x])%8!=0):
                    message_array[x]='0'+message_array[x]
        result=""
        message_value=[]
        for x in range(len(message_array)):
            for y in range(0,len(message_array[x]),8):
                message_value+=wrap(str(message_array[x][y:y+8]))
        for x in range(len(message_value)):
            result+=chr(int(message_value[x],2))
        dlg.textEdit_New_Text.setText(result)
    except:
        dlg.label_Blablabla.setText("N and E should be numbers and so does your text")

dlg.pushButton_Generate_Keys.clicked.connect(Generate_Key_pair)
dlg.pushButton_Encrypt.clicked.connect(Encrypt)
dlg.pushButton_Decrypt.clicked.connect(Decrypt)

if __name__=="__main__":
    #open the application
    dlg.show()
    app.exec()

"""
label_Title
label_Blablabla
label_Type_Text
label_New_Text
pushButton_Generate_Keys
pushButton_Encrypt
pushButton_Decrypt
label_Private_Key
label_Public_Key
Public_N_Label
Public_E_Label
Private_N_Label
Private_D_Label
lineEdit_Private_N
lineEdit_Private_D
lineEdit_Public_N
lineEdit_Public_E
textEdit_New_Text
textEdit_Type_Text
"""