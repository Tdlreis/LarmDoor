from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import modelformset_factory
from user.forms import UserForm, StudentForm, RfidForm, IntroForm, UserDoorForm
from .models import User, Rfid
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    introform = IntroForm(request.POST or None)
    userForm = UserForm(request.POST or None)
    studentForm = StudentForm(request.POST or None)
    userDoorForm = UserDoorForm(request.POST or None)


    RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=1)
    rfidFormset = RfidFormFormset(request.POST or None, queryset=Rfid.objects.none())

    studentForm.fields['user_coordinator'].empty_label = ''

    
    if request.method == 'POST':
        if introform.is_valid():
            full_name = introform.cleaned_data['full_name']
            user_type = introform.cleaned_data['user_type']            
            
            if user_type == "1":
                if userForm.is_valid() and studentForm.is_valid() and userDoorForm.is_valid() and rfidFormset.is_valid():
                    userDoor = userDoorForm.save(commit=False)
                    userDoor.full_name = full_name
                    userDoor.save()

                    user = userForm.save(commit=False)
                    user.full_name = full_name
                    user.user_type = user_type
                    user.doorUser = userDoor
                    user.save()

                    student = studentForm.save(commit=False)
                    student.user = user
                    student.save()


                    for form in rfidFormset:
                        if form.has_changed():
                            rfid = form.save(commit=False)
                            rfid.user = userDoor
                            rfid.save()
                    
                    return redirect(reverse('index'))
            elif user_type == "2":
                userDoorForm.fields['expiration_date'].required = False
                if userForm.is_valid() and userDoorForm.is_valid() and rfidFormset.is_valid():    
                    print("entrou")                
                    userDoor = userDoorForm.save(commit=False)
                    userDoor.full_name = full_name
                    userDoor.save()

                    user = userForm.save(commit=False)
                    user.full_name = full_name
                    user.user_type = user_type
                    user.doorUser = userDoor
                    user.save()

                    for form in rfidFormset:
                        if form.has_changed():
                            rfid = form.save(commit=False)
                            rfid.user = userDoor
                            rfid.save()
                    
                    return redirect(reverse('index'))
            elif user_type == "3":
                if userDoorForm.is_valid() and rfidFormset.is_valid():
                    userDoor = userDoorForm.save(commit=False)
                    userDoor.full_name = full_name
                    userDoor.save()


                    for form in rfidFormset:
                        if form.has_changed():
                            rfid = form.save(commit=False)
                            rfid.user = userDoor
                            rfid.save()

                    return redirect(reverse('index'))
            elif user_type == "4":
                if userForm.is_valid():
                    user = userForm.save(commit=False)
                    user.full_name = full_name
                    user.user_type = user_type
                    user.save()

                    return redirect(reverse('index'))

    context = {
        "introform": introform,
        "userForm": userForm, 
        "studentForm": studentForm,
        "rfidFormset": rfidFormset,
        "userDoorForm": userDoorForm,
    }
    return render(request, 'form.html', context)
