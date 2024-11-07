# emergency/recovery.py
import zipfile
import os
from typing import Optional

class SystemRecovery:
    def __init__(self):
        self.backup_dir = "backups"
        self.recovery_dir = "recovery"
        
    def list_backups(self):
        """List available backups"""
        return [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
        
    def restore_from_backup(self, backup_name: str):
        """Restore system from backup"""
        backup_path = os.path.join(self.backup_dir, backup_name)
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup {backup_name} not found")
            
        # Clear recovery directory
        if os.path.exists(self.recovery_dir):
            shutil.rmtree(self.recovery_dir)
        os.makedirs(self.recovery_dir)
        
        # Extract backup
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(self.recovery_dir)
            
        # Verify recovery
        self.verify_recovery()
        
    def verify_recovery(self):
        """Verify recovered files"""
        required_dirs = ["config", "data", "models"]
        for dir_name in required_dirs:
            recovery_path = os.path.join(self.recovery_dir, dir_name)
            if not os.path.exists(recovery_path):
                raise Exception(f"Recovery verification failed: {dir_name} missing")
