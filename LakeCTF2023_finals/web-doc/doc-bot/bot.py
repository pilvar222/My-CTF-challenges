from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait(driver, sec):
  # I have coding skill issue so here's a time.sleep that doesn't freeze the browser
  try:
    WebDriverWait(driver, sec).until(
        EC.presence_of_element_located((By.ID, "substituteToSleepBcsIDKHowToCodeLol")))
  except:
    pass


def visit(url):
  chrome_options=webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(chrome_options=chrome_options)
  driver.get("http://doc-web:3000/")
  driver.add_cookie({"name": "flag", "value": os.environ['FLAG']})
  driver.get(url)
  wait(driver, 3)
  driver.quit()
