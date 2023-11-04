from django.shortcuts import render

from userform.models import User, UserDoor, Student

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