import os
import logging
from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation
from typing import Optional, Any

class ConfigManager:
    """Manages configuration for the README manager using ConfigParser."""
    
    DEFAULT_CONFIG_PATHS = [
        'default_config.ini',  # Project-level default config
        '~/.readme_manager/config.ini',  # User-level config
        '.readme_manager.ini'  # Directory-level config
    ]

    def __init__(self, custom_config_path: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            custom_config_path: Optional path to a custom config file
        """
        self.logger = logging.getLogger(__name__)
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self._load_config(custom_config_path)

    def _load_config(self, custom_config_path: Optional[str]) -> None:
        """Load configuration from various sources in order of precedence."""
        # Load configs in order of precedence
        config_paths = self.DEFAULT_CONFIG_PATHS.copy()
        if custom_config_path:
            config_paths.append(custom_config_path)

        # Load each config file, overlaying on top of previous ones
        for config_path in config_paths:
            path = Path(os.path.expanduser(config_path))
            if path.exists():
                try:
                    self.config.read(path)
                    self.logger.info(f"Loaded config from {path}")
                except Exception as e:
                    self.logger.warning(f"Error loading config from {path}: {str(e)}")

        # If no config files were found, load defaults
        if not self.config.sections():
            self._load_default_config()

    def _load_default_config(self) -> None:
        """Load default configuration values."""
        self.config.add_section('file_settings')
        self.config.set('file_settings', 'default_file', 'README.md')
        self.config.set('file_settings', 'backup_enabled', 'yes')
        self.config.set('file_settings', 'backup_directory', '.backups')
        self.config.set('file_settings', 'backup_count', '5')

        self.config.add_section('logging')
        self.config.set('logging', 'level', 'INFO')
        self.config.set('logging', 'format', 
                       '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.config.set('logging', 'file', 'readme_manager.log')

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            section: Configuration section
            option: Option name within section
            fallback: Default value if option doesn't exist
            
        Returns:
            Configuration value or fallback
        """
        return self.config.get(section, option, fallback=fallback)

    def getboolean(self, section: str, option: str, fallback: bool = None) -> bool:
        """Get a boolean configuration value.
        
        Args:
            section: Configuration section
            option: Option name within section
            fallback: Default value if option doesn't exist
        """
        return self.config.getboolean(section, option, fallback=fallback)

    def getint(self, section: str, option: str, fallback: int = None) -> int:
        """Get an integer configuration value."""
        return self.config.getint(section, option, fallback=fallback)

    def getfloat(self, section: str, option: str, fallback: float = None) -> float:
        """Get a float configuration value."""
        return self.config.getfloat(section, option, fallback=fallback)

    def set(self, section: str, option: str, value: str) -> None:
        """Set a configuration value.
        
        Args:
            section: Configuration section
            option: Option name within section
            value: Value to set
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def save_config(self, path: Optional[str] = None) -> None:
        """Save current configuration to a file.
        
        Args:
            path: Path to save the configuration file (optional)
        """
        if not path:
            path = '.readme_manager.ini'
        
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('w') as f:
                self.config.write(f)
            self.logger.info(f"Saved configuration to {path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
            raise