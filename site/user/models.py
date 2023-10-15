from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.conf import settings
from cryptography.fernet import Fernet

class UserDoor(models.Model):
    full_name = models.CharField('Nome Completo', max_length=100, unique=True)
    nickname = models.CharField('Apelido', max_length=12, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

class User(AbstractUser):
    full_name = models.CharField('Nome Completo', max_length=100, unique=True)
    email = models.EmailField('E-mail', unique=True)
    user_type = models.PositiveSmallIntegerField()
    is_admin = models.BooleanField('Administrador', default=False)
    is_analist = models.BooleanField('Analista', default=False)

    authorization = models.BooleanField('Autorização', default=False)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    doorUser = models.ForeignKey(UserDoor, on_delete=models.CASCADE, blank=True, null=True)


    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'user_type']
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


    def __str__(self):
        return self.full_name   
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_course = models.CharField('Curso', max_length=100)
    institution_code = models.IntegerField('Matrícula', unique=True)

    user_coordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinator', limit_choices_to={'user_type': 2})
    user_project = models.CharField('Projeto', max_length=100)

class Rfid(models.Model):
    rfid_uid = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(UserDoor, on_delete=models.CASCADE)
    authorization = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.rfid_uid = self.rfid_uid.upper()
        fernet = Fernet(settings.SECRET_KEY);
        self.rfid_uid = fernet.encrypt(self.rfid_uid.encode())
        super(Rfid, self).save(*args, **kwargs)

class PunchCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    punch_in_time = models.DateTimeField()    
    punch_out_time = models.DateTimeField(null=True, blank=True)
    reviw =  models.BooleanField(default=False)
    out  = models.BooleanField(default=True)
