from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import modelformset_factory


from userform.models import User, Student, Rfid, UserDoor, UserSystem
from usertable.forms import UserForm, StudentForm, RfidForm, UserDoorFormProfessor, UserDoorForm, UserSystemForm

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

def delete(request, pk):
    db = User.objects.get(pk=pk)
    db.delete()
    return redirect('table')

def update(request, pk, model):
    obj = None 
    userForm = None
    studentForm = None
    userDoorForm = None 
    rfidFormset = None
    userSystemForm = None
    if model == 1:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.userdoor
        userDoorForm = UserDoorFormProfessor(request.POST or None, instance=userDoor)
        userSystem = obj.usersystem
        userSystemForm = UserSystemForm(request.POST or None, instance=userSystem)
        qs = userDoor.rfid_set.all()
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)


        if userForm.is_valid() and userDoorForm.is_valid() and rfidFormset.is_valid():    
            user = userForm.save()
            
            userDoor = userDoorForm.save(commit=False)
            userDoor.user = user
            userDoor.save()

            userSystem = userSystemForm.save(commit=False)
            userSystem.user = user
            userSystem.save()                

            for form in rfidFormset:
                if form.has_changed():
                    rfid = form.save(commit=False)
                    rfid.user = userDoor
                    rfid.save()

            return redirect(reverse('table'))
    elif model == 2:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.userdoor
        userDoorForm = UserDoorForm(request.POST or None, instance=userDoor)
        stuobj = obj.student
        studentForm = StudentForm(request.POST or None, instance=stuobj)
        userSystem = obj.usersystem
        userSystemForm = UserSystemForm(request.POST or None, instance=userSystem)
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)

        if userSystemForm.is_valid() and studentForm.is_valid() and userDoorForm.is_valid() and rfidFormset.is_valid():
            user = userForm.save(commit=False)
            user.save()

            userDoor = userDoorForm.save(commit=False)
            userDoor.user = user
            userDoor.save()

            userSystem = userSystemForm.save(commit=False)
            userSystem.user = user
            userSystem.save()

            student = studentForm.save(commit=False)
            student.user = user
            student.save()

            for form in rfidFormset:
                if form.has_changed():
                    rfid = form.save(commit=False)
                    rfid.user = userDoor
                    rfid.save()
            return redirect(reverse('table'))
    elif model == 3:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)
        userDoor = obj.userdoor
        userDoorForm = UserDoorForm(request.POST or None, instance=userDoor)
        
        RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
        qs = userDoor.rfid_set.all()
        rfidFormset = RfidFormFormset(request.POST or None, queryset=qs)

        if userDoorForm.is_valid() and rfidFormset.is_valid():
            user = userForm.save(commit=False)
            user.save()

            userDoor = userDoorForm.save(commit=False)
            userDoor.user = user
            userDoor.save()


            for form in rfidFormset:
                if form.has_changed():
                    rfid = form.save(commit=False)
                    rfid.user = userDoor
                    rfid.save()
                    return redirect(reverse('table'))

    elif model == 4:
        obj = get_object_or_404(User, pk=pk)
        userForm = UserForm(request.POST or None, instance=obj)
        userSystem = obj.usersystem
        userSystemForm = UserSystemForm(request.POST or None, instance=userSystem)

        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.save()

            userSystem = userSystemForm.save(commit=False)
            userSystem.user = user
            userSystem.save()

            return redirect(reverse('table'))

    context = {
        "userForm": userForm, 
        "studentForm": studentForm,
        "userSystemForm": userSystemForm,
        "userDoorForm": userDoorForm,
        "rfidFormset": rfidFormset,
    }
    return render(request, 'editform.html', context)