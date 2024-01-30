from unifi_backup_settings import UnifiBackupSettings

def get_unifi_backup_settings() -> set[UnifiBackupSettings]:
    backup_settings = [
        UnifiBackupSettings('Example', '000000000000000000000000000000000000000000000000000000000000:000000000'),
        # insert UnifiBackupSettings here
    ]
    return backup_settings