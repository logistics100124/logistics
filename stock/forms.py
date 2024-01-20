from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Organization, Driver, Automobile, Coming, Category, Catalog, ViewCatalog, Outgo, Sale
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Организация
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name','address','phone','email','leader',]
        widgets = {
            'name': TextInput(attrs={"size":"100"}),            
            'address': TextInput(attrs={"size":"80"}),
            'phone': TextInput(attrs={"size":"50", "type":"tel"}),            
            'email': TextInput(attrs={"size":"50", "type":"email"}), 
            'leader': TextInput(attrs={"size":"100"}),
        }
        labels = {
            'title': _('organization_title'),            
        }

# Водитель 
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['full_name', 'birthday', 'phone', 'category',]
        widgets = {
            'full_name': TextInput(attrs={"size":"100"}),
            'birthday': DateInput(attrs={"type":"date"}),
            'phone': TextInput(attrs={"size":"60", "type":"tel", "pattern": "+7-[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
            'category': TextInput(attrs={"size":"80"}),
        }
    # Метод-валидатор для поля birthday
    def clean_birthday(self):        
        if isinstance(self.cleaned_data['birthday'], datetime.date) == True:
            data = self.cleaned_data['birthday']
            # Проверка даты рождения не моложе 18 лет
            if data > timezone.now() - relativedelta(years=18):
                raise forms.ValidationError(_('Minimum age 18 years old'))
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Автомобиль 
class AutomobileForm(forms.ModelForm):
    class Meta:
        model = Automobile
        fields = ['replica', 'reg_number', 'driver',]
        widgets = {
            'replica': TextInput(attrs={"size":"100"}),  
            'reg_number': TextInput(attrs={"size":"50"}),            
            'driver': forms.Select(attrs={'class': 'chosen'}),           
        }
        labels = {
            'title': _('organization_title'),            
        }

# Приходные накладные  
class ComingForm(forms.ModelForm):
    class Meta:
        model = Coming
        fields = ('datec', 'numb', 'organization', 'automobile', )
        widgets = {
            'datec': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
            'organization': forms.Select(attrs={'class': 'chosen'}),  
            'automobile': forms.Select(attrs={'class': 'chosen'}),  
        }
        labels = {
            'organization': _('organization'),            
            'automobile': _('automobile'),            
        }
    # Метод-валидатор для поля datec
    def clean_datec(self):
        data = self.cleaned_data['datec']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

# Категория товара
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('category', 'title', 'details', 'price', 'quantity', 'unit', 'storage', 'photo')
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 5}),            
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'quantity': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'unit': TextInput(attrs={"size":"50"}),
            'storage': TextInput(attrs={"size":"75"}),
        }
        labels = {
            'category': _('category'),            
            'photo': _('catalog_photo'),            
        }
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data       

# Расходные накладные  
class OutgoForm(forms.ModelForm):
    class Meta:
        model = Outgo
        fields = ('dateo', 'numb', 'organization', 'automobile', )
        widgets = {
            'dateo': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
            'organization': forms.Select(attrs={'class': 'chosen'}),  
            'automobile': forms.Select(attrs={'class': 'chosen'}),  
            
        }
        labels = {
            'organization': _('organization'),            
            'automobile': _('automobile'),     
        }
    # Метод-валидатор для поля dateo
    def clean_dateo(self):
        data = self.cleaned_data['dateo']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('catalog', 'quantity')
        widgets = {
            'catalog': forms.Select(attrs={'class': 'chosen'}),
            'quantity': NumberInput(attrs={"size":"10"}),            
        }
        labels = {
            'catalog': _('catalog'),            
        }
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        available = ViewCatalog.objects.filter(available__gt=0).only('id').all()
        self.fields['catalog'].queryset = Catalog.objects.filter(id__in = available)
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data


# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
