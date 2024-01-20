from django.contrib import admin

from .models import Driver, Organization, Automobile, Coming, Category, Catalog, Outgo, Sale

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Driver)
admin.site.register(Organization)
admin.site.register(Automobile)
admin.site.register(Coming)
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Outgo)
admin.site.register(Sale)
