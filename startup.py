# startup.py
import asyncio
from pathlib import Path
import logging
import os
from typing import Dict, Optional

class SystemStartup:
    def __init__(self):
        # Create necessary directories first
        self.create_directories()
        self.logger = self.setup_logging()
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
    def create_directories(self):
        """Create all necessary directories"""
        directories = [
            'logs',
            'config',
            'data',
            'models',
            'cache',
            'backup',
            'temp'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def setup_logging(self):
        """Setup system logging"""
        log_file = Path('logs/system.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('SAM')
        
    async def start(self):
        """Start all systems"""
        try:
            # Start core systems
            self.logger.info("Starting core systems...")
            core_system = CoreSystem()
            await core_system.start()
            
            # Start monitoring
            self.logger.info("Starting monitoring...")
            monitor = SystemMonitor()
            asyncio.create_task(monitor.start_monitoring())
            
            # Start backup system
            self.logger.info("Starting backup system...")
            backup = EmergencyBackup()
            asyncio.create_task(backup.start_auto_backup())
            
            # Start remote access
            self.logger.info("Starting remote access...")
            remote = RemoteAccessManager()
            await remote.start()
            
            self.logger.info("System startup complete!")
            
        except Exception as e:
            self.logger.error(f"Startup failed: {e}")
            raise

if __name__ == "__main__":
    startup = SystemStartup()
    asyncio.run(startup.start())
