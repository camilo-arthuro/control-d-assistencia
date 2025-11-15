from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime, date, time
from app.model.UserTic import Alumno, Trabajador
from app.model.clase import Asignatura, Asiste, Horario_T
import paho.mqtt.client as mqtt
import os

load_dotenv()

'''
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")
'''

# AWS IoT MQTT
AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
AWS_IOT_PORT = int(os.getenv("AWS_IOT_PORT", 8883))
AWS_IOT_TOPIC = os.getenv("AWS_IOT_TOPIC")
AWS_IOT_CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID")
AWS_IOT_CERT = os.getenv("AWS_IOT_CERT")
AWS_IOT_KEY = os.getenv("AWS_IOT_KEY")
AWS_IOT_ROOT_CA = os.getenv("AWS_IOT_ROOT_CA")

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
    print("Conectado a AWS IoT con codigo:", rc)
    client.subscribe(AWS_IOT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload}")

    try:
        payload = msg.payload.decode()
        print("Payload decodificado: ", payload)
    except Exception as e:
        print("Formato inesperado, no se pudo convertir: ", e)
        payload = "Formato inesperado"
    id_usuario = str(payload)
    info_fecha = datetime.now()
    fecha_actual = info_fecha.date()
    hh = info_fecha.hour
    mm = info_fecha.minute
    hora_actual=time(hh,mm)

    with (Session(engine) as db):
        query = select(Alumno).where(Alumno.id_alumno == id_usuario)
        ddbb_alumno = db.exec(query).first()
        if not ddbb_alumno:
            query_trabajador=select(Trabajador).where(Trabajador.id_persona == id_usuario)
            ddbb_trabajador=db.exec(query_trabajador).first()
            if not ddbb_trabajador:
                return print(f"Tarjeta sin asignar: {id_usuario}")
            else:
                registro_trabajador=Horario_T(
                    id_personal=id_usuario,
                    fecha=fecha_actual,
                    hora=hora_actual
                )
                db.add(registro_trabajador)
                db.commit()
                return print(f"Asistencia registrada {id_usuario}")
        else:
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

def start_mqtt():
    client = mqtt.Client(client_id=AWS_IOT_CLIENT_ID)
    client.tls_set(ca_certs=AWS_IOT_ROOT_CA,
                   certfile=AWS_IOT_CERT,
                   keyfile=AWS_IOT_KEY)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(AWS_IOT_ENDPOINT, AWS_IOT_PORT, keepalive=60)
    client.loop_forever()
