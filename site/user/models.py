from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.conf import settings
from cryptography.fernet import Fernet


class User(AbstractUser):
    username = models.CharField('Usuário', unique=True, max_length=100)
    email = models.EmailField('E-mail', unique=True)
    authorization = models.BooleanField('Autorização', default=False)
    user_type = models.PositiveSmallIntegerField()
    created_by = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_course = models.CharField('Curso', max_length=100)
    institution_code = models.IntegerField('Matrícula', unique=True)

    user_coordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinator', limit_choices_to={'user_type': 3})
    user_project = models.CharField('Projeto', max_length=100)
  
class Uuid(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()
    
class Rfid(models.Model):
    rfid_uid = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
