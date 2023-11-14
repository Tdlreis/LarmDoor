from cryptography.fernet import Fernet

# fernet = Fernet.generate_key()
# print(fernet)

SECRET_KEY1 = b'ComMmOzeo3K1BG1CxiZ6l8PkYecQzWjwjYukFGHwmZ0='
fernet = Fernet(SECRET_KEY1)
print(fernet)

# mensagem = "teste"
# print(mensagem)
# mensagem = mensagem.encode()
# print(mensagem)
# rfid_uid = fernet.encrypt(mensagem)
# print(rfid_uid)

rfid_uid = fernet.decrypt(b'gAAAAABlRABtvmbqolbuZZUHCSTPTvTnPpVD3_iwDlexWUipukGHWxjnhHMEcc7uYlMikct7eeshl9_v_nbAsRFGOX1g2jsrpg==')
print(rfid_uid)
rfid_uid = rfid_uid.decode()
print(rfid_uid)