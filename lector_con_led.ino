#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  22
#define SS_PIN   5
int led = 25;

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  while (!Serial);
  
  pinMode(led, OUTPUT);
  Serial.println("=== LECTOR RFID RC522 - CODIGO CORREGIDO ===");
  
  // Iniciar SPI
  SPI.begin();
  
  // Iniciar MFRC522
  mfrc522.PCD_Init();
  delay(4);
  
  // Mostrar versión del firmware
  Serial.print("Firmware MFRC522: ");
  mfrc522.PCD_DumpVersionToSerial();
  
  Serial.println("Coloca una tarjeta cerca del lector...");
  Serial.println();
}

void loop() {
  // Verificar si hay una tarjeta presente
  if (!mfrc522.PICC_IsNewCardPresent()) {
    delay(50);
    return;
  }
  
  // Intentar leer la tarjeta
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Tarjeta leída correctamente
  Serial.println("✅ TARJETA DETECTADA CORRECTAMENTE");
  digitalWrite(led, HIGH);
  
  // Mostrar UID
  Serial.print("UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();
  
  // Mostrar tipo de tarjeta - FORMA CORREGIDA
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.print("Tipo: ");
  Serial.println(mfrc522.PICC_GetTypeName(piccType));
  
  // Mostrar tamaño
  Serial.print("Tamaño UID: ");
  Serial.print(mfrc522.uid.size);
  Serial.println(" bytes");
  
  Serial.println("================================");
  Serial.println();
  
  // Detener comunicación
  mfrc522.PICC_HaltA();
  delay(2000);
  digitalWrite(led, LOW);
}