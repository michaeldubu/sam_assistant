# remote/access_manager.py
from fastapi import FastAPI, WebSocket
from typing import Dict, Set
import jwt
import asyncio
import json

class RemoteAccessManager:
    def __init__(self):
        self.app = FastAPI()
        self.active_connections: Dict[str, WebSocket] = {}
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await self.connect(websocket, client_id)
            
        @self.app.get("/status")
        async def get_status():
            return {"status": "online", "clients": len(self.active_connections)}
            
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        try:
            while True:
                data = await websocket.receive_text()
                await self.process_message(client_id, data)
        except Exception:
            self.disconnect(client_id)
            
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
