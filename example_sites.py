from unifi_backup_settings import UnifiBackupSettings, UISettings, CurrentUISettings, NewUISettings

def get_unifi_backup_settings() -> set[UnifiBackupSettings]:
    backup_settings = [
        # basic settings, current UI, backs up both network and OS settings
        UnifiBackupSettings('Example', '000000000000000000000000000000000000000000000000000000000000:000000000'),

        # current UI, no OS backups
        UnifiBackupSettings('Example', '000000000000000000000000000000000000000000000000000000000000:000000000', UISettings(CurrentUISettings(backup_OS=False))),

        # current UI, no network backups
        UnifiBackupSettings('Example', '000000000000000000000000000000000000000000000000000000000000:000000000', UISettings(CurrentUISettings(backup_network=False))),

        # new UI, potentially change version
        UnifiBackupSettings('Example', '000000000000000000000000000000000000000000000000000000000000', UISettings(new_ui_settings=NewUISettings('7.2.97.0'))),
    ]
    return backup_settings