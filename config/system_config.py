# config/system_config.py
import yaml
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.load_all_configs()
        
    def load_all_configs(self):
        """Load all configuration files"""
        self.system_config = self.load_config("system")
        self.network_config = self.load_config("network")
        self.security_config = self.load_config("security")
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        config_file = self.config_dir / f"{config_name}.yaml"
        if not config_file.exists():
            return self.create_default_config(config_name)
        with open(config_file) as f:
            return yaml.safe_load(f)
            
    def create_default_config(self, config_name: str) -> Dict[str, Any]:
        """Create default configuration"""
        defaults = {
            "system": {
                "name": "SAM Assistant",
                "version": "1.0.0",
                "mode": "production",
                "features": {
                    "3d_interface": True,
                    "voice_control": True,
                    "remote_access": True,
                    "monitoring": True
                }
            },
            "network": {
                "host": "0.0.0.0",
                "port": 8000,
                "monitoring_port": 8050,
                "remote_port": 8080,
                "ssl_enabled": True
            },
            "security": {
                "token_expiry": 86400,
                "encryption_enabled": True,
                "backup_enabled": True,
                "allowed_ips": ["127.0.0.1"]
            }
        }
        
        config = defaults.get(config_name, {})
        config_file = self.config_dir / f"{config_name}.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
        return config
