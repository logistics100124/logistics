"""
URL configuration for logistics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from stock import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    #path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('organization/index/', views.organization_index, name='organization_index'),
    path('organization/create/', views.organization_create, name='organization_create'),
    path('organization/edit/<int:id>/', views.organization_edit, name='organization_edit'),
    path('organization/delete/<int:id>/', views.organization_delete, name='organization_delete'),
    path('organization/read/<int:id>/', views.organization_read, name='organization_read'),
    
    path('driver/index/', views.driver_index, name='driver_index'),
    path('driver/create/', views.driver_create, name='driver_create'),
    path('driver/edit/<int:id>/', views.driver_edit, name='driver_edit'),
    path('driver/delete/<int:id>/', views.driver_delete, name='driver_delete'),
    path('driver/read/<int:id>/', views.driver_read, name='driver_read'),
 
    path('automobile/index/', views.automobile_index, name='automobile_index'),
    path('automobile/create/', views.automobile_create, name='automobile_create'),
    path('automobile/edit/<int:id>/', views.automobile_edit, name='automobile_edit'),
    path('automobile/delete/<int:id>/', views.automobile_delete, name='automobile_delete'),
    path('automobile/read/<int:id>/', views.automobile_read, name='automobile_read'),

    path('coming/index/', views.coming_index, name='coming_index'),
    path('coming/create/', views.coming_create, name='coming_create'),
    path('coming/edit/<int:id>/', views.coming_edit, name='coming_edit'),
    path('coming/delete/<int:id>/', views.coming_delete, name='coming_delete'),
    path('coming/read/<int:id>/', views.coming_read, name='coming_read'),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),

    path('catalog/index/<int:coming_id>/', views.catalog_index, name='catalog_index'),
    path('catalog/list/', views.catalog_list, name='catalog_list'),
    path('catalog/create/<int:coming_id>/', views.catalog_create, name='catalog_create'),
    path('catalog/edit/<int:id>/<int:coming_id>/', views.catalog_edit, name='catalog_edit'),
    path('catalog/delete/<int:id>/<int:coming_id>/', views.catalog_delete, name='catalog_delete'),
    path('catalog/read/<int:id>/<int:coming_id>/', views.catalog_read, name='catalog_read'),
    path('catalog/details/<int:id>/', views.catalog_details, name='catalog_details'),    

    path('outgo/index/', views.outgo_index, name='outgo_index'),
    path('outgo/create/', views.outgo_create, name='outgo_create'),
    path('outgo/edit/<int:id>/', views.outgo_edit, name='outgo_edit'),
    path('outgo/delete/<int:id>/', views.outgo_delete, name='outgo_delete'),
    path('outgo/read/<int:id>/', views.outgo_read, name='outgo_read'),

    path('sale/index/<int:outgo_id>/', views.sale_index, name='sale_index'),
    path('sale/create/<int:outgo_id>/', views.sale_create, name='sale_create'),
    path('sale/edit/<int:id>/<int:outgo_id>/', views.sale_edit, name='sale_edit'),
    path('sale/delete/<int:id>/<int:outgo_id>/', views.sale_delete, name='sale_delete'),
    path('sale/read/<int:id>/<int:outgo_id>/', views.sale_read, name='sale_read'),

    path('report/index/', views.report_index, name='report_index'),
    path('export/excel/', views.export_excel, name='export_excel'),     

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


