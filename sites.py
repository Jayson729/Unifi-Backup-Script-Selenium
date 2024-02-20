from unifi_backup_settings import UnifiBackupSettings
from device_information import get_device_information


class Sites:
    def __init__(self, downloads_path, current_datetime):
        self.backup_settings = _get_unifi_backup_settings(
            downloads_path, current_datetime)


def _get_unifi_backup_settings(downloads_path, current_datetime) -> set[UnifiBackupSettings]:
    backup_settings = []
    for company, information in get_device_information().items():
        backup_settings.append(UnifiBackupSettings(
            company, **information, downloads_path=downloads_path, current_datetime=current_datetime))
    return backup_settings
