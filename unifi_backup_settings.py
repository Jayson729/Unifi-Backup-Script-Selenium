from dataclasses import dataclass
from enum import Enum
from selenium_scripts import backup_OS_settings_current_UI_selenium, backup_network_settings_current_UI_selenium
from typing import Callable


class UISettings(Enum):
    BACKUP_ONLY_NETWORK = 1
    BACKUP_ONLY_OS = 2
    BACKUP_NETWORK_AND_OS = 3


@dataclass
class UnifiBackupSettings:
    """Class for tracking settings for unifi backups"""
    location: str
    ip: str
    downloads_path: str
    current_datetime: str
    ui_settings: UISettings = UISettings.BACKUP_NETWORK_AND_OS
    network_link_format: str = 'https://unifi.ui.com/consoles/{ip}/network/default/settings/system'
    os_link_format: str = 'https://unifi.ui.com/consoles/{ip}/console-settings'
    selenium_script_network: Callable = backup_network_settings_current_UI_selenium
    selenium_script_os: Callable = backup_OS_settings_current_UI_selenium

    def __post_init__(self):
        self.network_filename: str = f'{self.location}_unifi_network_backup_{self.current_datetime}.unf'
        self.os_filename: str = f'{self.location}_unifi_os_backup_{self.current_datetime}.unifi'
        self.network_site = self.network_link_format.format(ip=self.ip)
        self.os_site = self.os_link_format.format(ip=self.ip)
