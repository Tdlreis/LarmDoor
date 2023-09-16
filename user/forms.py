from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from .models import User, Student, Rfid


class UserForm(forms.ModelForm):
    authorization = forms.BooleanField(required=False, initial=True)
    user_type = forms.ChoiceField(choices=[('','Selecione uma opção'), (1,'Aluno'), (2,"Externo"), (3, "Professor"), (4, "Administrador")])
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'authorization', 'user_type', 'password']

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