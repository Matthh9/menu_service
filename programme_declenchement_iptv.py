# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 18:26:05 2020

@author: Matthieu
"""


global retour


##############################################################################
### DECLARATION DES CLASS ET DES FONCTIONS
##############################################################################
def envoiMail(destinataire, objet, corps, cc):
    email_source = "email@source.fr"
    
    from win32com.client import Dispatch
    Outlook = Dispatch('Outlook.application')
    mail = Outlook.CreateItem(0)
    mail.SentOnBehalfOfName=email_source
    mail.To = destinataire
    mail.CC = email_source+cc
    mail.Subject = objet
    mail.GetInspector

    index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body'))
    mail.HTMLbody = mail.HTMLbody[:index + 1] + corps + mail.HTMLbody[index + 1:]

    mail.Display(True)



def preparationEnvoiMail(ticket, chaine, probleme, commentaire, destinataire, cc):
    objet = "["+ticket+"] - chaine " + chaine + " - " + probleme
    corps = "Bonjour, <br><br>Nous constatons le problème suivant : " + probleme+" sur la(les) chaine(s) : " + chaine+"."
    if (commentaire!=""):
        corps+="<br>Information complémentaire : "+commentaire
    corps+="<br>Nous avons ouvert l’incident : "+ticket+".<br><br>Pouvez-vous investiguer sur la cause de ce problème ?"

    envoiMail(destinataire, objet, corps, cc)



def rechercheListePartenaire():
    from csv import reader
    partenaire=[]
    
    with open('partenaire.csv') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')
        for row in csv_reader:
            partenaire.append(row[0])
    
    return partenaire[1:]



def rechercheMailPartenaire(partenaire):
    from csv import reader
    
    with open('partenaire.csv') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')

        for row in csv_reader:
            if (partenaire in row):
                return row[1],row[2]

    return ["",""]



def declenchementOrange(mdp, numeroTT, chaine, zap, probleme, commentaire, typeIncident, qualite):
    url_fournisseur="URL"
    user="user"
    num_telephone="0100000000"
    prestation="prestation"
    
    
    from selenium.webdriver import Chrome
    
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException

    driver = Chrome()
    
    driver.get(url_fournisseur)
    driver.find_element_by_id("username").send_keys(user)
    ## pour les 2 cas de l'interface de connexion de l'ihm
    try:
        driver.find_element_by_id("password").send_keys(mdp)
        driver.find_element_by_id("submit-button").click()
    except:
        driver.find_element_by_id("submit-button").click()
        
        try:
            # Wait as long as required, or maximum of 60 sec for element to appear
            # If successful, retrieves the element
            element = WebDriverWait(driver,60).until(
                  EC.presence_of_element_located((By.ID, "currentPassword")))
        except TimeoutException:
            print("Echec chargement de la page")
    
        driver.find_element_by_id("currentPassword").send_keys(mdp)
        driver.find_element_by_id("submit-button").click()

    try:
        # Wait as long as required, or maximum of 60 sec for element to appear
        # If successful, retrieves the element
        element = WebDriverWait(driver,60).until(
             EC.presence_of_element_located((By.XPATH, "//form[@id='userDomainForm']/input[@type='submit']")))
    except TimeoutException:
        print("Echec chargement de la page")

    driver.find_element_by_xpath("//form[@id='userDomainForm']/input[@type='submit']").click()
    driver.find_element_by_partial_link_text('Dépôt de signalisation').click()
    driver.find_element_by_name("prestationId1").send_keys(prestation)
    driver.find_element_by_xpath("//div[@id='button']/input[@type='submit']").click()
    driver.find_element_by_partial_link_text('Suite dépôt').click()
    driver.find_element_by_xpath("//div[@id='button']/input[@type='submit']").click()

    #onglet informations générales
    driver.find_element_by_name("clientTicketId").send_keys(numeroTT)
    driver.find_element_by_name("depositorName").clear()
    driver.find_element_by_name("depositorName").send_keys("Bouygtel Service 3x8")
    driver.find_element_by_name("depositorPhoneNumber").clear()
    driver.find_element_by_name("depositorPhoneNumber").send_keys(num_telephone)

    #onglet informations complémentaires
    driver.find_element_by_partial_link_text('Informations complémentaires').click()
    driver.find_element_by_name('INFO_NON').click()
    driver.find_element_by_name('INFO_SAIS_PAS_VERIMATRIX').click()
    driver.find_element_by_xpath("//input[@name='INFO_DLAM_CONCERNE'][@value='ORANGE_BOUYGUES']").click()
    driver.find_element_by_name('INFO_FLUX_TV_OPE').click()
    driver.find_element_by_xpath("//input[@name='INFO_ADELIA'][@value='PAS_INCIDENT']").click()
    driver.find_element_by_name("INFO_ND_1").send_keys(num_telephone)

    #onglet Défauts constatés
    driver.find_element_by_partial_link_text('Défauts constatés').click()
    driver.find_element_by_name(typeIncident).click()
    driver.find_element_by_name(qualite).click()
    driver.find_element_by_name("DEFECT_LIBELLE_CHAINE").send_keys(chaine)
    driver.find_element_by_name("DEFECT_NUM_ZAP").send_keys(zap)
    driver.find_element_by_name("DEFECT_DESCRIPTION").send_keys(probleme)
    if(typeIncident=="DEFECT_INTERRUPTION"):
        driver.find_element_by_name("DEFECT_NATURE_INTERRUPTION").send_keys(probleme)
    elif(typeIncident=="DEFECT_DEGRADATION"):
        driver.find_element_by_name("DEFECT_NATURE_DEGRAD").send_keys(probleme)

    driver.find_element_by_name("description").send_keys(commentaire)
    driver.find_element_by_xpath("//*[@value='Déposer']").click()




def messageErreur(message, titre):
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtCore import Qt

    #il faut une app pour faire un widget messagebox, ici c'est fourni dans le main directement sinon il faut decommenter la ligne du dessous
    # appInterne = QApplication(sys.argv)
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setTextInteractionFlags((Qt.LinksAccessibleByKeyboard
                                    | Qt.LinksAccessibleByMouse
                                    | Qt.TextBrowserInteraction
                                    | Qt.TextSelectableByKeyboard
                                    | Qt.TextSelectableByMouse))
    msgBox.setTextFormat(Qt.RichText)
    msgBox.setWindowTitle(titre)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()



##############################################################################
### GENERAL
##############################################################################


def traitement_general_declenchement_iptv(retour, mdp_orf):
    if (retour[1]=="GCF"):
        #si on a orange déclenchement par l'interface
        #d'abord on modifie les informations pour aller avec les valeurs du site :
    
        #changement de la valeur de type incident par le nom du champ a cliquer correspondant
        if (retour[6]=="Interruption"):
            retour[6]="DEFECT_INTERRUPTION"
        elif (retour[6]=="Dégradation"):
            retour[6]="DEFECT_DEGRADATION"
        
        #pareil qu'au dessus mais pour la qualité
        if (retour[7]=="HD et SD"):
            retour[7]="SD_HD"
        retour[7]="DEFECT_TV_"+retour[7]
    
        declenchementOrange(mdp_orf, retour[0], retour[2], retour[3], retour[4], retour[5], retour[6], retour[7])
    
    else:
        #sinon on prépare un mail
        #lecture du fichier pour trouver le mail du partenaire
        destinataire=retour[1]
        if (destinataire!="Autre"):
            destinataire, cc = rechercheMailPartenaire(destinataire)
    
            if (destinataire == ""):
                messageErreur("Partenaire non trouvé dans le fichier des adresses mails.", "ERREUR partenaire")
                destinataire=""
                cc=""
        else : 
            destinataire=""
            cc=""
        preparationEnvoiMail(retour[0], retour[2], retour[4], retour[5], destinataire, cc)