from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime, date, time
from app.model.UserTic import Alumno, Persona
from app.model.clase import Asignatura, Trabaja, Asiste
import paho.mqtt.client as mqtt
import os

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
    print("Conectado a HiveMQ broker con codigo:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

    id_usuario = int(msg.payload.decode())
    info_fecha = datetime.now()
    fecha_actual = info_fecha.date()
    hh = info_fecha.hour
    mm = info_fecha.minute
    hora_actual=time(hh,mm)

    with (Session(engine) as db):
        query = select(Persona).where(Persona.id_persona == id_usuario)
        ddbb_persona = db.exec(query).first()
        rol = ddbb_persona.rol
        if not ddbb_persona:
            return print(f"Tarjeta sin asignar: {id_usuario}")
        elif rol == "alumno":
            registro_alumno=Asiste(
                id_alumno = id_usuario,
                id_asignatura= 1,
                fecha= fecha_actual,
                hora= hora_actual,
                asistio= True
            )
            db.add(registro_alumno)
            db.commit()
            return print(f"Asistencia registrada {id_usuario}")
        else:
            registro_personal=Trabaja(
                id_personal=id_usuario,
                fecha=fecha_actual,
                hora=hora_actual
            )
            db.add(registro_personal)
            db.commit()
            return print(f"Asistencia registrada {id_usuario}")

def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_forever()

def asistencia_trabaja(id_persona, fecha, hora): #PENDING!!!!!!!!!!!
    registro=Trabaja(
        id_persona=id_persona,
        fecha=fecha,
        hora=hora,
        zona="itic bcn",
        asistio=True
    )
    return registro
