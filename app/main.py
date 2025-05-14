from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
import asyncio
from datetime import datetime
import random

from app.connection_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

@app.get('/')
def start():
    return {"Message": "Test API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    data = {
        "type": "sensor_data",
        "data": [{
            "timestamp": datetime.now(),
            "airTemperature": 65.3,
            "airHumidity": 20.3,
            "soilHumidity": 15.3,
            "soilTemperature": 45.3,
            "sensorWorking": 5
        }],
        "status": 0
    }

    try:
        while True:
            data['data'][0]['timestamp'] = datetime.now()
            data['data'][0]['airTemperature'] = max(10, random.randint(-10, 10) + random.randint(-10, 10))
            data['data'][0]['airHumidity'] = max(14, random.randint(-10, 10) + random.randint(-7, 7))
            data['data'][0]['soilHumidity'] = max(7, random.randint(-10, 10) + random.randint(-6, 6))
            data['data'][0]['soilTemperature'] = max(8, random.randint(-10, 10) + random.randint(-2, 3))

            await manager.broadcast(jsonable_encoder(data))

            await asyncio.sleep(20) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Unexpected error: {e}")
        manager.disconnect(websocket)
