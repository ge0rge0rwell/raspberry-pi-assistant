import psutil
import platform
import os
import time
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI()

# Enable CORS for the React GUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SystemMonitor:
    @staticmethod
    def get_stats():
        return {
            "cpu_usage": psutil.cpu_percent(interval=None),
            "memory_usage": psutil.virtual_memory().percent,
            "temperature": SystemMonitor._get_temp(),
            "uptime": SystemMonitor._get_uptime(),
            "platform": platform.system(),
            "processor": platform.processor(),
        }

    @staticmethod
    def _get_temp():
        try:
            # RPi specific temperature read
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read()) / 1000.0
                return round(temp, 1)
        except:
            return 0.0

    @staticmethod
    def _get_uptime():
        return round(time.time() - psutil.boot_time(), 0)

@app.get("/stats")
async def stats():
    return SystemMonitor.get_stats()

# WebSocket for real-time events (STT, TTS, State)
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

async def broadcast_event(event_type: str, data: dict):
    message = json.dumps({"type": event_type, "data": data})
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            pass
