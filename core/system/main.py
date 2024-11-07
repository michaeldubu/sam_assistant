# core/system/main.py
from dataclasses import dataclass
import asyncio
import json
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class SystemConfig:
    name: str = "SAM Assistant"
    version: str = "1.0.0"
    mode: str = "production"
    features_enabled: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.features_enabled is None:
            self.features_enabled = {
                "3d_interface": True,
                "voice_control": True,
                "remote_access": True,
                "family_profiles": True,
                "business_analytics": True
            }

class CoreSystem:
    def __init__(self):
        self.config = self.load_config()
        self.base_path = Path(__file__).parent.parent
        self.systems = {
            "interface": None,
            "voice": None,
            "monitoring": None,
            "remote": None
        }
        
    def load_config(self) -> SystemConfig:
        """Load system configuration"""
        try:
            with open('config/local/settings.json') as f:
                config_data = json.load(f)
            return SystemConfig(**config_data)
        except Exception as e:
            print(f"Error loading config: {e}")
            return SystemConfig()
            
    async def start(self):
        """Start all systems"""
        startup_tasks = [
            self.start_interface(),
            self.start_voice_control(),
            self.start_monitoring(),
            self.start_remote_access()
        ]
        await asyncio.gather(*startup_tasks)
        
    async def start_interface(self):
        """Initialize and start interface"""
        from .interface import Interface
        self.systems["interface"] = Interface()
        await self.systems["interface"].start()
        
    async def start_voice_control(self):
        """Initialize voice control"""
        from .voice import VoiceControl
        self.systems["voice"] = VoiceControl()
        await self.systems["voice"].start()
        
    async def start_monitoring(self):
        """Initialize monitoring"""
        from .monitoring import MonitoringSystem
        self.systems["monitoring"] = MonitoringSystem()
        await self.systems["monitoring"].start()
        
    async def start_remote_access(self):
        """Initialize remote access"""
        from .remote import RemoteAccess
        self.systems["remote"] = RemoteAccess()
        await self.systems["remote"].start()
