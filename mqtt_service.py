from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime
from .model.UserTic import Alumno, Persona, PersonalServicio, Profesor
from .model.clase import Clase, Fecha, Asignatura, DarAsignatura, Trabaja
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
    hh = info_fecha.hour
    dd = info_fecha.day
    mm = info_fecha.month
    aa = info_fecha.year
    jornada = "mañana" if hh < 14 else "tarde"

    with Session(engine) as db:
        query = select(Alumno).where(Alumno.id_alumno == id_usuario)
        ddbb_alumno = db.exec(query).first()

        if ddbb_alumno:
            query_asignatura = select(Asignatura).where(Asignatura.descripcion == jornada)
            ddbb_asignatura = db.exec(query_asignatura).first()
            if not ddbb_asignatura:
                print(f"No se encontró asignatura para jornada {jornada}")
                return
            registro_alumno = Clase(
                id_alumno=ddbb_alumno.id_alumno,
                id_asignatura=ddbb_asignatura.id_asignatura,
                hora=hh,
                dia=dd,
                mes=mm,
                anyo=aa,
                asistio=True
            )
            db.add(registro_alumno)
            db.commit()
            print(f"Asistencia registrada")
        else:
            query = select(Persona).where(Persona.id == id_usuario)
            ddbb_personal = db.exec(query).first()

            if not ddbb_personal:
                print(f"Tarjeta sin asignar {id_usuario}")
                return
            registro_personal = Trabaja(
                id_persona = ddbb_personal.id_persona,
                hora = hh,
                dia = dd,
                mes = mm,
                anyo = aa,
                asistio= True
            )
            db.add(registro_personal)
            db.commit()
            print(f"Asistencia registrada")

def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_forever()