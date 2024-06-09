import tkinter as tk 
import secrets 
import math 
import random

# en prend p, q comme input 

# Calculer PGCD 
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#calculer n 
def calculeN(p,q ):
    n = p*q
    return n 

#fonction d'euler 
def euler(p,q):
    fi = (p-1)*(q-1)
    return fi 

#choisir un e qui convient 
def choisirE(fi):
    v = False
    while v==False :
        e = random.randint(2, fi)
        if pgcd(e, fi)== 1 :
            v =True
    return e 


# Algorithme d'Euclide étendu 
def Euclide(e, fi):
    if e == 0:
        return fi, 0, 1 
    else:
        s, y, x = Euclide(fi % e, e)
        return s, x - (fi // e) * y, y 

# calculer le d 
def modularInverse(e, fi):  
    g, x, y = Euclide(e, fi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % fi

# Encoder un message en ASCII
def asciiEncode(message):
    asciiMessage = []
    for char in message:
        asciiMessage.append(ord(char))
    return asciiMessage
        
# De ASCII vers lettre 
def asciiToLettre(asciiMessage):
    textCrypter = ''
    for i in range(len(asciiMessage)):
        textCrypter += chr(asciiMessage[i])
    return textCrypter


# crypter un message 
def Crypter(message, p, q):
    #trouver le e 
    n= calculeN(p,q)
    fi= euler(p,q)
    e = choisirE(fi)
    
    # Convertir le message en ASCII
    asciiMessage = asciiEncode(message)
    for i in range(len(asciiMessage)):
        asciiMessage[i] = pow(asciiMessage[i], e, n)
        
    # Convertir ASCII en texte
    textCrypter = asciiToLettre(asciiMessage)
    return textCrypter

# decrypter un messsage 
def Decrypter(message, p,q):
    #calculer le d 
    n = calculeN(p,q)
    fi=euler(p,q)
    e = choisirE(fi)
    d = modularInverse(e, fi)
    
    # Convertir le message en ASCII
    asciiMessage = asciiEncode(message)
    for i in range(len(asciiMessage)):
        asciiMessage[i] = pow(asciiMessage[i], d, n)
        
    # Convertir ASCII en texte
    textCrypter = asciiToLettre(asciiMessage)
    return textCrypter



# Interface graphique 
root = tk.Tk()
root.title("Text Cryptor / Decryptor")
root.geometry("500x300")
root.resizable(False, False)

# Label pour le message
labelMessage = tk.Label(root, text=" Enter the text to encrypt/decrypt: ")
labelMessage.pack()

message = tk.Entry(root, width=50)
message.pack()

# Label pour la cle publique
labelCle = tk.Label(root, text="Enter p and q  : ")
labelCle.pack()

frameCle = tk.Frame(root)
frameCle.pack()

labelp = tk.Label(frameCle, text="p : ")
labelp.grid(row=0, column=0, padx=5, pady=5)
p = tk.Entry(frameCle, width=20)
p.grid(row=0, column=1, padx=5, pady=5)

labelq = tk.Label(frameCle, text="q : ")
labelq.grid(row=0, column=2, padx=5, pady=5)
q = tk.Entry(frameCle, width=20)
q.grid(row=0, column=3, padx=5, pady=5)

# affichage de texte crypte
def affichageCry():
    textCrypted = Crypter(message.get(), int(p.get()), int(q.get()))
    labelResult.config(text="Crypted text : " + textCrypted)

# affichage de texte decrypter 
def affichageDec():
    textDecrypted = Decrypter(message.get(), int(p.get()), int(q.get()))
    labelResult.config(text="Decrypted text :"+ textDecrypted )
    
# Button pour Crypter
buttonCrypter = tk.Button(root, text="Crypter", width=10, height=2, command=affichageCry)
buttonCrypter.pack()
buttonCrypter.place(x=50, y=120)

# Button pour Decrypter 
buttonDecrypter = tk.Button(root, text="Decrypter", width= 10, height=2, command=affichageDec)
buttonDecrypter.pack()
buttonDecrypter.place(x=200, y=120)

# Label pour afficher le résultat
labelResult= tk.Label(root, text="")
labelResult.pack()

root.mainloop()