# devices/google_integration.py
import pychromecast
from pychromecast.controllers import BaseController
import asyncio
from typing import Dict

class GoogleDeviceManager:
    def __init__(self):
        self.devices = {}
        self.chromecasts = {}
        
    async def discover_devices(self):
        """Find all Google devices"""
        chromecasts, browser = pychromecast.get_chromecasts()
        for cc in chromecasts:
            cc.wait()  # Wait for device to be ready
            device_name = cc.device.friendly_name
            self.chromecasts[device_name] = cc
            self.devices[device_name] = {
                "type": cc.device.model_name,
                "ip": cc.host,
                "port": cc.port,
                "uuid": str(cc.uuid)
            }
            
    async def send_command(self, device_name: str, command: str, **kwargs):
        """Send command to Google device"""
        if device_name in self.chromecasts:
            cc = self.chromecasts[device_name]
            if command == "play":
                cc.media_controller.play()
            elif command == "pause":
                cc.media_controller.pause()
            elif command == "volume":
                cc.set_volume(kwargs.get('level', 0.5))
            elif command == "speak":
                # For Google Home speakers
                text = kwargs.get('text', '')
                lang = kwargs.get('language', 'en')
                self.cast_text_to_speech(cc, text, lang)

    def cast_text_to_speech(self, cc, text: str, language: str = 'en'):
        """Cast text to speech on Google Home"""
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={language}&client=tw-ob"
        cc.media_controller.play_media(tts_url, 'audio/mp3')
