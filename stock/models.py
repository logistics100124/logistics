from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# ������ ���������� ���������� � ������, � �������� �� ���������.
# ��� �������� ���� � ��������� ����� ������.
# ������ ���� ������ ������������ ���� ������� � ���� ������.
# ������ ������ ��� ����� �������������� �� django.db.models.Model.
# ������� ������ ������������ ���� � ���� ������.
# Django ������������� ������������� ��������� API ��� ������� � ������

# choices (������ ������). �������� (��������, ������ ��� ������) 2-� ���������� ��������,
# ������������ �������� �������� ��� ����.
# ��� �����������, ������ ����� ���������� select ������ ������������ ���������� ����
# � ��������� �������� ���� ���������� ����������.

# ����������� ��� ���� (�����, label). ������ ����, ����� ForeignKey, ManyToManyField � OneToOneField,
# ������ ���������� ��������� �������������� ����������� ��������.
# ���� ��� �� �������, Django �������������� ������� ���, ��������� �������� ����, ������� ������������� �� ������.
# null - ���� True, Django �������� ������ �������� ��� NULL � ���� ������. �� ��������� - False.
# blank - ���� True, ���� �� ����������� � ����� ���� ������. �� ��������� - False.
# ��� �� �� �� ��� � null. null ��������� � ���� ������, blank - � �������� ������.
# ���� ���� �������� blank=True, ����� �������� �������� ������ ��������.
# ��� blank=False - ���� �����������.

# �����������
class Organization(models.Model):
    name = models.CharField(_('organization_name'), max_length=128)
    address = models.CharField(_('organization_address'), max_length=128)
    phone = models.CharField(_('organization_phone'), max_length=32)
    email = models.CharField(_('organization_email'), max_length=128)
    leader = models.CharField(_('organization_leader'), max_length=128)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'organization'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]
        # ���������� �� ���������
        ordering = ['name']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}, {}, {}".format(self.name, self.phone, self.email)

# �������� 
class Driver(models.Model):
    full_name = models.CharField(_('full_name'), max_length=128)
    birthday = models.DateTimeField(_('birthday'))
    phone = models.CharField(_('phone'), max_length=64)
    category = models.CharField(_('category'), max_length=128)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'driver'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['full_name']),
        ]
        # ���������� �� ���������
        ordering = ['full_name']
    def __str__(self):
        # ����� � ��� Select 
        return "{}".format(self.full_name)

# ����������
class  Automobile(models.Model):
    replica = models.CharField(_('replica'), max_length=128)
    reg_number = models.CharField(_('reg_number'), max_length=64, unique=True)
    driver = models.ForeignKey(Driver, related_name='automobile_driver', on_delete=models.CASCADE)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'automobile'
    def __str__(self):
        # ����� � ��� Select 
        return "{} {}".format(self.replica, self.reg_number)

# ��������� ��������� 
class Coming(models.Model):
    datec = models.DateTimeField(_('datec'))
    numb = models.IntegerField(_('numb'))     
    organization = models.ForeignKey(Organization, related_name='coming_organization', on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, related_name='coming_automobile', on_delete=models.CASCADE)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'coming'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datec']),            
        ]
        # ���������� �� ���������
        ordering = ['datec']
    def __str__(self):
        # ����� �������� � ��� SELECT 
        return "#{} {}".format(self.numb, self.datec)

# ������������� ��������� ��������� 
class ViewComing(models.Model):
    datec = models.DateTimeField(_('datec'))
    numb = models.IntegerField(_('numb'))     
    organization = models.CharField(_('organization'), max_length=256)
    replica = models.CharField(_('replica'), max_length=128)
    reg_number = models.CharField(_('reg_number'), max_length=64)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_coming'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datec']),
        ]
        # ���������� �� ���������
        ordering = ['datec']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "#{} {}".format(self.numb, self.datec)

# ��������� ������
class Category(models.Model):
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'category'
    def __str__(self):
        # ����� ��������� ��� SELECT 
        return "{}".format(self.title)

# ������� �������
class Catalog(models.Model):
    coming = models.ForeignKey(Coming, related_name='catalog_coming', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('catalog_price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    photo = models.ImageField(_('catalog_photo'), upload_to='images/', blank=True, null=True)    
    storage = models.CharField(_('storage'), max_length=96)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)

# ������������� ���� ������ ������� �������
class ViewCatalog(models.Model):
    coming_id = models.IntegerField(_('coming_id'))
    category_id = models.IntegerField(_('category_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    photo = models.ImageField(_('catalog_photo'), upload_to='images/', blank=True, null=True)  
    storage = models.CharField(_('storage'), max_length=96)      
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    sale_quantity = models.IntegerField(_('sale_quantity'))
    available = models.IntegerField(_('available'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)

# ��������� ��������� 
class Outgo(models.Model):
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    organization = models.ForeignKey(Organization, related_name='outgo_organization', on_delete=models.CASCADE)
    automobile = models.ForeignKey(Automobile, related_name='outgo_automobile', on_delete=models.CASCADE)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'outgo'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateo']),            
        ]
        # ���������� �� ���������
        ordering = ['dateo']
    def __str__(self):
        # ����� �������� � ��� SELECT 
        return "#{} {}".format(self.numb, self.dateo)
        # Override the save method of the model

 # ������������� ��������� ��������� 
class ViewOutgo(models.Model):
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    organization = models.CharField(_('organization'), max_length=256)
    replica = models.CharField(_('replica'), max_length=128)
    reg_number = models.CharField(_('reg_number'), max_length=64)
    total = models.IntegerField(_('total')) 
    #total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_outgo'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateo']),
        ]
        # ���������� �� ���������
        ordering = ['dateo']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "#{} {}".format(self.numb, self.dateo)

# ������� 
class Sale(models.Model):
    outgo = models.ForeignKey(Outgo, related_name='sale_outgo', on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, related_name='sale_catalog', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'sale'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['outgo']),
            models.Index(fields=['catalog']),
        ]
        # ���������� �� ���������
        ordering = ['outgo']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}".format(self.catalog, self.quantity)
        # ������� �� ���� �� ��������� �� �������
        #managed = False

# ������������� ������� 
class ViewSale(models.Model):
    outgo_id = models.IntegerField(_('outgo_id'))
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    organization = models.CharField(_('organization'), max_length=256)
    replica = models.CharField(_('replica'), max_length=128)
    reg_number = models.CharField(_('reg_number'), max_length=64)
    catalog_id = models.IntegerField(_('catalog_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    photo = models.ImageField(_('catalog_photo'), upload_to='images/', blank=True, null=True)    
    storage = models.CharField(_('storage'), max_length=96)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_sale'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['outgo_id']),
            models.Index(fields=['catalog_id']),
        ]
        # ���������� �� ���������
        ordering = ['outgo_id']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}".format(self.catalog_id, self.quantity)
        # ������� �� ���� �� ��������� �� �������
        #managed = False
