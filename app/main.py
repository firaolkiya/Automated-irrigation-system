from fastapi import FastAPI, WebSocket
import asyncio
from datetime import datetime
import random
app = FastAPI()

@app.get('/')
def start():
    return {
        "Message": "Test api"
    }

clients:list[WebSocket] = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    clients.append(websocket)

    data = {
        "type":"sensor_data",
        "data":[{
        "timestamp":datetime.now(),
        "airTemperature": 65.3,
        "airHumidity": 20.3,
        "soilHumidity": 15.3,
        "soilTemperature": 45.3,
        "sensorWorking": 5
        }],
        "status":0
    }
    

    while True:
        data['data'][0]['airTemperature'] = min(15, random.randint(-10,10)+random.randint(-10,10))
        data['data'][0]['airHumidity']=min(45, random.randint(-10,10)+random.randint(-7,7))
        data['data'][0]['soilHumidity']=min(17, random.randint(-10,10)+random.randint(-6,6))
        data['data'][0]['soilTemperature']=min(20, random.randint(-10,10)+random.randint(-2,3))
        for client in clients:
            await websocket.send_json(data)
        await asyncio.sleep(delay=60)  
