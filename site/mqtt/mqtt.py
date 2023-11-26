import paho.mqtt.client as mqtt
from django.conf import settings
from userform.models import UserDoor, Rfid
from django.utils import timezone
from cryptography.fernet import Fernet
import time
import socket
import threading

lastRfid = None

def getLastRfid():
    global lastRfid
    temp = lastRfid
    lastRfid = None
    return temp

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.publish("server/status", "online", 2, True)
    else:
        print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    if msg.topic.startswith("server/auth/"):
        try:
            global lastRfid
            lastRfid = msg.payload.decode("utf-8").upper()

            # fernet = Fernet(settings.SECRET_KEY1);
            # crypt = fernet.encrypt(lastRfid.encode()).decode()
            # print(crypt)

            rfid = Rfid.objects.get(rfid_uid=lastRfid)
            user = rfid.user

            if user.expiration_date < timezone.now().date():
                user.authorization = False
                user.save()
                client.publish("door/notauth", " ")
            elif not user.authorization:
                client.publish("door/notauth", " ")
            elif not rfid.authorization:
                client.publish("door/notauth", " ")
            else:
                client.publish("door/enter", user.nickname)
                topic_parts = msg.topic.split('/')
                last_part = topic_parts[-1]
                print(last_part)
                # if last_part == 'in':
                #     punch_in(user.pk)
                # elif last_part == 'out':
                #     punch_out(user.pk)
   
        except Rfid.DoesNotExist:
            print("Não encontrado")
            client.publish("door/notopen", " ")
            pass
        
    
def on_disconnect(client, userdata, rc):
    client.loop_stop()
    mqtt_thread = threading.Thread(target=establish_mqtt_connection)
    mqtt_thread.start()

def start_mqtt_handler():
    mqtt_thread = threading.Thread(target=establish_mqtt_connection)
    mqtt_thread.start()

def establish_mqtt_connection():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_disconnect = on_disconnect

    # Set MQTT broker credentials if required
    if settings.MQTT_USER and settings.MQTT_PASSWORD:
        client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    client.will_set("server/status", "offline", 2, True)

    while True:
        try:
            client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, 60)
            # Subscribe to topics
            for topic in settings.MQTT_TOPICS:
                client.subscribe(topic, qos=2)

            # Start the MQTT loop in a non-blocking manner
            client.loop_start()
            break
        except socket.error as e:
            # Handle the socket connection error
            print(f"Socket connection error: {e}")
            # time.sleep(1)

