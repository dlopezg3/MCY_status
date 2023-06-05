import importCsv as ic
import scrapper as scrapper
import pdb

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os.path

import csv

def get_mcy_status():
    
    chrome_options = scrapper.browser_setup()

    # # Set path to chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get("https://subsidiosfonvivienda.minvivienda.gov.co/micasaya/")

    with open("db/cedulas.csv", 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=';')
      header = next(reader)
      problems = []
      pr = len(problems)
      for row in reader:
        if pr < len(problems):
          browser = False
          pr = len(problems)
        if not browser:
          browser = scrapper.open_browser()
          browser.get("https://subsidiosfonvivienda.minvivienda.gov.co/micasaya/")
        cedula = row[0]
        scrapper.go_to_page(browser, cedula, problems)
      
      print("errores: ", problems)
      browser.close()
    
if __name__ == '__main__':
   get_mcy_status()
