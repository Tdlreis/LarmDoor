from django import forms
from userform.models import PunchCard

class PunchCardForm(forms.ModelForm):
    punch_in_time = forms.DateTimeField(label="Punch In Time", widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))
    punch_out_time = forms.DateTimeField(label="Punch Out Time", widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))

    class Meta:
        model = PunchCard
        fields = ['punch_in_time', 'punch_out_time']