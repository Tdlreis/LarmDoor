from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from userform.models import User, Rfid
from django.core.validators import RegexValidator

class UserDoorForm(forms.ModelForm):
    nickname = forms.CharField(label="Apelido", max_length=12, required=True, validators=[RegexValidator(r'^[0-9a-zA-Z ]*$', 'Apenas letras e números são permitidos')])
    expiration_date = forms.DateField(label="Data de Expiração", widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ['full_name', 'nickname', 'expiration_date']
        exclude = ['full_name']

class UserDoorFormProfessor(forms.ModelForm):
    nickname = forms.CharField(label="Apelido", max_length=12, required=True, validators=[RegexValidator(r'^[0-9a-zA-Z ]*$', 'Apenas letras e números são permitidos')])
    class Meta:
        model = User
        fields = ['full_name', 'nickname', 'expiration_date']
        exclude = ['full_name', 'expiration_date']

class UserForm(forms.ModelForm):
    authorization = forms.BooleanField(required=False, initial=True)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'user_type','is_admin' ,'is_analist', 'authorization']
        exclude = ['user_type', 'password']

class StudentForm(forms.ModelForm):
    institution_code = forms.CharField(label="Matricula:", max_length=8)

    class Meta:
        model = User
        fields = ['user_course', 'institution_code', 'user_coordinator', 'user_project']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['user_course'].label = "Curso:"
        self.fields['user_coordinator'].label = "Orientador:"
        self.fields['user_project'].label = "Projeto:"

class RfidForm(forms.ModelForm):
    rfid_uid = forms.CharField(label="",  max_length=8)
    authorization = forms.BooleanField(label="", required=False, initial=True)
    class Meta:
        model = Rfid
        fields = ["rfid_uid", "authorization"]

    def clean_rfid_uid(self):
        upper = self.cleaned_data['rfid_uid']
        return upper.upper()