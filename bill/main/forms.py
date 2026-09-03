from django import forms
from .models import *

class Makebill(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['tenant','room']
        # exclude=['bill_status','date_created']
        widgets={
            'tenant': forms.CheckboxSelectMultiple
        }



        
class Addtenant(forms.ModelForm):
    class Meta:
        model  = Tenant
        fields = '__all__'
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'joined_date': forms.DateInput(attrs={'type': 'date'}),
            'leaving_date': forms.DateInput(attrs={'type': 'date'}),
        }
