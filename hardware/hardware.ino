//Includes
//Include WiFi
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
//Include LCD_I2C
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
//Include RFID reader
#include <MFRC522.h>
//Include MQTT+
#include <PubSubClient.h>

//Global Variables
//Config RfID ports
#define RST_PIN D0
#define SS_PIN0 D3
#define SS_PIN1 D4

//Config Button and Locker ports
#define locker 2
#define buzzer D8

//WiFi
const char* ssid     = "LARM_ALUNOS";
const char* password = "LarmUfscq2022";

//MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
// const char* MQTT_BROKER_IP_ADDRESS = "192.168.3.46";
// const char* MQTT_BROKER_IP_ADDRESS = "172.190.138.174";
// const char* MQTT_BROKER_IP_ADDRESS = "192.168.3.82";
// const char* MQTT_BROKER_IP_ADDRESS = "192.168.252.134";
const char* MQTT_BROKER_IP_ADDRESS = "150.162.234.90";

const char* MQTTUSERNAME = "Esp32";
const char* MQTTPWD = "JIa6sEtBt1JEmqm";

//RFID
MFRC522 rfid0(SS_PIN0, RST_PIN);
MFRC522 rfid1(SS_PIN1, RST_PIN);


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
	
	lcd.setCursor(0, (name.length()/2)-8);
	lcd.print(name);


	delay(1000);
	digitalWrite(locker,HIGH);
	delay(100);
	digitalWrite(locker,LOW);

	timer1_enable(TIM_DIV16, TIM_EDGE, TIM_SINGLE);
	timer1_write(5000000);
	
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

	timer1_enable(TIM_DIV16, TIM_EDGE, TIM_SINGLE);
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
		if(WiFi.status() != WL_CONNECTED){
			wifiStartup();
		}
		Serial.println("Tentando reconectar ao broker MQTT...");
		if (mqttClient.connect("ESP32Client", MQTTUSERNAME, MQTTPWD)) {		
			Serial.println("Reconectado ao broker MQTT!");
			// mqttClient.subscribe("door/enter");
			// mqttClient.subscribe("door/leave");
			// mqttClient.subscribe("door/notopen");			
			// mqttClient.subscribe("door/notauth");			
			mqttClient.subscribe("door/#");			
			mqttClient.subscribe("server/status");
			Serial.println("Conectado ao broker MQTT!");
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
	else if(strcmp(topic, "door/exit") == 0){
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
	timer1_disable();
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
	pinMode(buzzer, OUTPUT);

	wifiStartup();
	mqttStartup();

	SPI.begin(); // Init SPI bus

	Serial.println("RFID Reader 1");
	rfid0.PCD_Init(); // Init MFRC522
	Serial.println("RFID Reader 2");
	rfid1.PCD_Init(); // Init MFRC522
	Serial.println("RFID Activated");

	timer1_attachInterrupt(lcdResetInter);
	timer1_disable();
	
	lcd.clear();
    lcd.setCursor(2,0);
    lcd.print("Aproxime seu");
    lcd.setCursor(5,1);
    lcd.print("cartao");

}

void loop(){	
	// Verifica se a conexão com o broker MQTT está ativa e reconecta-se, se necessário
	if (!mqttClient.connected()) {
		reconnect();
	}
	// Processa as mensagens MQTT recebidas
	mqttClient.loop();

	if (rfid0.PICC_IsNewCardPresent() && rfid0.PICC_ReadCardSerial()){
        String cardUID;
        for (size_t i = 0; i < rfid0.uid.size; i++)
        {
            cardUID.concat(String(rfid0.uid.uidByte[i] < 0x10 ? "0" : ""));
            cardUID.concat(String(rfid0.uid.uidByte[i], HEX));
        }
        rfid0.PICC_HaltA();
		String message = "{\"side\":\"1\",\"cardUID\":\"" + cardUID + "\"}";
		mqttClient.publish("server/auth/outside", cardUID.c_str());
		Serial.println(message);
    }
	else if (rfid1.PICC_IsNewCardPresent() && rfid1.PICC_ReadCardSerial()){
		String cardUID;
		for (size_t i = 0; i < rfid1.uid.size; i++)
		{
			cardUID.concat(String(rfid1.uid.uidByte[i] < 0x10 ? "0" : ""));
			cardUID.concat(String(rfid1.uid.uidByte[i], HEX));
		}
        rfid1.PICC_HaltA();
		String message = "{\"side\":\"2\",\"cardUID\":\"" + cardUID + "\"}";
		mqttClient.publish("server/auth/inside", cardUID.c_str());
		Serial.println(message);
	}
	if(RLCD == true){
      resetLCD();
      RLCD = false;
    }
}

