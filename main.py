import time as t
import os
import pyautogui
from pytesseract import pytesseract
from utils import get_total_price
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup
download_dir = "C:/Users/Joseph/Downloads"
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# Filter out directories, leave only files
download_dir_files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
last_download_name = max(download_dir_files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x))).lower()

total = get_total_price(last_download_name, download_dir, path_to_tesseract)
if float(total) > 0.0:

    # Initialize Web Driver
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:/Users/Joseph/AppData/Local/Google/Chrome/User Data")

    driver = webdriver.Chrome(service=Service(r"C:\Users\Joseph\chromedriver-win64\chromedriver.exe"), options=options)

    driver.get('https://www.grubhub.com/account/history?'
               'pageNum=1&pageSize=20&facet=scheduled%3Afalse&facet=orderType%3AALL&sorts=default')

    wait = WebDriverWait(driver, 20)


    # Run Automation
    button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/ghs-site-container/span/div/div[3]/div/span/'
                                                                  'div/ghs-router-outlet/div/div/div[2]/span/span/div/span/'
                                                                  'div[2]/div/div[2]/div/div[1]/div/span/div/div[2]/div[5]/'
                                                                  'div/button')))
    button.click()
    button = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="receipt-body"]/div[4]/div/div[3]/div/div/div[2]/div[2]/a')))
    button.click()
    button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="safeHtmlWrapper1"]/span')))
    button.click()
    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div/span/div/div/div/div/div[2]/span[2]/button')))
    button.click()
    button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="OTHER"]')))
    button.click()
    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div/span/div/div/div/div/form/div[2]/span/button')))
    button.click()

    textbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="total"]')))
    textbox.send_keys(total)
    t.sleep(2)

    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div/span/div/div/div/div/form/div[2]/span/button')))
    button.click()

    # Open the file explorer dialog
    file_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div/'
                                                                        'span/div/div/div/div/form/div[1]/div/div[3]/div/'
                                                                        'div/label/span')))
    file_input.click()

    t.sleep(1)
    # Type the file path into the file name field
    pyautogui.write(last_download_name)

    # Press enter to upload the file
    pyautogui.press('enter')

    t.sleep(8)

    # submit button DO NOT uncommment
    # button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div/div/span/div/div/div/div/form/div[2]/span/button')))
    # button.click()

    t.sleep(25)

else:
    raise ValueError("No total found")

#make definitions, add to github, add fucntion calls