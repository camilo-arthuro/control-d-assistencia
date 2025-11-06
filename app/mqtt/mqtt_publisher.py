import paho.mqtt.client as mqtt
import time
import json

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "test/control-assistencia"

client = mqtt.Client()

client.connect(MQTT_HOST, MQTT_PORT)

payload = "1"
client.publish(MQTT_TOPIC, payload)
print(f"Mensaje enviado: {payload}")

'''
for i in range(5):
    payload = {
        "id_usuario": f"user_{i}",
        "timestamp": time.time(),
        "evento": "entrada"
    }
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"Mensaje enviado: {payload}")
    time.sleep(2)  # Espera entre mensajes
'''
client.disconnect()
