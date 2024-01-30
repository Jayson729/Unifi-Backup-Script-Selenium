from dataclasses import dataclass, field

@dataclass
class CurrentUISettings:
    backup_network: bool = True
    backup_OS: bool = True

@dataclass
class NewUISettings:
    version_in_url: str = None

@dataclass(init=False)
class UISettings:
    current_ui_settings: CurrentUISettings
    new_ui_settings: NewUISettings

    def __init__(self, current_ui_settings: CurrentUISettings = None, new_ui_settings: NewUISettings = None):
        self.current_ui_settings = current_ui_settings
        self.new_ui_settings = new_ui_settings

        # default to current ui backuping both if no settings are entered
        if current_ui_settings is None and new_ui_settings is None:
            self.current_ui_settings = CurrentUISettings(True, True)

@dataclass
class UnifiBackupSettings:
    """Class for tracking settings for unifi backups"""
    location: str
    ip: str
    # have to use field to make non-mutable class
    ui_settings: UISettings = field(default_factory=UISettings) 
