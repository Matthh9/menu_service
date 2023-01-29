# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 03:13:32 2022

@author: MADASILV
"""

### appel de l'interface les déclenchement fournisseur IPTV

import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QInputDialog, QLineEdit, QApplication, QMessageBox 

import pyperclip as pc

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

### utilsé pour transformer en exe
from multiprocessing import Queue
import cffi


import programme_check_sig_orange
import programme_declenchement_iptv
import programme_traitement_alarmes
import gestionMdpOrf


global mdp_orf


##############################################################################
### DECLARATION DES CLASS ET DES FONCTIONS
##############################################################################

#menu principal
MainFile = "IHM_main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainFile)

#IHM check sig orf
FileCheckOrf = "IHM_check_sig_orf.ui" 
Ui_WindowCheckOrf,_ = uic.loadUiType(FileCheckOrf)

#IHM déclenchement fournisseur
fileDeclenchement = "IHM_declenchement_IPTV.ui" 
Ui_WindowDeclenchement,_ = uic.loadUiType(fileDeclenchement)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.buttonDecIptv.clicked.connect(self.OpenWindowDeclenchement)
        self.buttonCheckSigOrf.clicked.connect(self.OpenWindowCheckOrf)
        self.buttonAlarmes.clicked.connect(self.TraitementAlarmes)
        self.buttonAlarmesDCM.clicked.connect(self.TraitementAlarmesDCM)
        self.changerMDPORF.clicked.connect(self.changementMdp_ORF)
  
    
    
    def changementMdp_ORF(self):
        global mdp_orf
        self.dialog_passwrd = QInputDialog()
        self.dialog_passwrd.resize(300, 100)
        self.dialog_passwrd.setWindowTitle("Changement MDP ORF")
        self.dialog_passwrd.setLabelText("Mot de passe ESAV ORF :")
        self.dialog_passwrd.setTextEchoMode(QLineEdit.Password)
        ok = self.dialog_passwrd.exec_()
        if ok:
            mdp_orf=self.dialog_passwrd.textValue()
            gestionMdpOrf.changement_MDP_ORF(bytes(mdp_orf, encoding='utf-8'))
        else:
            mdp_orf = ''
        del(self.dialog_passwrd)
    

    def changementLabel(self):
        self.etat.setText("")

    def OpenWindowCheckOrf(self):
        try:
            self.anotherwindow = WindowCheckOrf()
            self.anotherwindow.show()
        except:
            self.etat.setText("Erreur lors du check de la sig")
            QTimer().singleShot(3000, self.changementLabel)
            pass  
        
        
    def OpenWindowDeclenchement(self):
        try:
            self.anotherwindow = WindowDeclenchement()
            self.anotherwindow.show()
        except:
            self.etat.setText("Erreur lors du déclenchement fournisseur")
            QTimer().singleShot(3000, self.changementLabel)
            pass  
        
    def TraitementAlarmes(self):
        try:
            pc.copy(programme_traitement_alarmes.traitementAlarmesGenerales(pc.paste()))
            self.etat.setText("Traitement Fait\nRésultat dans presse papier")
            QTimer().singleShot(3000, self.changementLabel)
        except:
            self.etat.setText("Erreur donnée non reconnue")
            QTimer().singleShot(3000, self.changementLabel)
            pass  
        
    def TraitementAlarmesDCM(self):
        try :
            pc.copy(programme_traitement_alarmes.traitementAlarmesDCM(pc.paste()))
            self.etat.setText("Traitement Fait\nRésultat dans presse papier")
            QTimer().singleShot(3000, self.changementLabel)
        except:
            self.etat.setText("Erreur donnée non reconnue")
            QTimer().singleShot(3000, self.changementLabel)
            pass        



class WindowCheckOrf(QtWidgets.QMainWindow, Ui_WindowCheckOrf):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_WindowCheckOrf.__init__(self)
        self.setupUi(self)

        #close the window
        self.goCheckSigOrf.clicked.connect(self.Close)

    def Close(self):
        programme_check_sig_orange.check_sig(mdp_orf, self.valSig.text())
        self.close()



class WindowDeclenchement(QtWidgets.QMainWindow, Ui_WindowDeclenchement):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_WindowDeclenchement.__init__(self)
        self.setupUi(self)

        self.TDR.addItems(programme_declenchement_iptv.rechercheListePartenaire())
    
        #close the window
        self.declenchement_partenaire.clicked.connect(self.declenchement)
        self.TDR.currentIndexChanged.connect(self.changementTDR)
        
        

    def declenchement(self):
        retour=[]
        retour.append(self.numeroTT.toPlainText())
        retour.append(self.TDR.currentText())
        retour.append(self.chaine.toPlainText())
        retour.append(self.zap.toPlainText())
        retour.append(self.probleme.toPlainText())
        retour.append(self.commentaire.toPlainText())
        retour.append(self.type_incident.currentText())
        retour.append(self.qualite.currentText())
        programme_declenchement_iptv.traitement_general_declenchement_iptv(retour, mdp_orf)
        self.close()


    #fonction permettant de griser la partie type zap et qualité propre a orange lorsque une autre TDR est sélectionnée
    def changementTDR(self):
        index=self.TDR.currentText()
        if(index=="GCF"):
            # self.infoComplementaireOrange.show()
            self.infoComplementaireOrange.setEnabled(True)
        else:
            # self.infoComplementaireOrange.hide()
            self.infoComplementaireOrange.setEnabled(False)



##############################################################################
### GENERAL
##############################################################################
if __name__ == "__main__":
    app = 0 # if not the core will die
    app = QtWidgets.QApplication(sys.argv)
    
    
    # from selenium import webdriver
    ### check de prerequis pour l'utilisation du script notamment webdriver
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    ###check si la version de webdriver est bonne
    try:
        driver=Chrome(options=chrome_options)
    except Exception as err:
        if ("This version of ChromeDriver only supports Chrome version" in  err.msg):    
            version = err.msg.split("Current browser version is ")[1].split(".")[0]
            message = """<p>La version de webdriver n'est pas supportée pour cette version de chrome.</p>
<p>Il faut télécharger la nouvelle version sur la page :</p>
    <a href='https://chromedriver.chromium.org/downloads'>https://chromedriver.chromium.org/downloads</a>
<p>Il faut suivre le lien pour la version {}, ensuite télécharger le dossier chromedriver_win32.zip, le décompresser et remplacer celui existant dans le dossier du programme par le nouveau.</p>
            """.format(version)
            
            programme_declenchement_iptv.messageErreur(message, "Erreur avec la version du webdriver")
        else:
            programme_declenchement_iptv.messageErreur("Erreur inconnue contacter le SAV", "Erreur inconnue")
    else:
        driver.close()
        
        
    ### lecture du fichier avec le mdp orf
    mdp_orf=gestionMdpOrf.lire_MDP_ORF()
    
    


    window = MainWindow()
    window.show()
    sys.exit(app.exec_())