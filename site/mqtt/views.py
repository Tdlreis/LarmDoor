from django.http import JsonResponse

from mqtt.mqtt import getLastRfid

# Create your views here.
def fetchrfid(request):
    return JsonResponse({'rfid': getLastRfid()})