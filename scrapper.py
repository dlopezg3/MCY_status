# import download_checker as downc

import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pdb

def go_to_page(browser, cedula, problems):
    if not browser:
      open_browser()
      browser.get("https://subsidiosfonvivienda.minvivienda.gov.co/micasaya/")

    ## Start navigation
    try: 
      assert "Consulta Hogar - Ministerio de Vivienda, Ciudad y Territorio" in browser.title
    except AssertionError as e:
      print("No se encuentra la página correcta")
    except NoSuchElementException:
       print("-")
    
    try:
       Select(browser.find_element(By.ID, 'cbTipoIdentificacion')).select_by_value("1")
       browser.find_element(By.ID, "txtIdentificacion").send_keys(cedula)
       browser.find_element(By.CLASS_NAME, "btn-mcy").submit()

       status_box = WebDriverWait(browser, 10).until(
          EC.presence_of_element_located((By.ID, "swal2-title"))
        )
    except TimeoutException as e:
       print(f"Error al buscar - {cedula}")
       problems.append(cedula)
       browser.close()
       return problems
       
    try: 
        status = browser.find_element(By.XPATH, "//h2[@id='swal2-title']/span[1]/span[1]").text
    
    except NoSuchElementException:
       try:
          status = browser.find_element(By.XPATH, "//h2[@id='swal2-title']/span[1]").text
       except:
          print(f"No se encuentra uno de los elementos - {cedula}")
          browser.close()
          problems.append(cedula)
          return problems
          
          
    print(cedula + "," + status)
    browser.refresh()

    


def browser_setup():
    ## Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # Abriendo explorador
    # chrome_options.add_argument("--headless=new") # Sin explorador

    chrome_options.add_experimental_option("prefs", {
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })

    return chrome_options

def open_browser():
    chrome_options = browser_setup()

    # # Set path to chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

    return webdriver.Chrome(service=webdriver_service, options=chrome_options)
      
     
if __name__ == '__main__':
    ## Setup chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--no-sandbox") # Abriendo explorador
    chrome_options.add_argument("--headless=new") # Sin explorador

    chrome_options.add_experimental_option("prefs", {
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })
   
    ## Choose Chrome Browser
    # Set path to chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")
    
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    cedula = "1047406265"
    go_to_page(browser, cedula)
    browser.close()