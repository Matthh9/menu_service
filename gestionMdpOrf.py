# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 07:49:32 2022

@author: MADASILV
"""

"""
Programme simple pour chiffrer le mot de passe permettant l'accès à l'interface du fournisseur
Le mot de passe est chiffré pour être stocké dans un fichier txt et est déchiffré lorsqu'on veut accéder à l'espace
de cette mnaière l'utilisateur n'a pas besoin de le taper à chaque fois
"""

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

nom_fichier_mdp_orf="mdp_orf.txt"


def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding


#le programme est distribué sous forme d'executable la clé peut être laissé en clair dedans
#une autre possibilité est de récupérer par python des variables du pc comme son numéro et le logging de l'utilisateur afin d'avoir une clé unique pour le chiffrement
cle_chiffrement = b"secret_AES_key_string_to_encrypt/decrypt_with"

# print("key:  {}".format(cle_chiffrement))
# print("data: {}".format(my_data))
# encrypted = encrypt(cle_chiffrement, my_data)
# print("\nenc:  {}".format(encrypted))
# decrypted = decrypt(cle_chiffrement, encrypted)
# print("dec:  {}".format(decrypted))


def lire_MDP_ORF():
    file = open(nom_fichier_mdp_orf, "r")
    mdp = file.readlines()[0]
    file.close()
    return(decrypt(cle_chiffrement, mdp).decode("utf-8"))


def changement_MDP_ORF(mdp):
    file = open(nom_fichier_mdp_orf, "w")
    file.write(encrypt(cle_chiffrement, mdp))
    file.close()
    
    
# var = "test de mdp 123456"
# changement_MDP_ORF(bytes(var, encoding='utf-8'))
# print(lire_MDP_ORF())