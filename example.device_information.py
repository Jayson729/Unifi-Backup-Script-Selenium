from unifi_backup_settings import UISettings
from selenium_scripts import backup_network_settings_current_UI_selenium, backup_OS_settings_current_UI_selenium


def get_company_information():
    unifi_company_information: dict[str, dict[str, ]] = {
        # example device backing up both OS and network using the default selenium script (current UI)
        # the ip is the value in the URL when accessing network/os settings
        'DEVICE 1':     {'ip': '000000000000000000000000000000000000000000000000000000000000:000000000', },

        # example device backing up only OS settings using the default selenium script (current UI)
        'DEVICE 2':     {'ip': '000000000000000000000000000000000000000000000000000000000000:000000000', 'ui_settings': UISettings.BACKUP_ONLY_OS},

        # example device backing up only network settings using the default selenium script (current UI)
        'DEVICE 3':     {'ip': '000000000000000000000000000000000000000000000000000000000000:000000000', 'ui_settings': UISettings.BACKUP_ONLY_NETWORK},

        # example device backing up both OS and network using custom selenium scripts (must have a site and driver keyword argument)
        'DEVICE 4':     {'ip': '000000000000000000000000000000000000000000000000000000000000:000000000',
                         'selenium_script_network': backup_network_settings_current_UI_selenium,
                         'selenium_script_os': backup_OS_settings_current_UI_selenium},
    }
    return unifi_company_information
