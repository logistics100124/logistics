from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Driver, Organization, Automobile, Coming, ViewComing, Category, Catalog, ViewCatalog, Outgo, ViewOutgo, Sale, ViewSale
# Подключение форм
from .forms import DriverForm, OrganizationForm, AutomobileForm, ComingForm, CategoryForm, CatalogForm, OutgoForm, SaleForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        return render(request, "index.html")            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Отчеты
@login_required
#@group_required("Managers")
def report_index(request):
    try:
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            finish_date = request.POST.get("finish_date")
            # Приходные накладные
            coming = ViewComing.objects.filter(datec__range=[start_date, finish_date]).order_by('datec')
            # Расходные накладные
            outgo = ViewOutgo.objects.filter(dateo__range=[start_date, finish_date]).order_by('dateo')
        else:
            start_date = (datetime.now()-timedelta(days=365)).strftime('%Y-%m-%d')
            finish_date = datetime.now().strftime('%Y-%m-%d')
            # Приходные накладные
            coming = ViewComing.objects.all().order_by('datec')
            # Расходные накладные
            outgo = ViewOutgo.objects.all().order_by('dateo')
        # Товар по приходным накладным
        catalog = ViewCatalog.objects.order_by('category').order_by('title')
        # Проданый товар
        sale = ViewSale.objects.order_by('dateo')
        # Каталог доступных товаров
        catalog_available = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        return render(request, "report/index.html", {"coming": coming, "catalog": catalog, "outgo": outgo, "sale": sale, "catalog_available": catalog_available, "start_date": start_date, "finish_date": finish_date})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Экспорт в Excel
