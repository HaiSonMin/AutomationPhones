"""
Bridge Configuration - Centralized configuration for all bridges
"""

from pathlib import Path
import json
from typing import Dict, Any, Optional


class BridgeConfig:
    """Centralized configuration for all bridges"""

    # API Configuration
    SERVER_URL = "http://localhost:9000/api/v1"
    API_TIMEOUT = 30
    API_RETRY_COUNT = 3

    # Cache Configuration
    CACHE_TTL = 300  # 5 minutes
    CACHE_SIZE = 1000

    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # UI Configuration
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    UI_URL = "http://localhost:3000"

    # Security
    TOKEN_SERVICE_NAME = "AutomationToolPhones"
    TOKEN_KEY = "auth_token"
    USER_KEY = "auth_user"

    # Performance
    MAX_CONCURRENT_REQUESTS = 10
    CONNECTION_POOL_SIZE = 100

    # Features (enable/disable bridges)
    ENABLED_BRIDGES = {
        "auth": True,
    }

    @classmethod
    def load_from_file(cls, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load configuration from JSON file

        Args:
            config_path: Path to config file (optional)

        Returns:
            Configuration dictionary
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"

        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)

        # Return default config
        return {
            "server_url": cls.SERVER_URL,
            "timeout": cls.API_TIMEOUT,
            "retry_count": cls.API_RETRY_COUNT,
            "ui": {
                "width": cls.WINDOW_WIDTH,
                "height": cls.WINDOW_HEIGHT,
                "url": cls.UI_URL,
            },
            "enabled_bridges": cls.ENABLED_BRIDGES,
        }

    @classmethod
    def save_to_file(cls, config: Dict[str, Any], config_path: Optional[Path] = None):
        """
        Save configuration to JSON file

        Args:
            config: Configuration dictionary
            config_path: Path to save config (optional)
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)


# Default configuration instance
config = BridgeConfig.load_from_file()
