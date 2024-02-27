import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def backup_OS_settings_current_UI_selenium(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    backup_button_xpath = '//*[contains(text(), "Back Up Now")]'
    driver.get(site)
    time.sleep(5)   # wait for site to load, for some reason next line doesn't fully work
    backup_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, backup_button_xpath)))
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(backup_button)).click()
    time.sleep(1)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(backup_button))  # download started
    time.sleep(5)   # download finished

def backup_network_settings_current_UI_selenium(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    backups_button_xpath = "//*[contains(text(), 'Backups')]"
    download_button_xpath = '//*[contains(text(), "Download")]'
    download2_button_name = 'backupDownload'

    driver.get(site)
    backups_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, backups_button_xpath)))
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(backups_button)).click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, download_button_xpath))).click()
    downloadDiv = driver.find_element(By.CLASS_NAME, "ReactModalPortal")    # don't really know why this is needed...
    download2_button = WebDriverWait(downloadDiv, 60).until(EC.presence_of_element_located((By.NAME, download2_button_name)))
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(download2_button)).click()
    time.sleep(10)

def backup_network_settings_new_UI_selenium(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    backup_download_name = 'backupDownload'
    driver.get(site)
    backup_download_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, backup_download_name)))
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(backup_download_button)).click()
    time.sleep(10)