def export_excel(request): 
    try:
        # Приходные накладные
        #coming = ViewComing.objects.filter(datec__range=[start_date, finish_date]).order_by('datec')
        coming = ViewComing.objects.all().order_by('-datec')
        #coming = ViewComing.objects.all().order_by('-datec')
        # Расходные накладные
        #outgo = ViewOutgo.objects.filter(dateo__range=[start_date, finish_date]).order_by('dateo')
        outgo = ViewOutgo.objects.all().order_by('dateo')
        # Товар по приходным накладным
        catalog = ViewCatalog.objects.order_by('category').order_by('title')
        # Проданый товар
        sale = ViewSale.objects.order_by('dateo')
        # Каталог доступных товаров
        catalog_available = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
       
       # Create a HttpResponse object and set its content_type header value to Microsoft excel.
        response = HttpResponse(content_type='application/vnd.ms-excel') 
        # Set HTTP response Content-Disposition header value. Tell web server client the attached file name is students.xls.
        response['Content-Disposition'] = 'attachment;filename=report.xls' 
        # Create a new Workbook file.
        work_book = xlwt.Workbook(encoding = 'utf-8') 

        # Maintain some worksheet styles，style_head_row, style_data_row, style_green, style_red
        # This style will be applied to worksheet head row.
        style_head_row = xlwt.easyxf("""    
            align:
              wrap off,
              vert center,
              horiz center;
            borders:
              left THIN,
              right THIN,
              top THIN,
              bottom THIN;
            font:
              name Arial,
              colour_index white,
              bold on,
              height 0xA0;
            pattern:
              pattern solid,
              fore-colour 0x19;
            """
        )
        # Define worksheet data row style. 
        style_data_row = xlwt.easyxf("""
            align:
              wrap on,
              vert center,
              horiz left;
            font:
              name Arial,
              bold off,
              height 0XA0;
            borders:
              left THIN,
              right THIN,
              top THIN,
              bottom THIN;
            """
        )
        # Set data row date string format.
        #style_data_row.num_format_str = 'dd/mm/yyyy'
        # Define a green color style.
        style_green = xlwt.easyxf(" pattern: fore-colour 0x11, pattern solid;")
        # Define a red color style.
        style_red = xlwt.easyxf(" pattern: fore-colour 0x0A, pattern solid;")

        # Create a new worksheet in the above workbook.
        work_sheet = work_book.add_sheet(u'coming')
        # Generate worksheet head row data.
        work_sheet.write(0,0, 'datec', style_head_row) 
        work_sheet.write(0,1, 'numb', style_head_row) 
        work_sheet.write(0,2, 'organization', style_head_row) 
        work_sheet.col(2).width = 8000
        work_sheet.write(0,3, 'automobile', style_head_row) 
        work_sheet.col(3).width = 8000
        work_sheet.write(0,4, 'catalogs', style_head_row) 
        work_sheet.col(4).width = 30000
        # Generate worksheet data row data.
        row = 1 
        for com in coming:
            work_sheet.write(row,0, com.datec.strftime('%d.%m.%Y'), style_data_row)
            work_sheet.write(row,1, com.numb, style_data_row)
            work_sheet.write(row,2, com.organization, style_data_row)
            work_sheet.write(row,3, com.replica, style_data_row)
            result=str(com.total) + " ₽" 
            for cat in catalog:
                if (cat.coming_id==com.id):
                    result=result + "\n" + cat.title + ": " + str(cat.price) + " ₽, " + str(cat.quantity) + " " + cat.unit
            work_sheet.write(row,4, result, style_data_row)
            row=row + 1 
        # Create a StringIO object.
        output = BytesIO()
    
        # Create a new worksheet in the above workbook.
        work_sheet = work_book.add_sheet(u'outgo')
        # Generate worksheet head row data.
        work_sheet.write(0,0, 'dateo', style_head_row) 
        work_sheet.write(0,1, 'numb', style_head_row) 
        work_sheet.write(0,2, 'organization', style_head_row) 
        work_sheet.col(2).width = 8000
        work_sheet.write(0,3, 'automobile', style_head_row) 
        work_sheet.col(3).width = 8000
        work_sheet.write(0,4, 'catalogs', style_head_row) 
        work_sheet.col(4).width = 30000
        # Generate worksheet data row data.
        row = 1 
        for com in outgo:
            work_sheet.write(row,0, com.dateo.strftime('%d.%m.%Y'), style_data_row)
            work_sheet.write(row,1, com.numb, style_data_row)
            work_sheet.write(row,2, com.organization, style_data_row)
            work_sheet.write(row,3, com.replica, style_data_row)
            result=str(com.total) + " ₽" 
            for sal in sale:
                if (sal.outgo_id==com.id):
                    result=result + "\n" + sal.title + ": " + str(sal.price) + " ₽, " + str(sal.quantity) + " " + sal.unit
            work_sheet.write(row,4, result, style_data_row)
            row=row + 1 
        # Create a StringIO object.
        output = BytesIO()
           
        # Create a new worksheet in the above workbook.
        work_sheet = work_book.add_sheet(u'available')
        # Generate worksheet head row data.
        work_sheet.write(0,0, 'category', style_head_row) 
        work_sheet.col(0).width = 10000
        work_sheet.write(0,1, 'title', style_head_row) 
        work_sheet.col(1).width = 15000
        work_sheet.write(0,2, 'price', style_head_row) 
        work_sheet.col(2).width = 3000
        work_sheet.write(0,3, 'available', style_head_row) 
        work_sheet.write(0,4, 'total', style_head_row) 
        work_sheet.col(4).width = 4000
        work_sheet.write(0,5, 'storage', style_head_row) 
        work_sheet.col(5).width = 6000
        # Generate worksheet data row data.
        row = 1 
        for ava in catalog_available:
            work_sheet.write(row,0, ava.category, style_data_row)
            work_sheet.write(row,1, ava.title, style_data_row)
            work_sheet.write(row,2, str(ava.price) + " ₽", style_data_row)
            work_sheet.write(row,3, ava.available , style_data_row)
            work_sheet.write(row,4, str(ava.total) + " ₽", style_data_row)
            work_sheet.write(row,5, ava.storage, style_data_row)
            row=row + 1 
        # Create a StringIO object.
        output = BytesIO()

        # Save the workbook data to the above StringIO object.
        work_book.save(output)
        # Reposition to the beginning of the StringIO object.
        output.seek(0)
        # Write the StringIO object's value to HTTP response to send the excel file to the web server client.
        response.write(output.getvalue()) 
        return response
    except Exception as exception:
        print(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def organization_index(request):
    try:
        organization = Organization.objects.all().order_by('name')
        return render(request, "organization/index.html", {"organization": organization,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def organization_create(request):
    try:
        if request.method == "POST":
            organization = Organization()
            organization.name = request.POST.get("name")
            organization.address = request.POST.get("address")
            organization.phone = request.POST.get("phone")
            organization.email = request.POST.get("email")
            organization.leader = request.POST.get("leader")
            organizationform = OrganizationForm(request.POST)
            if organizationform.is_valid():
                organization.save()
                return HttpResponseRedirect(reverse('organization_index'))
            else:
                return render(request, "organization/create.html", {"form": organizationform})
        else:        
            organizationform = OrganizationForm()
            return render(request, "organization/create.html", {"form": organizationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def organization_edit(request, id):
    try:
        organization = Organization.objects.get(id=id)
        if request.method == "POST":
            organization.name = request.POST.get("name")
            organization.address = request.POST.get("address")
            organization.phone = request.POST.get("phone")
            organization.email = request.POST.get("email")
            organization.leader = request.POST.get("leader")
            organizationform = OrganizationForm(request.POST)
            if organizationform.is_valid():
                organization.save()
                return HttpResponseRedirect(reverse('organization_index'))
            else:
                return render(request, "organization/edit.html", {"form": organizationform})
        else:
            # Загрузка начальных данных
            organizationform = OrganizationForm(initial={'name': organization.name, 'address': organization.address, 'phone': organization.phone, 'email': organization.email, 'leader': organization.leader, })
            return render(request, "organization/edit.html", {"form": organizationform})
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def organization_delete(request, id):
    try:
        organization = Organization.objects.get(id=id)
        organization.delete()
        return HttpResponseRedirect(reverse('organization_index'))
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def organization_read(request, id):
    try:
        organization = Organization.objects.get(id=id) 
        return render(request, "organization/read.html", {"organization": organization})
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def driver_index(request):
    try:
        driver = Driver.objects.all().order_by('full_name')
        return render(request, "driver/index.html", {"driver": driver,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def driver_create(request):
    try:
        if request.method == "POST":
            driver = Driver()
            driver.full_name = request.POST.get("full_name")
            driver.birthday = request.POST.get("birthday")
            driver.phone = request.POST.get("phone")
            driver.category = request.POST.get("category")
            driverform = DriverForm(request.POST)
            if driverform.is_valid():
                driver.save()
                return HttpResponseRedirect(reverse('driver_index'))
            else:
                return render(request, "driver/create.html", {"form": driverform})
        else:        
            driverform = DriverForm(initial={ 'birthday': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "driver/create.html", {"form": driverform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def driver_edit(request, id):
    try:
        driver = Driver.objects.get(id=id)
        if request.method == "POST":
            driver.full_name = request.POST.get("full_name")
            driver.birthday = request.POST.get("birthday")
            driver.phone = request.POST.get("phone")
            driver.category = request.POST.get("category")
            driverform = DriverForm(request.POST)
            if driverform.is_valid():
                driver.save()
                return HttpResponseRedirect(reverse('driver_index'))
            else:
                return render(request, "driver/edit.html", {"form": driverform})
        else:
            # Загрузка начальных данных
            driverform = DriverForm(initial={'full_name': driver.full_name, 'birthday': driver.birthday.strftime('%Y-%m-%d'), 'phone': driver.phone, 'category': driver.category, })
            return render(request, "driver/edit.html", {"form": driverform})
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def driver_delete(request, id):
    try:
        driver = Driver.objects.get(id=id)
        driver.delete()
        return HttpResponseRedirect(reverse('driver_index'))
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def driver_read(request, id):
    try:
        driver = Driver.objects.get(id=id) 
        return render(request, "driver/read.html", {"driver": driver})
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request, coming_id):
    #catalog = Catalog.objects.all().order_by('title')
    coming = ViewComing.objects.get(id=coming_id)
    catalog = ViewCatalog.objects.filter(coming_id=coming_id).order_by('title')
    return render(request, "catalog/index.html", {"catalog": catalog, "coming": coming, "coming_id": coming_id})
    
# Список для просмотра и отправки в корзину
#@login_required
#@group_required("Managers")
#@login_required
def catalog_list(request):
    try:
        # Каталог доступных товаров
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        # Категории и подкатегория товара (для поиска)
        category = Category.objects.all().order_by('title')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по категории товара
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    catalog = catalog.filter(category=selected_item_category).all()
                # Поиск по названию товара
                catalog_search = request.POST.get("catalog_search")
                #print(catalog_search)                
                if catalog_search != '':
                    catalog = catalog.filter(title__contains = catalog_search).all()
                # Сортировка
                sort = request.POST.get('radio_sort')
                #print(sort)
                direction = request.POST.get('checkbox_sort_desc')
                #print(direction)
                if sort=='title':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-title')
                    else:
                        catalog = catalog.order_by('title')
                elif sort=='price':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-price')
                    else:
                        catalog = catalog.order_by('price')
                elif sort=='category':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-category')
                    else:
                        catalog = catalog.order_by('category')
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "selected_item_category": selected_item_category, "catalog_search": catalog_search, "sort": sort, "direction": direction,})    
            else:          
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category,})    
        else:
            return render(request, "catalog/list.html", {"catalog": catalog, "category": category, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request, coming_id):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.coming_id = coming_id
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform, "coming_id": coming_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def catalog_edit(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price, 'quantity': catalog.quantity, 'unit': catalog.unit, })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = ViewCatalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None)
        return render(request, "catalog/details.html", {"catalog": catalog,})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def automobile_index(request):
    try:
        automobile = Automobile.objects.all().order_by('reg_number')
        return render(request, "automobile/index.html", {"automobile": automobile,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def automobile_create(request):
    try:
        if request.method == "POST":
            automobile = Automobile()
            automobile.replica =  request.POST.get("replica")
            automobile.reg_number = request.POST.get("reg_number")
            automobile.driver = Driver.objects.filter(id=request.POST.get("driver")).first()
            automobileform = AutomobileForm(request.POST)
            if automobileform.is_valid():
                automobile.save()
                return HttpResponseRedirect(reverse('automobile_index'))
            else:
                return render(request, "automobile/create.html", {"form": automobileform})
        else:        
            automobileform = AutomobileForm()
            return render(request, "automobile/create.html", {"form": automobileform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def automobile_edit(request, id):
    try:
        automobile = Automobile.objects.get(id=id)
        if request.method == "POST":
            automobile.replica =  request.POST.get("replica")
            automobile.reg_number = request.POST.get("reg_number")
            automobile.driver = Driver.objects.filter(id=request.POST.get("driver")).first()
            automobileform = AutomobileForm(request.POST)
            if automobileform.is_valid():
                automobile.save()
                return HttpResponseRedirect(reverse('automobile_index'))
            else:
                return render(request, "automobile/edit.html", {"form": automobileform})
        else:
            # Загрузка начальных данных
            automobileform = AutomobileForm(initial={'replica': automobile.replica, 'reg_number': automobile.reg_number, 'driver': automobile.driver, })
            return render(request, "automobile/edit.html", {"form": automobileform})
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def automobile_delete(request, id):
    try:
        automobile = Automobile.objects.get(id=id)
        automobile.delete()
        return HttpResponseRedirect(reverse('automobile_index'))
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def automobile_read(request, id):
    try:
        automobile = Automobile.objects.get(id=id) 
        return render(request, "automobile/read.html", {"automobile": automobile})
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
@login_required
@group_required("Managers")
def coming_index(request):
    coming = ViewComing.objects.all().order_by('-datec')
    return render(request, "coming/index.html", {"coming": coming,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def coming_create(request):
    try:
        if request.method == "POST":
            coming = Coming()
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb")
            coming.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
            coming.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/create.html", {"form": comingform})
        else:        
            comingform = ComingForm(initial={'datec': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "coming/create.html", {"form": comingform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def coming_edit(request, id):
    try:
        coming = Coming.objects.get(id=id)
        if request.method == "POST":
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb") 
            coming.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
            coming.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/edit.html", {"form": comingform})
        else:
            # Загрузка начальных данных
            comingform = ComingForm(initial={'datec': coming.datec.strftime('%Y-%m-%d'), 'numb': coming.numb, 'organization': coming.organization, 'automobile': coming.automobile, })
            return render(request, "coming/edit.html", {"form": comingform})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def coming_delete(request, id):
    try:
        coming = Coming.objects.get(id=id)
        coming.delete()
        return HttpResponseRedirect(reverse('coming_index'))
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def coming_read(request, id):
    try:
        coming = ViewComing.objects.get(id=id) 
        return render(request, "coming/read.html", {"coming": coming})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request, coming_id):
    #catalog = Catalog.objects.all().order_by('title')
    coming = ViewComing.objects.get(id=coming_id)
    catalog = ViewCatalog.objects.filter(coming_id=coming_id).order_by('title')
    return render(request, "catalog/index.html", {"catalog": catalog, "coming": coming, "coming_id": coming_id})
    
# Список для просмотра и отправки в корзину
#@login_required
#@group_required("Managers")
#@login_required
def catalog_list(request):
    try:
        # Каталог доступных товаров
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        # Категории и подкатегория товара (для поиска)
        category = Category.objects.all().order_by('title')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по категории товара
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    catalog = catalog.filter(category=selected_item_category).all()
                # Поиск по названию товара
                catalog_search = request.POST.get("catalog_search")
                #print(catalog_search)                
                if catalog_search != '':
                    catalog = catalog.filter(title__contains = catalog_search).all()
                # Сортировка
                sort = request.POST.get('radio_sort')
                #print(sort)
                direction = request.POST.get('checkbox_sort_desc')
                #print(direction)
                if sort=='title':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-title')
                    else:
                        catalog = catalog.order_by('title')
                elif sort=='price':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-price')
                    else:
                        catalog = catalog.order_by('price')
                elif sort=='category':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-category')
                    else:
                        catalog = catalog.order_by('category')
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "selected_item_category": selected_item_category, "catalog_search": catalog_search, "sort": sort, "direction": direction,})    
            else:          
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category,})    
        else:
            return render(request, "catalog/list.html", {"catalog": catalog, "category": category, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request, coming_id):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.coming_id = coming_id
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalog.storage = request.POST.get("storage")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform, "coming_id": coming_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def catalog_edit(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalog.storage = request.POST.get("storage")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price, 'quantity': catalog.quantity, 'unit': catalog.unit, 'storage': catalog.storage, })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = ViewCatalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None)
        return render(request, "catalog/details.html", {"catalog": catalog,})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

###################################################################################################

@login_required
@group_required("Managers")
def outgo_index(request):
    outgo = ViewOutgo.objects.all().order_by('-dateo')
    return render(request, "outgo/index.html", {"outgo": outgo,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def outgo_create(request):
    try:
        if request.method == "POST":
            outgo = Outgo()
            outgo.consumer = request.POST.get("consumer")
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")
            outgo.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
            outgo.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/create.html", {"form": outgoform})
        else:        
            outgoform = OutgoForm(initial={'dateo': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "outgo/create.html", {"form": outgoform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def outgo_edit(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        if request.method == "POST":
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")  
            outgo.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
            outgo.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/edit.html", {"form": outgoform})
        else:
            # Загрузка начальных данных
            outgoform = OutgoForm(initial={'dateo': outgo.dateo.strftime('%Y-%m-%d'), 'numb': outgo.numb, 'organization': outgo.organization, 'automobile': outgo.automobile,  })
            return render(request, "outgo/edit.html", {"form": outgoform})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def outgo_delete(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        outgo.delete()
        return HttpResponseRedirect(reverse('outgo_index'))
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def outgo_read(request, id):
    try:
        outgo = ViewOutgo.objects.get(id=id) 
        return render(request, "outgo/read.html", {"outgo": outgo})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def sale_index(request, outgo_id):
    #sale = Sale.objects.all()
    outgo = ViewOutgo.objects.get(id=outgo_id)
    sale = ViewSale.objects.filter(outgo_id=outgo_id)
    return render(request, "sale/index.html", {"sale": sale, "outgo": outgo, "outgo_id": outgo_id})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def sale_create(request, outgo_id):
    try:
        # Каталог доступных товаров
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        if request.method == "POST":
            # Перебрать весь каталог смотреть отмеченные товары
            for cat in catalog:
                if request.POST.get("quantity" + str(cat.id)):
                    sale = Sale()
                    sale.outgo_id = outgo_id
                    sale.catalog_id = cat.id
                    sale.quantity = request.POST.get("quantity" + str(cat.id))
                    sale.save()
                    #print(f"{cat.id}.{cat.title} - {cat.available}")
            return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
        else:        
            saleform = SaleForm()
            return render(request, "sale/create.html", {"form": saleform, "outgo_id": outgo_id, "catalog": catalog})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    #try:
    #    # Каталог доступных товаров
    #    catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
    #    if request.method == "POST":
    #        sale = Sale()
    #        sale.outgo_id = outgo_id
    #        sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
    #        #sale.catalog = ViewCatalog.objects.filter(id=request.POST.get("catalog")).first()
    #        sale.quantity = request.POST.get("quantity")
    #        saleform = SaleForm(request.POST)
    #        if saleform.is_valid():
    #            #sale.save()
    #            return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
    #        else:
    #            return render(request, "sale/create.html", {"form": saleform})
    #    else:        
    #        saleform = SaleForm()
    #        return render(request, "sale/create.html", {"form": saleform, "outgo_id": outgo_id, "catalog": catalog})
    #except Exception as exception:
    #    print(exception)
    #    return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def sale_edit(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        if request.method == "POST":
            sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.quantity = request.POST.get("quantity")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
            else:
                return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})            
        else:
            # Загрузка начальных данных
            saleform = SaleForm(initial={'catalog': sale.catalog, 'quantity': sale.quantity, })
            #print('->',sale.photo )
            return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def sale_delete(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def sale_read(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        return render(request, "sale/read.html", {"sale": sale, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################    

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user