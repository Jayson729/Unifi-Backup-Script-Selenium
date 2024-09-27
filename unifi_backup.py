import os
import datetime
import shutil
from pathlib import Path
from selenium import webdriver
from unifi_backup_settings import UnifiBackupSettings, UISettings
from sites import Sites


class Browsers:
    NUM_BROWSERS = 3
    MICROSOFT_EDGE = 1
    MOZILLA_FIREFOX = 2
    GOOGLE_CHROME = 3


def move_file_by_extension(downloads_folder: str, path_to_move: str, extension: str) -> None:
    for filename in os.listdir(downloads_folder):
        if filename.endswith(extension):
            if path_to_move is None:
                path_to_move = os.path.join(
                    downloads_folder, 'old-unf-and-unifi-files', filename)
            absolute_file_location = os.path.join(downloads_folder, filename)
            os.makedirs(os.path.dirname(path_to_move), exist_ok=True)
            shutil.move(absolute_file_location, path_to_move)


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


def get_webdriver_from_userinput(userinput: int) -> webdriver.Edge | webdriver.Chrome | webdriver.Firefox:
    if userinput == Browsers.MICROSOFT_EDGE:
        options = webdriver.EdgeOptions()
        options.add_argument('inprivate')
        driver = webdriver.Edge(options=options)
    elif userinput == Browsers.MOZILLA_FIREFOX:
        options = webdriver.FirefoxOptions()
        options.add_argument('--incognito')
        driver = webdriver.Firefox(options=options)
    elif userinput == Browsers.GOOGLE_CHROME:
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        driver = webdriver.Chrome(options=options)
    return driver


def backup_unifi(backup_setting: UnifiBackupSettings, driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox, files_not_backed_up: list[str]) -> None:
    os_path = os.path.join(
        backup_setting.downloads_path, "unifi_backups", backup_setting.location, backup_setting.os_filename
    )
    network_path = os.path.join(
        backup_setting.downloads_path, "unifi_backups", backup_setting.location, backup_setting.network_filename
    )

    if backup_setting.ui_settings == UISettings.BACKUP_NETWORK_AND_OS:
        try:
            backup_setting.selenium_script_network(
                site=backup_setting.network_site, driver=driver)
            move_file_by_extension(
                backup_setting.downloads_path, network_path, ".unf")

            backup_setting.selenium_script_os(
                site=backup_setting.os_site, driver=driver)
            move_file_by_extension(
                backup_setting.downloads_path, os_path, ".unifi")
        except Exception as e:
            if e == KeyboardInterrupt:
                KeyboardInterrupt()
            print(
                f'Could not backup {backup_setting.location} NETWORK or OS settings')
            files_not_backed_up.append(
                f'{backup_setting.location} NETWORK or OS')

    elif backup_setting.ui_settings == UISettings.BACKUP_ONLY_NETWORK:
        try:
            backup_setting.selenium_script_network(
                site=backup_setting.network_site, driver=driver)
            move_file_by_extension(
                backup_setting.downloads_path, network_path, ".unf")
        except Exception as e:
            if e == KeyboardInterrupt:
                KeyboardInterrupt()
            print(
                f'Could not backup {backup_setting.location} NETWORK settings')
            files_not_backed_up.append(f'{backup_setting.location} NETWORK')

    elif backup_setting.ui_settings == UISettings.BACKUP_ONLY_OS:
        try:
            backup_setting.selenium_script_os(
                site=backup_setting.os_site, driver=driver)
            move_file_by_extension(
                backup_setting.downloads_path, os_path, ".unifi")
        except Exception as e:
            if e == KeyboardInterrupt:
                KeyboardInterrupt()
            print(f'Could not backup {backup_setting.location} OS settings')
            files_not_backed_up.append(f'{backup_setting.location} OS')


def login_unifi_user(driver: webdriver.Edge | webdriver.Chrome | webdriver.Firefox) -> None:
    driver.get('https://unifi.ui.com/consoles')
    input('Press enter in this console when you are logged in')


def main() -> None:
    driver = get_webdriver()
    downloads_path = os.path.join(Path.home(), "Downloads")
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    sites = Sites(downloads_path, current_datetime)

    login_unifi_user(driver)

    move_file_by_extension(downloads_path, None, '.unf')
    move_file_by_extension(downloads_path, None, '.unifi')

    files_not_backed_up = []
    for backup_setting in sites.backup_settings:
        backup_unifi(backup_setting, driver, files_not_backed_up)

    if files_not_backed_up != []:
        print('Error backing up the following files:')
        print(files_not_backed_up)
    else:
        print('All files backed up successfully')
    driver.quit()


if __name__ == "__main__":
    main()
