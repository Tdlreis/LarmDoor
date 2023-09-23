from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import modelformset_factory
from user.forms import UserForm, StudentForm, RfidForm
from .models import User, Rfid
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    form = UserForm(request.POST or None)
    strudentForm = StudentForm(request.POST or None)
    RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=1)
    formset = RfidFormFormset(request.POST or None, queryset=Rfid.objects.none())

    strudentForm.fields['user_coordinator'].empty_label = ''

    context = {
        "form": form, 
        "formset": formset,
        "strudentForm": strudentForm,
        "initial": True
    }
    
    if request.method == 'POST':
        if form['user_type'].value() == "1" and form.is_valid() and formset.is_valid() and strudentForm.is_valid():
            parent = form.save(commit=False)
            parent.save()

            child = strudentForm.save(commit=False)
            child.user = parent
            child.save()

            for form in formset:
                if form.has_changed():
                    child = form.save(commit=False)
                    child.user = parent
                    child.rfid_uid = child.rfid_uid.upper()
                    child.save()

            return redirect(reverse('index'))
        elif form.is_valid() and formset.is_valid():
            parent = form.save(commit=False)
            parent.save()

            for form in formset:
                if form.has_changed():
                    child = form.save(commit=False)
                    child.user = parent
                    child.rfid_uid = child.rfid_uid.upper()
                    child.save()

            return redirect(reverse('index'))
        else:
            context = {
                "form": form, 
                "formset": formset,
                "strudentForm": strudentForm,
                "username": form.errors.get('username'), 
                "email": form.errors.get('email'), 
                "user_type": form.errors.get('user_type'),
                "password": form.errors.get('password')
            }
            # print(context)
    
    return render(request, 'form.html', context)
