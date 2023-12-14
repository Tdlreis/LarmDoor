from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.db.models import Avg, Count
from statistics import mean
from .models import Entradas
from userform.models import PunchCard
from dateutil.relativedelta import relativedelta



# Create your views here.


def home(request):
    return render(request, 'home.html')


def medias(request, date_mode=2, start_date=None, end_date=None):
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else datetime.now() - timedelta(days=28)
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()

    x = Entradas.objects.filter(data__range=[start_date, end_date])

    interval = None

    if date_mode == 0:  # mes (months)
        # Calculate the difference in months
        interval = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    elif date_mode == 1:  # sem (weeks)
        interval = (end_date - start_date).days // 7
    else:  # dia (days)
        # Calculate the difference in days
        interval = (end_date - start_date).days

    labels = []
    data_temperatura = []
    data_humidade = []
    data_lux = []
    data_volts = []
    data_alunos = []

    for i in range(interval + 1):
        entries = None
        if date_mode == 0:  # mes (months)
            current_date = start_date + relativedelta(months=i)
            entries = Entradas.objects.filter(data__month=current_date.month, data__year=current_date.year)
        elif date_mode == 1:  # sem (weeks)
            current_date = start_date + timedelta(weeks=i)
            entries = Entradas.objects.filter(data__date__range=[current_date, current_date + timedelta(days=6)])
        else:  # dia (days)
            current_date = start_date + timedelta(days=i)
            entries = Entradas.objects.filter(data__date=current_date.date())

        temperatures = [entry.temperatura for entry in entries]
        humidities = [entry.humidade for entry in entries]
        lux_values = [entry.lux for entry in entries]
        volts_values = [entry.voltagem for entry in entries]
        students = [entry.alunos for entry in entries]

        total_temperature = sum(temperatures) if temperatures else 0
        total_humidade = sum(humidities) if humidities else 0
        total_lux = sum(lux_values) if lux_values else 0
        total_volts = sum(volts_values) if volts_values else 0
        total_students = sum(students) if students else 0

        num_entries = len(temperatures)

        average_temperature = round(total_temperature / num_entries, 2) if num_entries > 0 else 0
        average_humidade = round(total_humidade / num_entries, 2) if num_entries > 0 else 0
        average_lux = round(total_lux / num_entries, 2) if num_entries > 0 else 0
        average_volts = round(total_volts / num_entries, 2) if num_entries > 0 else 0
        average_students = round(total_students / num_entries, 2) if num_entries > 0 else 0

        labels.append(current_date.strftime('%Y-%m-%d'))
        data_temperatura.append(average_temperature)
        data_humidade.append(average_humidade)
        data_lux.append(average_lux)
        data_volts.append(average_volts)
        data_alunos.append(average_students)

    data_json = {
        'data_alunos': data_alunos,
        'data_temperatura': data_temperatura,
        'data_humidade': data_humidade,
        'data_lux': data_lux,
        'data_volts': data_volts,
        'labels': labels,

    }

    return JsonResponse(data_json)
