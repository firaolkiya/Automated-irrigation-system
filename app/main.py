from fastapi import FastAPI, WebSocket
import asyncio

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
        "data":[
            {
        "airTemperature": 65.3,
        "airHumidity": 20.3,
        "soilHumidity": 15.3,
        "soilTemperature": 45.3,
        "sensorWorking": "all"
        }
            ],
        "status":0
    }
    

    while True:
        
        for client in clients:
            await websocket.send_json(data)
        await asyncio.sleep(delay=60)  
