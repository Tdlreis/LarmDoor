//Includes
//Include WiFi
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
//Include LCD_I2C
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
//Include RFID reader
#include <MFRC522.h>
//Include MQTT
#include <PubSubClient.h>

//Global Variables
//Config RfID ports
#define RST_PIN 5
#define SS_PIN0 17
#define SS_PIN1 16

//Config Button and Locker ports
#define locker 2

//WiFi
const char* ssid     = "TDLR";
const char* password = "Thiago2001";

//MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
const char* MQTT_BROKER_IP_ADDRESS = "192.168.3.46";
// const char* MQTT_BROKER_IP_ADDRESS = "172.190.138.174";
const char* MQTTUSERNAME = "esp32";
const char* MQTTPWD = "n9tt-9g0a-b7fq-ranc";

//RFID
// MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522 rfid[2] = {MFRC522(SS_PIN0, RST_PIN), MFRC522(SS_PIN1, RST_PIN)};


//LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

//Timer
bool RLCD = false;
bool online = false;


//Setup Functions
void mqttStartup(){
    // Configura o servidor MQTT e o cliente MQTT
    mqttClient.setServer(MQTT_BROKER_IP_ADDRESS, 1883);
    mqttClient.setCallback(mqttCallback);
    reconnect();
}

void wifiStartup(){
	Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

	lcd.clear();
	lcd.setCursor(6, 0);
	lcd.print("WiFi");
	lcd.setCursor(2, 1);
	lcd.print("connecting");
	
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
	}
}

void openDoor(String name, bool enter){
	lcd.clear();
	if (enter)
	{
		lcd.setCursor(2, 0);
		lcd.print("Bem vindo(a)");		
	}
	else
	{
		lcd.setCursor(3, 0);
		lcd.print("Volte Logo");
	}
	
	
	if(name.length()>16){
		for (int pos = 0; pos < name.length()-15; pos++) {
			lcd.setCursor(0, 1);
			lcd.print(name.substring(pos, pos + 16));
			delay(500);
		}
	}
	else{
		lcd.setCursor(0, (name.length()/2)-8);
		lcd.print(name);
	} 

	delay(1000);
	digitalWrite(locker,HIGH);
	delay(100);
	digitalWrite(locker,LOW);

	timerRestart(refreshTimer);
    timerStart(refreshTimer);
}

void notOpenDoor(bool auth){
	lcd.clear();
	lcd.setCursor(5,0);
	lcd.print("Cartao");
	lcd.setCursor(1,3);
	if(auth){
		lcd.print("Nao autorizado");
	}
	else{
		lcd.print("Nao cadastrado");
	}

	// timer1_enable(TIM_DIV16, TIM_EDGE, TIM_SINGLE);
	timer1_write(5000000);
}

//MQTT
//Reconects to MQTT Server
void reconnect() {
	lcd.clear();
	lcd.setCursor(6, 0);
	lcd.print("MQTT");
	lcd.setCursor(2, 1);
	lcd.print("connecting");
	while (!mqttClient.connected()) {
		Serial.println("Tentando reconectar ao broker MQTT...");
		if (mqttClient.connect("ESP32Client", MQTTUSERNAME, MQTTPWD)) {		
			Serial.println("Reconectado ao broker MQTT!");
			// mqttClient.subscribe("door/enter");
			// mqttClient.subscribe("door/leave");
			// mqttClient.subscribe("door/notopen");			
			// mqttClient.subscribe("door/notauth");			
			mqttClient.subscribe("door/#");			
			mqttClient.subscribe("server/status");
		} else {
			Serial.print("Falha ao se reconectar ao broker MQTT com erro: ");
			Serial.println(mqttClient.state());
		}
	}
}

