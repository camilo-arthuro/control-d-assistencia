from fastapi import FastAPI
import threading
from mqtt_service import start_mqtt

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()
