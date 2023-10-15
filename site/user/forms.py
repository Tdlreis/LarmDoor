from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from .models import User, Student, Rfid, UserDoor
from django.core.validators import RegexValidator

class IntroForm(forms.Form):
    full_name = forms.CharField(label="Nome Completo", max_length=100)
    user_type = forms.ChoiceField(label="Tipo de Usuário",choices=[('','Selecione uma opção'), (1,'Aluno'), (2,"Professor"), (3, "Visitante"), (4, "Observador")], widget=forms.Select(attrs={'id': 'id_user_type'}))

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if User.objects.filter(full_name=full_name).exists() or UserDoor.objects.filter(full_name=full_name).exists():
            raise forms.ValidationError("Usuario já cadastrado")
        return full_name


class UserDoorForm(forms.ModelForm):
    nickname = forms.CharField(label="Apelido", max_length=12, required=True, validators=[RegexValidator(r'^[0-9a-zA-Z]*$', 'Apenas letras e números são permitidos')])
    expiration_date = forms.DateField(label="Data de Expiração", widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = UserDoor
        fields = ['full_name', 'nickname', 'expiration_date']
        exclude = ['full_name']

class UserForm(forms.ModelForm):
    authorization = forms.BooleanField(required=False, initial=True)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'user_type','is_admin' ,'is_analist', 'authorization']
        exclude = ['full_name', 'user_type']

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
    rfid_uid = forms.CharField(label="")
    authorization = forms.BooleanField(label="", required=False, initial=True)

    class Meta:
        model = Rfid
        fields = ["rfid_uid", "authorization"]