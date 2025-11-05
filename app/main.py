from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from .mqtt.mqtt_service import start_mqtt
from dotenv import load_dotenv
from .model.UserTic import Persona
from .model.clase import Asignatura
import threading
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()

@app.post("/api/asistencia/persona", response_model=dict, tags=["CREAR USUARIO"])
async def crear_usuario(usuario_nuevo: Persona, db: Session = Depends(get_db)):
    datos_usuario = Persona.model_validate(usuario_nuevo)
    db.add(datos_usuario)
    db.commit()
    return {"msg":"Usuario creado y añadido a la DDBB"}
