from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import modelformset_factory


from userform.models import User, Student, Rfid, UserDoor, UserSystem
from usertable.forms import UserForm, StudentForm, RfidForm, UserDoorFormTemp, UserDoorFormProfessor, UserDoorFormStudent

# Create your views here.
def table(request):
    professores = User.objects.select_related('usersystem').filter(user_type=2)

    alunos = User.objects.select_related('usersystem', 'student').filter(user_type=1)
    
    visitantes = User.objects.select_related('userdoor').filter(user_type=3)

    observadores = User.objects.select_related('usersystem').filter(user_type=4)
    
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
        db.delete()
    elif(model == 2):
        db = User.objects.get(pk=pk)
        db.delete()
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
        qs = userDoor.rfid_set.all()
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)
        if userForm.is_valid() and userDoorForm.is_valid() and rfidFormset.is_valid():    
            userDoor = userDoorForm.save(commit=False)
            userDoor.save()

            user = userForm.save(commit=False)
            user.full_name = userDoor.full_name
            user.doorUser = userDoor
            user.save()

            for form in rfidFormset:
                if form.has_changed():
                    rfid = form.save(commit=False)
                    rfid.user = userDoor
                    rfid.save()
            return redirect(reverse('table'))
    elif model == 2:
        obj = get_object_or_404(User, pk=pk)
        stuobj = get_object_or_404(Student, user=obj)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.doorUser
        studentForm = StudentForm(request.POST or None, instance=stuobj)
        userDoorForm = UserDoorFormStudent(request.POST or None, instance=userDoor)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)

    elif model == 3:
        userDoor = get_object_or_404(UserDoor, pk=pk)
        userDoorForm = UserDoorFormTemp(request.POST or None, instance=userDoor)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)

    elif model == 4:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)

    context = {
        "userForm": userForm, 
        "studentForm": studentForm,
        "userDoorForm": userDoorForm,
        "rfidFormset": rfidFormset,
    }
    return render(request, 'editform.html', context)