from django.shortcuts import render
from userform.models import PunchCard
from hours.views import format_hour
from django.http import JsonResponse
from .forms import PunchCardForm
from django.contrib.auth.decorators import login_required, user_passes_test

# from userform.views import staff_chek

# Create your views here.
# @login_required
# @user_passes_test(staff_chek, login_url='index')
def reviewlist(request):
    data = []
    try:
        nonValidated = PunchCard.objects.filter(reviw=False).order_by('punch_in_time')
        for n in nonValidated:
            values = {
                'name': n.user.user.full_name,
                'in': None,
                'out': None,
                'hours': None,
                'id': n.pk,
                'form': PunchCardForm(instance=n)
            }
            if n.punch_in_time == None or n.punch_out_time == None:
                values['in'] = "Não registrado"
                values['out'] = "Não registrado"
                values['hours'] = "Erro"
            elif n.punch_in_time == None:
                values['in'] = "Não registrado"
                values['out'] = n.punch_out_time
                values['hours'] = "Erro"
            elif n.punch_out_time == None:
                values['in'] = n.punch_in_time
                values['out'] = "Não registrado"
                values['hours'] = "Erro"
            else:
                values['in'] = n.punch_in_time
                values['out'] = n.punch_out_time
                values['hours'] = format_hour((n.punch_out_time - n.punch_in_time).total_seconds())
            data.append(values)
        context = {
            'data': data,
        }
    except PunchCard.DoesNotExist:
        context = {
            'data': data
        }
        pass

    return render(request, 'review.html', context)

# @login_required
# @user_passes_test(staff_chek, login_url='index')
def review(request, id):
    if request.method == 'POST':
        punch_card = PunchCard.objects.get(id=id)
        punch_card.reviw = True
        punch_card.punch_in_time = request.POST['punch_in_time']
        punch_card.punch_out_time = request.POST['punch_out_time']
        punch_card.save()

    return JsonResponse({'success': True})

def delete(request, id):
    punch_card = PunchCard.objects.get(id=id)
    punch_card.delete()

    return JsonResponse({'success': True})