# control-d-assistencia 

## main.py
El fitxer main.py és el punt d’entrada del backend desenvolupat amb FastAPI. Les seves funcions principals són:  
* Inicialització de la base de dades: carrega la URL des de .env, crea l’engine amb SQLModel i genera les taules.  
* Gestió de sessions: defineix la dependència get_db() per obrir i tancar connexions de manera segura.  
* Integració amb MQTT: en l’event startup, inicia un fil que executa el servei mqtt_service per escoltar missatges d’AWS IoT.  
* API REST: implementa endpoints CRUD per a les entitats principals:  
  * CREATE: alumnes, treballadors i assignatures.  
  * READ: llistat d’alumnes, treballadors, assignatures, assistències i horaris.  
  * UPDATE: modificació d’alumnes i treballadors (incloent canvi de rol).  
  * DELETE: eliminació d’alumnes, treballadors i assignatures.  

En conjunt, main.py proporciona la interfície REST que permet gestionar les dades del sistema i coordinar-les amb el servei MQTT.  
## mqtt_service.py
El fitxer mqtt_service.py és el mòdul encarregat de la comunicació amb AWS IoT Core mitjançant el protocol MQTT. Les seves funcions principals són:  
* Configuració de connexió: carrega endpoint, port, certificats i claus TLS des de .env.  
* Subscripció i publicació:  
  * Subscriu al topic rfid/tag per rebre els IDs de targeta enviats per l’Arduino.  
  * Publica al topic rfid/led la resposta (1 per LED verd, 0 per LED vermell).
* Processament de missatges:  
  * Decodifica el payload rebut i comprova si l’ID existeix a la base de dades.  
  * Si és alumne → registra assistència a la taula Asiste.  
  * Si és treballador → registra assistència a la taula Horario_T.  
  * Si no existeix o hi ha duplicat → publica 0 i mostra error.  
* Gestió d’errors: controla excepcions d’integritat (IntegrityError) per evitar registres duplicats.  
* Execució contínua: la funció start_mqtt() manté el client en bucle (loop_forever) per escoltar missatges en temps real.  

Aquest mòdul actua com a pont entre el hardware (Arduino) i el backend, garantint la sincronització immediata entre la lectura de targetes i el registre d’assistència.  

Ambdós mòduls formen el nucli del sistema, combinant backend modern i comunicació IoT segura per automatitzar el registre d’assistència.  