import os
import sys
import subprocess
import json

def setup():
    """Setup SAM Assistant"""
    # Create virtual environment
    subprocess.run(["python", "-m", "venv", "venv"])
    
    # Activate virtual environment
    if sys.platform == "win32":
        subprocess.run(["venv\\Scripts\\activate"])
    else:
        subprocess.run(["source", "venv/bin/activate"])
    
    # Install requirements
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    
    print("Setup complete")

if __name__ == "__main__":
    setup()
