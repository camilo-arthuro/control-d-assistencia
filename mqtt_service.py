import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from .model.UserTic import AlumneTic, ClasseTic

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

#DDBB
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def on_connect(client, userdata, flags, rc):
    print("Connected to HiveMQ broker with code:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg,assistencia_confirmada: ClasseTic, find_user: AlumneTic, db: Session = Depends(get_db)):
    print(f"Message received in {msg.topic}: {msg.payload.decode()}")
    # save the data in the database
    user_id = int(msg.payload.decode())
    query = select(find_user).where(find_user.id == user_id)
    ddbb_user = db.exec(query).first()
    assistencia_confirmada.id_alumne = ddbb_user.id
    assistencia_confirmada.alumne_name = ddbb_user.name
    assistencia_confirmada.assistencia = True
    db.add(assistencia_confirmada)
    db.commit()
def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_forever()