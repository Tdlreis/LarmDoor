from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from .models import User, Student, Rfid, UserDoor, UserSystem
from django.core.validators import RegexValidator

class UserForm(forms.ModelForm):
    full_name = forms.CharField(label="Nome Completo", max_length=100)
    user_type = forms.ChoiceField(label="Tipo de Usuário",choices=[('','Selecione uma opção'), (1,'Aluno'), (2,"Professor"), (3, "Visitante"), (4, "Observador")], widget=forms.Select(attrs={'id': 'id_user_type'}))
    authorization = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['full_name', 'user_type', 'authorization']

class UserDoorForm(forms.ModelForm):
    nickname = forms.CharField(label="Apelido", max_length=12, required=True, validators=[RegexValidator(r'^[0-9a-zA-Z ]*$', 'Apenas letras e números são permitidos')])
    expiration_date = forms.DateField(label="Data de Expiração", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = UserDoor
        fields = ['nickname', 'expiration_date']

class UserSystemForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserSystem
        fields = ['email', 'password', 'is_admin' ,'is_analist']

class StudentForm(forms.ModelForm):
    institution_code = forms.CharField(label="Matricula:", max_length=8)

    class Meta:
        model = Student
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