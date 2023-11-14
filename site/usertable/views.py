from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import modelformset_factory
from django.conf import settings
from cryptography.fernet import Fernet

from userform.models import User, Rfid
from usertable.forms import UserForm, StudentForm, RfidForm, UserDoorForm, UserDoorFormProfessor

# Create your views here.
def table(request):
    professores = User.objects.filter(user_type=2)

    alunos = Student.objects.select_related('user')
    
    visitantes = UserDoor.objects.filter(isUser=0)

    observadores = User.objects.filter(user_type=4)
    
    context = {
        'Professores': professores,
        'Alunos': alunos,
        'Visitantes': visitantes,
        'Observadores': observadores,
    }

    return render(request, 'usertable.html', context)

def delete(request, pk, model):
    if(model == 1):
        db = User.objects.get(pk=pk)
        db2 = db.doorUser
        db.delete()
        db2.delete()
    elif(model == 2):
        db = User.objects.get(pk=pk)
        db2 = db.doorUser
        db.delete()
        db2.delete()
    elif(model == 3):
        db = UserDoor.objects.get(pk=pk)
        db.delete() 
    elif(model == 4):
        db = User.objects.get(pk=pk)
        db.delete()
    return redirect('table')

def update(request, pk, model):
    obj = None 
    userForm = None
    studentForm = None
    userDoorForm = None 
    rfidFormset = None
    if model == 1:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.doorUser
        userDoorForm = UserDoorFormProfessor(request.POST or None, instance=userDoor)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)
        
    elif model == 2:
        obj = get_object_or_404(User, pk=pk)
        stuobj = get_object_or_404(Student, user=obj)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.doorUser
        studentForm = StudentForm(request.POST or None, instance=stuobj)
        userDoorForm = UserDoorFormProfessor(request.POST or None, instance=userDoor)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)

    elif model == 3:
        userDoor = get_object_or_404(UserDoor, pk=pk)
        userDoorForm = UserDoorFormProfessor(request.POST or None, instance=userDoor)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)
    elif model == 4:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)

    if rfidFormset:
        fernet = Fernet(settings.SECRET_KEY1)
        for rfid in qs:
            print(rfid.rfid_uid)
            rfid.rfid_uid = fernet.decrypt(rfid.rfid_uid)
    
    context = {
        "userForm": userForm, 
        "studentForm": studentForm,
        "userDoorForm": userDoorForm,
        "rfidFormset": rfidFormset,
    }
    return render(request, 'editform.html', context)