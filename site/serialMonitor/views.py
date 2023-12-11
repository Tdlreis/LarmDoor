from django.http import JsonResponse

from .serial import getLastRfid
from django.contrib.auth.decorators import login_required, user_passes_test

from userform.views import admin_chek

# Create your views here.
@login_required
@user_passes_test(admin_chek, login_url='table')
def fetchrfid(request):
    return JsonResponse({'rfid': getLastRfid()})