import os
import time
import datetime
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sites import get_unifi_backup_settings


class Browsers:
    NUM_BROWSERS = 3
    MICROSOFT_EDGE = 1
    MOZILLA_FIREFOX = 2
    GOOGLE_CHROME = 3


def move_file_by_extension(downloads_folder: str, path_to_move: str, extension: str):
    for filename in os.listdir(downloads_folder):
        if filename.endswith(extension):
            if path_to_move is None:
                path_to_move = os.path.join(
                    downloads_folder, 'old-unf-and-unifi-files', filename)
            absolute_file_location = os.path.join(downloads_folder, filename)
            os.makedirs(os.path.dirname(path_to_move), exist_ok=True)
            shutil.move(absolute_file_location, path_to_move)


def backup_network_settings(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
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
    except:
        return 1


def backup_OS_settings(site: str, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
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
    except:
        return 1


def get_webdriver_from_userinput(userinput: int) -> webdriver.Edge | webdriver.Chrome | webdriver.Firefox:
    if userinput == Browsers.MICROSOFT_EDGE:
        options = webdriver.EdgeOptions()
        options.add_argument('--incognito')
        driver = webdriver.Edge(options=options)
    elif userinput == Browsers.MOZILLA_FIREFOX:
        options = webdriver.FirefoxOptions()
        options.add_argument('--incognito')
        driver = webdriver.Firefox(options=options)
    elif userinput == Browsers.GOOGLE_CHROME:
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(15)
    return driver


def get_webdriver() -> webdriver.Edge | webdriver.Chrome | webdriver.Firefox:
    driver = None
    while (1):
        print('|------------------------------------------------------------------------|')
        print('|  ENTER Q TO QUIT                                                       |')
        print('|  Select a broswer you will not use during this backup                  |')
        print('|  Any open tabs in the selected browser will be closed                  |')
        print('|  Any existing .unf and .unifi files will be moved to a new folder      |')
        print('|  Keep the browser window on screen at all times once the backup begins |')
        print('|                                                                        |')
        print('|  Please select the browser you would like to use                       |')
        print('|    (1): Microsoft Edge                                                 |')
        print('|    (2): Mozilla Firefox                                                |')
        print('|    (3): Google Chrome                                                  |')
        print('|------------------------------------------------------------------------|')
        userinput = input()
        if userinput.upper() == 'Q':
            print("Exiting Program")
            quit(0)
        if not userinput.isdigit():
            print('invalid browser number')
            continue

        userinput = int(userinput)
        if userinput > Browsers.NUM_BROWSERS or userinput < 0:
            print('invalid broswer number')
            continue
        driver = get_webdriver_from_userinput(userinput)
        return driver


def login_unifi_user(driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox):
    driver.get('https://unifi.ui.com/consoles')
    input('Press enter in this console when you are logged in')


def main():
    driver = get_webdriver()
    downloads_path = os.path.join(Path.home(), "Downloads")
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    backup_settings = get_unifi_backup_settings()

    login_unifi_user(driver)

    move_file_by_extension(downloads_path, None, '.unf')
    move_file_by_extension(downloads_path, None, '.unifi')

    files_not_backed_up = []
    for backup_setting in backup_settings:
        network_site = None
        OS_site = None
        if backup_setting.backup_network:
            network_site = f'https://unifi.ui.com/consoles/{backup_setting.ip}/network/default/settings/system'
        if backup_setting.backup_OS:
            OS_site = f'https://unifi.ui.com/consoles/{backup_setting.ip}/console-settings'

        if network_site is not None:
            new_filename = f"{backup_setting.location}_unifi_network_backup_{current_datetime}.unf"
            path_to_download = os.path.join(
                downloads_path, "unifi_backups", backup_setting.location, new_filename
            )
            if backup_network_settings(network_site, driver):
                print(
                    f'Could not backup {backup_setting.location} network settings')
                files_not_backed_up.append(
                    f'{backup_setting.location} Network')
            else:
                move_file_by_extension(
                    downloads_path, path_to_download, ".unf")

        if OS_site is not None:
            new_filename = f"{backup_setting.location}_unifi_os_backup_{current_datetime}.unifi"
            path_to_download = os.path.join(
                downloads_path, "unifi_backups", backup_setting.location, new_filename
            )
            if backup_OS_settings(OS_site, driver):
                print(
                    f'Could not backup {backup_setting.location} OS settings')
                files_not_backed_up.append(f'{backup_setting.location} OS')
            else:
                move_file_by_extension(
                    downloads_path, path_to_download, ".unifi")

    if files_not_backed_up != []:
        print('Error backing up the following files:')
        print(files_not_backed_up)
    else:
        print('All files backed up successfully')
    driver.quit()


if __name__ == "__main__":
    main()
