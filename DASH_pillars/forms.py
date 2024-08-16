from django import forms
from .models import Scholarship, Hardship, BasicNeedSupport

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name']

class HardshipForm(forms.ModelForm):
    class Meta:
        model = Hardship
        fields = ['name']

class BasicNeedSupportForm(forms.ModelForm):
    class Meta:
        model = BasicNeedSupport
        fields = ['name']
