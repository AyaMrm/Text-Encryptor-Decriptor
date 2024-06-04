import tkinter as tk
import secrets
import math 

# Vérifier si le nombre est premier 
def prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    else:
        sqrtn = math.isqrt(n) + 1
        
    for i in range(3, sqrtn, 2):
        if n % i == 0:
            return False
    return True
    
# Trouver le p et le q 
def trouverPQ(n):
    p = 0
    q = 0
    for i in range(2, int(n) // 2 + 1):
        if n % i == 0:
            if prime(i) and prime(n//i):
                p = i
                q = n // i
                break
    return p, q 

# Déterminer le d (exposant privé)( pas importance )
def leD(n):
    dBinaire = secrets.randbits(3072)
    nBits = n.bit_length()
    dBits = dBinaire.bit_length()
    v = True
    if nBits != dBits:
        print("Error! ")
        v = False
    else:
        D = int(dBinaire)
        return D, v

# La fonction d'Euler 
def euler(p, q):
    fi = (p - 1) * (q - 1)
    return fi

# Calculer PGCD 
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Vérifier le e 
def leE(e, fi):
    PGCD = pgcd(e, fi)
    resultat = True
    if e <= 1 or e >= fi or PGCD != 1:
        print("Error! ")
        resultat = False
    return resultat

# Algorithme d'Euclide étendu 
def Euclide(e, fi):
    if e == 0:
        return fi, 0, 1 
    else:
        s, y, x = Euclide(fi % e, e)
        return s, x - (fi // e) * y, y 
    
def modularInverse(e, fi):  # t est le fi
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

# Fonction pour crypter 
def Crypter(message_text, e, n):
    try:
        # Choix des nombres premiers 
        p, q = trouverPQ(n)
        # Calculer la fonction d'Euler 
        fi = euler(p, q)
        # Vérifier le e
        if not leE(e, fi):
            return "Error ! e invalid"
        
        # Calculer la clé privée 
        d = modularInverse(e, fi)
        clePrive = (e, n)
        
        # Convertir le message en ASCII
        asciiMessage = asciiEncode(message_text)
        for i in range(len(asciiMessage)):
             asciiMessage[i] = pow(asciiMessage[i], e, n)
        
        # Convertir ASCII en texte
        textCrypter = asciiToLettre(asciiMessage)
        return textCrypter
    except Exception as ex:
        print(f"Cryptage error : {ex}")
        return "Cryptage error."

# fontion pour decrypter 
def Decrypter (message, d, n):
    try:
        # convertir le message en ASCII 
        asciiMessage = asciiEncode(message)
        for i in range(len(message)):
            asciiMessage[i] = pow(asciiMessage[i], d, n)
        #convertir ASCII en texte 
        textDecrypter = asciiToLettre(asciiMessage)
        return textDecrypter 
    except Exception as ex:
        print(f"Decryptage Error! : {ex}")
        return "Decryptage error"
    
    


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
labelCle = tk.Label(root, text="Enter the public/private key (e/d, n) : ")
labelCle.pack()

frameCle = tk.Frame(root)
frameCle.pack()

labelE = tk.Label(frameCle, text="e : ")
labelE.grid(row=0, column=0, padx=5, pady=5)
E = tk.Entry(frameCle, width=20)
E.grid(row=0, column=1, padx=5, pady=5)

labelN = tk.Label(frameCle, text="n : ")
labelN.grid(row=0, column=2, padx=5, pady=5)
N = tk.Entry(frameCle, width=20)
N.grid(row=0, column=3, padx=5, pady=5)

# affichage de texte crypte
def affichageCry():
    textCrypted = Crypter(message.get(), int(E.get()), int(N.get()))
    labelResult.config(text="Crypted text : " + textCrypted)

# affichage de texte decrypter 
def affichageDec():
    textDecrypted = Decrypter(message.get(), int(E.get()), int(N.get()))
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