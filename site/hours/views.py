from django.shortcuts import render, get_object_or_404, redirect
from userform.models import PunchCard, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import locale

def is_the_user(user, id):
    try:
        if user.is_admin == True:
            return True
        if user.user.pk != id:
            return False
        else:
            return True
    except User.DoesNotExist:
        return False
    return True
    
def format_hour(inTime):
    if inTime == 0:
        return "0s"
    
    time = timedelta(seconds=inTime)
    hourString = ""
    minuteString = ""
    secondString = ""

    if time.total_seconds() // 3600 > 0:
        hourString = str(int(time.total_seconds() / 3600)) + "h"
        time = time - timedelta(hours=int(time.total_seconds() / 3600))
    if time.total_seconds() // 60 > 0:
        minuteString = str(int(time.total_seconds() / 60)) + "m"
        time = time - timedelta(minutes=int(time.total_seconds() / 60))
    if time.total_seconds() > 0:
        secondString = str(int(time.total_seconds())) + "s"
    
    return hourString + " " + minuteString + " " + secondString
        
@login_required
def hours(request, id):
    if not is_the_user(request.user, id):
        return redirect('table')
    
    data = []
    try:
        punch_cards = PunchCard.objects.filter(user=id)    
        errors = 0
        for p in punch_cards:
            if p.punch_in_time == None or p.punch_out_time == None:
                errors = errors + 1
                punch_cards = punch_cards.exclude(pk=p.pk)

        start_date = punch_cards.earliest('punch_in_time').punch_in_time.date()
        end_date = punch_cards.latest('punch_in_time').punch_in_time.date()

        current_date = start_date

        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)
            time = PunchCard.objects.filter(user=id, punch_in_time__range=[current_date, next_date], punch_out_time__isnull=False, punch_in_time__isnull=False)
            hourVal = 0
            hoursNotVal = 0
            for t in time:
                if t.reviw == True:
                    hourVal = hourVal + (t.punch_out_time - t.punch_in_time).total_seconds()
                else:
                    hoursNotVal = hoursNotVal + (t.punch_out_time - t.punch_in_time).total_seconds()

            
            values = {
                'start': current_date,
                'end': (next_date - timedelta(days=1)),
                'hoursVal': format_hour(hourVal),
                'hoursNotVal': format_hour(hoursNotVal),
            }
            current_date = next_date
            if hourVal > 0 or hoursNotVal > 0:
                data.append(values)

        data.reverse()
        context = {
            'data': data,
            'user': id,
            'admin': request.user.is_admin,
            'errors': errors,
        }
    except PunchCard.DoesNotExist:
        context = {
            'data': data,
            'user': id,
            'admin': request.user.is_admin,
        }
        pass

    return render(request, 'hours.html', context)

@login_required
def get_data(request, cat, id):
    if not is_the_user(request.user, id):
        return redirect('table')
    
    data = []

    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    if cat == 4:
        punch_cards = PunchCard.objects.filter(user=id)
        for p in punch_cards:
            if p.reviw == True:
                validado = "Sim",
            else:
                validado =  "Não",
            values = {
                'in': None,
                'out': None,
                'validated': validado,
                'hours': None,
            }

            if p.punch_in_time == None and p.punch_out_time == None:
                values['in'] = "Não registrado"
                values['out'] = "Não registrado"
                values['hours'] = "Erro"
            elif p.punch_in_time == None:
                values['in'] = p.punch_in_time = "Não registrado"
                values['out'] = p.punch_out_time.strftime('%H:%M do dia %d de %B de %Y')
                values['hours'] = "Erro"
            elif p.punch_out_time == None:
                values['in'] = p.punch_in_time.strftime('%H:%M do dia %d de %B de %Y')
                values['out'] = p.punch_out_time = "Não registrado"
                values['hours'] = "Erro"
            else:
                values['in'] = p.punch_in_time.strftime('%H:%M do dia %d de %B de %Y')
                values['out'] = p.punch_out_time.strftime('%H:%M do dia %d de %B de %Y')
                values['hours'] = format_hour((p.punch_out_time - p.punch_in_time).total_seconds())
            
            data.append(values)
        data.reverse()
    else:
        punch_cards = PunchCard.objects.filter(user=id, punch_out_time__isnull=False, punch_in_time__isnull=False)
        start_date = punch_cards.earliest('punch_in_time').punch_in_time.date()
        end_date = punch_cards.latest('punch_in_time').punch_in_time.date()
        
        current_date = start_date
        while current_date <= end_date:
            if cat == 0:
                next_date = current_date + timedelta(days=30)
            elif cat == 1:
                next_date = current_date + timedelta(days=1)
            elif cat == 2:
                next_date = current_date + timedelta(days=365)
            elif cat == 3:
                next_date = current_date + timedelta(days=7)
            time = PunchCard.objects.filter(user=id, punch_in_time__range=[current_date, next_date], punch_out_time__isnull=False, punch_in_time__isnull=False)
            hourVal = 0
            hoursNotVal = 0
            for t in time:
                if t.reviw == True:
                    hourVal = hourVal + (t.punch_out_time - t.punch_in_time).total_seconds()
                else:
                    hoursNotVal = hoursNotVal + (t.punch_out_time - t.punch_in_time).total_seconds()

            values = {
                'start': current_date.strftime('%d de %B de %Y').replace(current_date.strftime('%d de %B de %Y').split()[2], current_date.strftime('%d de %B de %Y').split()[2].capitalize()),
                'end': (next_date - timedelta(days=1)).strftime('%d de %B de %Y').replace(next_date.strftime('%d de %B de %Y').split()[2], next_date.strftime('%d de %B de %Y').split()[2].capitalize()),
                'hoursVal': format_hour(hourVal),
                'hoursNotVal': format_hour(hoursNotVal),
            }
            current_date = next_date
            if hourVal > 0 or hoursNotVal > 0:
                data.append(values)
        data.reverse()

    
    return JsonResponse({'data': data})