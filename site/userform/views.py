from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import modelformset_factory
from userform.forms import UserForm, StudentForm, RfidForm, UserSystemForm, UserDoorForm
from .models import User, Rfid
from django.http import JsonResponse

def create(request):
    userForm = UserForm(request.POST or None)
    userSystemForm = UserSystemForm(request.POST or None)
    studentForm = StudentForm(request.POST or None)
    userDoorForm = UserDoorForm(request.POST or None)


    RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=1)
    rfidFormset = RfidFormFormset(request.POST or None, queryset=Rfid.objects.none())

    studentForm.fields['user_coordinator'].empty_label = ''

    
    if request.method == 'POST':
        if userForm.is_valid():
            user_type = userForm.cleaned_data['user_type']            
            
            if user_type == "1":
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
            elif user_type == "2":
                userDoorForm.fields['expiration_date'].required = False
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
            elif user_type == "3":
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
            elif user_type == "4":
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
        "rfidFormset": rfidFormset,
        "userDoorForm": userDoorForm,
    }
    return render(request, 'form.html', context)