//MQTT Callback Function
void mqttCallback(char* topic, byte* payload, unsigned int length) {
	payload[length] = '\0';
	String message = (char*)payload;

	if(length == 0){}
	else if(strcmp(topic, "door/enter") == 0){
		openDoor(message, true);
	}
	else if(strcmp(topic, "door/leave") == 0){
		openDoor(message, false);
	}
	else if(strcmp(topic, "door/notopen") == 0){
		notOpenDoor(false);
	}
	else if(strcmp(topic, "door/notauth") == 0){
		notOpenDoor(true);
	}
	else if (strcmp(topic, "server/status") == 0)
	{
		if(message == "offline"){
			lcd.clear();
			lcd.setCursor(0,0);
			lcd.print("O Servidor esta:");
			lcd.setCursor(0,1);
			lcd.print("Offline");
			online = false;
			while (online == false)
			{
				// Verifica se a conexão com o broker MQTT está ativa e reconecta-se, se necessário
				if (!mqttClient.connected()) {
					reconnect();
				}
				// Processa as mensagens MQTT recebidas
				mqttClient.loop();
			}
		}
		else{
			resetLCD();
			online = true;
		}
	}
	



	Serial.print("Mensagem MQTT recebida no topico [");
	Serial.print(topic);
	Serial.print("]: ");
	Serial.println(message);
}

//LCD reset
void IRAM_ATTR lcdResetInter(){
    RLCD = true;
	// timer1_disable();
}

void resetLCD(){
	lcd.clear();
    lcd.setCursor(2,0);
    lcd.print("Aproxime seu");
    lcd.setCursor(5,1);
    lcd.print("cartao");
}

void setup(){
  	Serial.begin(115200);
	delay(10);
	lcd.init();
    lcd.backlight();
	lcd.clear();

	pinMode(locker, OUTPUT);

	wifiStartup();
	mqttStartup();
	SPI.begin(); // Init SPI bus
    rfid.PCD_Init(); // Init MFRC522

	timer1_attachInterrupt(lcdResetInter);
	timer1_enable(TIM_DIV16, TIM_EDGE, TIM_SINGLE);
	timer1_write(5000000);
	timer1_disable();
	
	lcd.clear();
    lcd.setCursor(2,0);
    lcd.print("Aproxime seu");
    lcd.setCursor(5,1);
    lcd.print("cartao");

}

void loop(){
	if(WiFi.status() != WL_CONNECTED){
		wifiStartup();
	}
	// Verifica se a conexão com o broker MQTT está ativa e reconecta-se, se necessário
	if (!mqttClient.connected()) {
		reconnect();
	}
	// Processa as mensagens MQTT recebidas
	mqttClient.loop();

	if (rfid[0].PICC_IsNewCardPresent() && rfid[0].PICC_ReadCardSerial()){
        String cardUID;
        for (size_t i = 0; i < rfid[0].uid.size; i++)
        {
            cardUID.concat(String(rfid[0].uid.uidByte[i] < 0x10 ? "0" : ""));
            cardUID.concat(String(rfid[0].uid.uidByte[i], HEX));
        }
        rfid[0].PICC_HaltA();
		Serial.println(cardUID);
		String message = "{\"side\":\"1\",\"cardUID\":\"" + cardUID + "\"}";
		mqttClient.publish("server/auth", message.c_str());
    }
	else if (rfid[1].PICC_IsNewCardPresent() && rfid[1].PICC_ReadCardSerial()){
		String cardUID;
		for (size_t i = 0; i < rfid[1].uid.size; i++)
		{
			cardUID.concat(String(rfid[1].uid.uidByte[i] < 0x10 ? "0" : ""));
			cardUID.concat(String(rfid[1].uid.uidByte[i], HEX));
		}
        rfid[1].PICC_HaltA();
		Serial.println(cardUID);
		String message = "{\"side\":\"1\",\"cardUID\":\"" + cardUID + "\"}";
		mqttClient.publish("server/auth", message.c_str());
	}
	if(RLCD == true){
      resetLCD();
      RLCD = false;
    }
}

