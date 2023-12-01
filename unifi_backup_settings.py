from dataclasses import dataclass


@dataclass
class UnifiBackupSettings:
    """Class for tracking settings for unifi backups"""
    location: str
    ip: str
    backup_network: bool = True
    backup_OS: bool = True
