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

        # example device backing up both OS and network using custom selenium scripts and custom link formats
        # (must have a site and driver keyword argument) this would be used in the case of a UI update with a
        # different URL. You do not necessarily have to change all of these, however more than likely if you
        # have to change one you will have to change the rest. If the URL has something such as a version, you
        # could add an extra field to unifi_backup_settings.py, add it to the format in __post_init__(), and
        # add that in curly braces in the inputted format. I've provided how to do this in comments in these files.
        'DEVICE 4':     {'ip': '000000000000000000000000000000000000000000000000000000000000:000000000',
                         'version': '0.0.0',
                         'network_link_format': 'https://unifi.ui.com/{version}/consoles/{ip}/network/default/settings/system',
                         'os_link_format': 'https://unifi.ui.com/{version}/consoles/{ip}/console-settings',
                         # these would likely be a custom script you made, this is here as an example
                         'selenium_script_network': backup_network_settings_current_UI_selenium,
                         'selenium_script_os': backup_OS_settings_current_UI_selenium},
    }

    return unifi_company_information
