import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def backup_OS_settings_current_UI_selenium(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    try:
        driver.get(site)
        time.sleep(5)
        backup_settings = driver.find_element(By.ID, "backupSettings")
        backup_button = backup_settings.find_element(
            By.XPATH, "//*[contains(text(), 'Back Up Now')]"
        )
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(backup_button)).click()
        time.sleep(1)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(backup_button))
        time.sleep(5)
        return 0
    # if it fails for any reason except for KeyboardInterrupt, then just continue and return failure
    # reasoning behind this is that we don't want to restart entire program if backup fails, simply
    # log the failure and continue. We do want to exit if user says to though.
    except Exception as e:
        if e == KeyboardInterrupt:
            KeyboardInterrupt()
        else:
            return 1


def backup_network_settings_current_UI_selenium(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    try:
        driver.get(site)
        backups_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Backups')]")))
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(backups_button)).click()
        download_button = driver.find_element(By.NAME, "backupDownload")
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(download_button)).click()
        downloadDiv = driver.find_element(By.CLASS_NAME, "ReactModalPortal")
        download_button2 = downloadDiv.find_element(By.NAME, "backupDownload")
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(download_button2)).click()
        time.sleep(10)
        return 0
    # if it fails for any reason except for KeyboardInterrupt, then just continue and return failure
    # reasoning behind this is that we don't want to restart entire program if backup fails, simply
    # log the failure and continue. We do want to exit if user says to though.
    except Exception as e:
        if e == KeyboardInterrupt:
            KeyboardInterrupt()
        else:
            return 1
