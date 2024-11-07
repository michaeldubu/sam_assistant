# startup.py
import asyncio
from pathlib import Path
import logging
from typing import Dict, Optional

class SystemStartup:
    def __init__(self):
        self.logger = self.setup_logging()
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
    def setup_logging(self):
        """Setup system logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/system.log'),
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
