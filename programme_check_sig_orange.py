# -*- coding: utf-8 -*-
"""
@author: MADASILV

"""
    
from selenium.webdriver import Chrome

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

##############################################################################
### DECLARATION DES CLASS ET DES FONCTIONS
##############################################################################


def check_sig(mdp, numeroTT):
    
    url_fournisseur="URL"
    user="user"
    
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver=Chrome(options=chrome_options)
    
    driver.get("url_fournisseur")
    driver.find_element_by_id("username").send_keys(user)
    ## pour les 2 cas de l'interface de connexion orange...
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
    driver.find_element_by_partial_link_text('Liste des signalisations').click()
    driver.find_element_by_name("numFt").send_keys(numeroTT)
    driver.find_element_by_name('action').click()
       
    driver.find_element_by_xpath("//table[@class='grid']/tbody[@class='grid']/tr/td/a").click()