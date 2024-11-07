# emergency/backup_system.py
import shutil
import os
from datetime import datetime
import zipfile
import asyncio

class EmergencyBackup:
    def __init__(self):
        self.backup_dir = "backups"
        self.critical_dirs = [
            "config",
            "data",
            "models",
            "user_profiles"
        ]
        os.makedirs(self.backup_dir, exist_ok=True)
        
    async def create_backup(self):
        """Create system backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        
        # Create zip file
        with zipfile.ZipFile(
            f"{self.backup_dir}/{backup_name}.zip", 
            'w', 
            zipfile.ZIP_DEFLATED
        ) as zipf:
            for dir_name in self.critical_dirs:
                if os.path.exists(dir_name):
                    for root, dirs, files in os.walk(dir_name):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            
    async def start_auto_backup(self):
        """Start automatic backup system"""
        while True:
            await self.create_backup()
            await asyncio.sleep(3600)  # Hourly backup
