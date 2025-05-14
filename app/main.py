from fastapi import FastAPI,WebSocket

app=FastAPI()

@app.websocket('/ws')
def start_listen(socket:WebSocket):
    socket.accept()
    data = {
        "message":"Succesfully connected"
    }
    socket.send_json(data)
