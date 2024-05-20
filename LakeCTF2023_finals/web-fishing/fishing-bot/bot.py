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

def visit(postId):
  chrome_options=webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(chrome_options=chrome_options)
  driver.get("http://fishing-web:3000/posts/"+postId)
  wait(driver, 3)
  driver.execute_script('document.querySelectorAll("a").forEach(a => {if (a.innerText == "[Login to view this content]") {a.click(); return}})')
  wait(driver, 3)
  if not driver.current_url.endswith("/login"):
    driver.quit()
    return
  usernameEl = driver.find_element_by_id("username")
  usernameEl.send_keys(os.environ['MODERATOR_USERNAME'])
  passwordEl = driver.find_element_by_id("password")
  passwordEl.send_keys(os.environ['MODERATOR_PASSWORD'])
  butEl = driver.find_element_by_id("submitbut")
  butEl.click()
  wait(driver, 10)
  driver.quit()
