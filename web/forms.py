from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from api.models import Calculation
from django.core.validators import EmailValidator

class RegistrForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='This field is required',validators=[EmailValidator])
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CalculationCreateForm(ModelForm):
    broker_forwarding_price = forms.IntegerField(initial=850, help_text='Broker price')
    certification_price = forms.IntegerField(initial=250, help_text='Certification price in Ukraine')
    company_services_price = forms.IntegerField(initial=400, help_text='Profit company')
    # auction = forms.CharField(initial="IAAI")

    class Meta:
        model = Calculation
        fields = '__all__'
        read_only_fields = ['id', 'create_date',]
        exclude = ['owner',
        'commission_price',
        'swift_price',
        'registration_price',
        'delivery_land_price',
        'delivery_all_price',
        'customs_clearance_price',
        'end_price',
        ]

class CalculationForm(ModelForm):

    class Meta:
        model = Calculation
        fields = '__all__'
        read_only_fields = ['id', 'create_date',]
        exclude = ['owner',]


class CalculationDeleteForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = []



