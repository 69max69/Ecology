from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User

        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class StaffForm(forms.ModelForm):
        class Meta:
            model = Staff
            fields = ('branch', 'department', 'function')
            widjets = {
                'department': forms.TextInput(attrs={'class': 'form-control'}),
                'function': forms.TextInput(attrs={'class': 'form-control'}),
                'branch': forms.Select(attrs={'class': 'form-control'}),
             }

class DateInput(forms.DateInput):
    input_type = 'date'


class AddEducatedWaste(forms.ModelForm):
    class Meta:
        model = EducatedWaste
        fields = ['name', 'object_name', 'quantity',  'date_of_educated']
        widgets = {
            'date_of_educated': DateInput(),
        }

class AddEducatedWaste1(AddEducatedWaste):
    class Meta:
        model = EducatedWaste
        fields = ['name', 'object_name', 'quantity',  'date_of_educated']
        widgets = {
            'date_of_educated': DateInput(),
        }
    def __init__(self, my_arg1, *args, **kwargs):
        super(AddEducatedWaste, self).__init__(*args, **kwargs)
        self.fields['object_name'].queryset = NameOfObjects.objects.filter(branch=my_arg1)


class AddReclaimedWaste(forms.ModelForm):
    class Meta:
        model = ReclaimedWaste
        fields = ['name', 'object_name', 'quantity',  'date_of_reclaimed']
        widgets = {
            'date_of_reclaimed': DateInput(),
        }

class AddReclaimedWaste1(AddReclaimedWaste):
    class Meta:
        model = ReclaimedWaste
        fields = ['name', 'object_name', 'quantity',  'date_of_reclaimed']
        widgets = {
            'date_of_reclaimed': DateInput(),
        }
    def __init__(self, my_arg1, *args, **kwargs):
        super(AddReclaimedWaste, self).__init__(*args, **kwargs)
        self.fields['object_name'].queryset = NameOfObjects.objects.filter(branch=my_arg1)

class AddTransferredWaste(forms.ModelForm):
    class Meta:
        model = TransferredWaste
        fields = ['name', 'object_name', 'quantity',  'date_of_transferred', 'type_transferr', 'counterparty']
        widgets = {
            'date_of_transferred': DateInput(),
        }

class AddTransferredWaste1(AddTransferredWaste):
    class Meta:
        model = TransferredWaste
        fields = ['name', 'object_name', 'quantity', 'date_of_transferred', 'type_transferr', 'counterparty']
        widgets = {
            'date_of_transferred': DateInput(),
        }
    def __init__(self, my_arg1, *args, **kwargs):
        super(AddTransferredWaste, self).__init__(*args, **kwargs)
        self.fields['object_name'].queryset = NameOfObjects.objects.filter(branch=my_arg1)

class ChoseReportDate(forms.Form):
    CHOICES = [('month', 'за месяц'),
               ('quater', 'за квартал'),
               ('year', 'за год'),]

    type_report = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='Тип отчета')

class ReportMonth(forms.Form):
    CHOICES = [('1', 'январь'),
               ('2', 'февраль'),
               ('3', 'март'),
               ('4', 'апрель'),
               ('5', 'май'),
               ('6', 'июнь'),
               ('7', 'июль'),
               ('8', 'август'),
               ('9', 'сентябрь'),
               ('10', 'октябрь'),
               ('11', 'ноябрь'),
               ('12', 'декабрь')]

    month = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='Месяц')
    year = forms.IntegerField(widget=forms.TextInput(attrs={'data-mask':"0000"}), max_value=2030, min_value=2019, label='Год')


class ReportQuater(forms.Form):

    quater = forms.IntegerField(widget=forms.TextInput, max_value=4, min_value=1, label='Квартал')
    year = forms.IntegerField(widget=forms.TextInput(attrs={'data-mask':"0000"}), max_value=2030, min_value=2019, label='Год')

class ReportYear(forms.Form):


    year = forms.IntegerField(widget=forms.TextInput(attrs={'data-mask':"0000"}), max_value=2030, min_value=2019, label='Год')


