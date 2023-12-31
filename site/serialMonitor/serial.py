from userform.models import Rfid, UserDoor, PunchCard
from django.utils import timezone
import threading
import serial 
import time
from minha_dashboard.models import Entradas
from django.db.models import Count
import random

lastRfid = None

def getLastRfid():
    global lastRfid
    temp = lastRfid
    lastRfid = None
    return temp

def start_serial_handler():
    door_serial_thread = threading.Thread(target=door_serial_connection)
    door_serial_thread.start()
    sensor_serial_thread = threading.Thread(target=sensor_serial_connection)
    sensor_serial_thread.start()

def sensor_serial_connection():
    ser = connect_to_serial("/dev/ttyACM0", 9600)
    people_count = 0

    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip().upper()
                print(data)

                values = data.split(',')
                if len(values) == 3:
                    people_count = PunchCard.objects.filter(punch_out_time__isnull=True).values('user').distinct().count()
                    print(f"Number of people in the room: {people_count}")

                    entrada = Entradas(temperatura=values[0], humidade=values[1], lux=values[2], alunos=people_count, voltagem=random.randint(0, 220))
                    entrada.save()
                    print("Data inserted into minhadashboard_entradas table.")
                    
                else:
                    print("Invalid data format.")
                
        except:
            ser = connect_to_serial("/dev/ttyACM0", 9600)

def connect_to_serial(port, baudrate):
    start_time = time.time()
    while True:
        try:
            ser = serial.Serial(port, baudrate)
            print("Conexão serial estabelecida.")
            return ser
        except serial.serialutil.SerialException:
            elapsed_time = time.time() - start_time
            if elapsed_time > 600:  # 600 segundos = 10 minutos
                print("Falha ao estabelecer conexão serial após 10 minutos.")
                return None
            wait_time = min(30, elapsed_time / 2)  # Espera até 30 segundos
            print(f"Falha ao conectar. Tentando novamente em {wait_time} segundos...")
            time.sleep(wait_time)

def door_serial_connection():
    ser1 = connect_to_serial("/dev/ttyUSB0", 9600)
    ser2 = connect_to_serial("/dev/ttyACM1", 9600)

    while True:     
        try:      
            if ser1.in_waiting > 0:
                teste = ser1.readline().decode('utf-8').strip().upper()
                print(teste)
                response = chek_db(teste)
                if response == False:
                    ser1.write(b'NOK!')
                    time.sleep(0.5)
                else:
                    ser1.write(response.nickname.encode() + b'!')
                    punch_in(response.pk)
                    time.sleep(0.5)
        except:
            ser1 = connect_to_serial("/dev/ttyUSB0", 9600)
        try:
            if ser2.in_waiting > 0:
                teste = ser2.readline().decode('utf-8').strip().upper()
                print(teste)
                response = chek_db(teste)
                if response == False:
                    ser1.write(b'NOK!')
                    time.sleep(0.5)
                else:
                    ser1.write(response.nickname.encode() + b'!')
                    punch_out(response.pk)
                    time.sleep(0.5)
        except:
            ser2 = connect_to_serial("/dev/ttyACM1", 9600)

def chek_db(code):
    try:
        rfid = Rfid.objects.get(rfid_uid=code)
        user = rfid.user
        print(user.nickname)

        if user.expiration_date is not None and user.expiration_date < timezone.now().date():
            user.authorization = False
            user.save()
            print("door/notauth - Data de expiração vencida")
            return False
        elif not user.user.authorization:
            print("door/notauth - Usuário não autorizado")
            return False
        elif not rfid.authorization:
            print("door/notauth - Cartão não autorizado")
            return False
        else:
            return user

    except Rfid.DoesNotExist:
        global lastRfid
        lastRfid = code
        print("Não encontrado")
        return False

def punch_in(user_id):
    user = UserDoor.objects.get(pk=user_id)
    current_time = timezone.now()
    last_punch = user.punchcard_set.last()

    if last_punch != None and last_punch.punch_in_time != None and (current_time - last_punch.punch_in_time).total_seconds() < 30:
        last_punch.punch_in_time = current_time
        last_punch.save()
    else:
        PunchCard.objects.create(user=user, punch_in_time=current_time)

def punch_out(user_id):
    user = UserDoor.objects.get(pk=user_id)
    current_time = timezone.now()
    last_punch = user.punchcard_set.last()
    
    if last_punch != None and last_punch.punch_out_time == None:
        last_punch.punch_out_time = current_time
        last_punch.save()
    else:
        if last_punch != None and (current_time - last_punch.punch_out_time).total_seconds() < 30:
            last_punch.punch_out_time = current_time
            last_punch.save()
        else:
            PunchCard.objects.create(user=user, punch_out_time=current_time)

