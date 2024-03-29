﻿# Generated by Django 4.2.2 on 2024-01-15 03:41
from pickle import FALSE, TRUE
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.db import migrations
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
# Подключаем модкль генерации случайных чисел
import random


global dict_category
dict_category = {}
global dict_catalog_price
dict_catalog_price = {}

# Получение случайного адреса (k - включает ли адрес квартиру)
def get_adres(k):
    ulica = ["ул. Баженова", 
            "ул. Вавилова", 
            "ул. Гастелло", 
            "ул. Гончарная", 
            "ул. Грибоедова", 
            "ул. Дружбы", 
            "ул. Ермекова",
            "ул. Жамбыла", 
            "ул. Защитная", 
            "ул. Ипподромная", 
            "ул. Караванная", 
            "ул. Кирпичная", 
            "ул. Луначарского", 
            "ул. Маяковского", 
            "ул. Некрасова", 
            "ул. Новоселов",
            "ул. Олимпийская", 
            "ул. Победы", 
            "ул. Садовая", 
            "ул. Стремянная", 
            "ул. Университетская", 
            "ул. Фрунзе",
            "ул. Чайковского" 
        ]
    if (k==True):
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) + "-" + str(random.randint(1, 200)) 
    else:
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) 
    return adres

# Получение случайного телефона
def get_telefon():
    if random.randint(0, 1) == 1:
        telefon = "+7-911-"
    else:
        telefon = "+7-904-" 
    telefon = telefon + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + "-" + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) 
    return telefon

# Добавить Организацию 
def insert_organization(apps, param):
    Organization = apps.get_model("stock", "Organization")
    organization = Organization()
    organization.name = param[0]
    organization.address = param[1]
    organization.phone = param[2]
    organization.email = param[3]
    organization.leader = param[4]
    organization.save()
    return 

# Добавить водителя 
def insert_driver(apps, param_driver):   
    Driver = apps.get_model("stock", "Driver")
    driver = Driver()
    driver.full_name = param_driver[0]
    driver.birthday = param_driver[1]
    driver.phone = param_driver[2]
    driver.category = param_driver[3]
    driver.save()
    return

# Добавить автомобиль
def insert_automobile(apps, param_automobile):   
    Automobile = apps.get_model("stock", "Automobile")
    automobile = Automobile()
    automobile.replica = param_automobile[0]
    automobile.reg_number = param_automobile[1]
    automobile.driver_id = param_automobile[2]
    automobile.save()
    return

# Добавить Приходные накладные 
def insert_coming(apps, param):
    Coming = apps.get_model("stock", "Coming")
    coming = Coming()
    coming.datec = param[0]
    coming.numb = param[1]
    coming.organization_id = param[2]
    coming.automobile_id = param[3]
    coming.save()
    return 

# Найти или Добавить Категорию
def get_category(apps, val):   
    # Поиск категории
    if val in dict_category.values():
        for k, v in dict_category.items():
            if v == val:
                return k    
    else:
        Category = apps.get_model("stock", "Category")
        category = Category()
        category.title = val
        category.save()
        dict_category[category.id] = category.title
        return category.id

# Добавить товар
def insert_catalog(apps, param_catalog):   
    # Добавить товар
    Catalog = apps.get_model("stock", "Catalog")
    catalog = Catalog()
    catalog.coming_id = param_catalog[0]
    catalog.category_id = param_catalog[1]
    catalog.title = param_catalog[2]
    catalog.details = param_catalog[3]
    catalog.price = param_catalog[4]
    catalog.quantity = param_catalog[5]
    catalog.unit = param_catalog[6]
    catalog.photo = param_catalog[7]
    catalog.storage = param_catalog[8]
    catalog.save()
    dict_catalog_price[catalog.id] = catalog.price    
    return

# Добавить Расходные накладные 
def insert_outgo(apps, param):
    Outgo = apps.get_model("stock", "Outgo")
    outgo = Outgo()
    outgo.dateo = param[0]
    outgo.numb = param[1]
    outgo.organization_id = param[2]
    outgo.automobile_id = param[3]
    outgo.save()
    return 

# Добавить Продажи
def insert_sale(apps, param):
    Sale = apps.get_model("stock", "Sale")
    sale = Sale()
    sale.outgo_id = param[0]
    sale.catalog_id = param[1]
    sale.quantity = param[2]
    sale.save()
    return 

# Начальные данные
def new_data(apps, schema_editor):
    try:
        # Суперпользователь id=1
        user = User.objects.create_superuser(username='root',
        email='logistics150124@mail.ru',
        first_name='Максим', 
        last_name='Колесников',
        password='SsNn5678+-@')
        print("Суперпользователь создан")
    
        # Группа менеджеров
        managers = Group.objects.get_or_create(name = 'Managers')
        managers = Group.objects.get(name='Managers')
        print("Группа менеджеров создана")
    
        # Пользователь с ролью менеджера id=2
        user = User.objects.create_user(username='manager', password='Ss0066+-', email='manager@mail.ru', first_name='Александр', last_name='Левонтенко')
        managers.user_set.add(user)
        print("Менеджер добавлен в группу менеджеров")

        # Простые пользователи () id3-12
        user = User.objects.create_user(username='user1', password='Uu0066+-', email='user1@mail.ru', first_name='Станислав', last_name='Овсянников')
        user = User.objects.create_user(username='user2', password='Uu0066+-', email='user2@mail.ru', first_name='Анастасия', last_name='Тарапеева')
        user = User.objects.create_user(username='user3', password='Uu0066+-', email='user3@mail.ru', first_name='Екатерина', last_name='Авдеева')
        user = User.objects.create_user(username='user4', password='Uu0066+-', email='user4@mail.ru', first_name='Наталья', last_name='Пантилеева')
        user = User.objects.create_user(username='user5', password='Uu0066+-', email='user5@mail.ru', first_name='Анна', last_name='Ситникова')
        user = User.objects.create_user(username='user6', password='Uu0066+-', email='user6@mail.ru', first_name='Татьяна', last_name='Дешко')
        user = User.objects.create_user(username='user7', password='Uu0066+-', email='user7@mail.ru', first_name='Роман', last_name='Машенькин')
        user = User.objects.create_user(username='user8', password='Uu0066+-', email='user8@mail.ru', first_name='Евгений', last_name='Свистунов')
        user = User.objects.create_user(username='user9', password='Uu0066+-', email='user9@mail.ru', first_name='Павел', last_name='Григорьев')
        user = User.objects.create_user(username='user10', password='Uu0066+-', email='user10@mail.ru', first_name='Кристина', last_name='Ким')        
        print("Созданы простые пользователи")
        
        # Организации
        parameters = ["АО Консул", get_adres(False), get_telefon(), "konsul@mail.ru", "Шориков Андрей Алексеевич"]
        insert_organization(apps, parameters)
        parameters = ["Медиа Регион", get_adres(False), get_telefon(), "media_region@mail.ru", "Морхов Юрий Михайлович"]
        insert_organization(apps, parameters)
        parameters = ["Инжиниринг", get_adres(False), get_telefon(), "inzhiniring@mail.ru", "Гарнов Виктор Александрович"]
        insert_organization(apps, parameters)
        parameters = ["ТОО Облако", get_adres(False), get_telefon(), "oblako@mail.ru", "Воробьева Ксения Николаевна"]
        insert_organization(apps, parameters)
        parameters = ["АО Памир", get_adres(False), get_telefon(), "pamir@mail.ru", "Кахановский Дмитрий Дмитриевич"]
        insert_organization(apps, parameters)
        parameters = ["АО Радиан", get_adres(False), get_telefon(), "radian@mail.ru", "Антошина Дарья Владимировна"]
        insert_organization(apps, parameters)
        parameters = ["ООО Сакура", get_adres(False), get_telefon(), "sakura@mail.ru", "Котяшов Кирилл Сергеевич"]
        insert_organization(apps, parameters)
        parameters = ["ООО Таёжная лавка", get_adres(False), get_telefon(), "tayozhnaya_lavka@mail.ru", "Цитцер Екатерина Андреевна"]
        insert_organization(apps, parameters)
        parameters = ["АО Уголок", get_adres(False), get_telefon(), "ugolok@mail.ru", "Ким Алина Артуровна"]
        insert_organization(apps, parameters)
        parameters = ["ТОО Орион", get_adres(False), get_telefon(), "orion@mail.ru", "Панин Виктор Романович"]
        insert_organization(apps, parameters)
        parameters = ["ООО Цветомания", get_adres(False), get_telefon(), "cvetomaniya@mail.ru", "Лобкарев Сергей Андреевич"]
        insert_organization(apps, parameters)
        parameters = ["Чайная история", get_adres(False), get_telefon(), "chajnaya_istoriya@mail.ru", "Афанасьев Андрей Владимирович"]
        insert_organization(apps, parameters)
        parameters = ["ООО Шанс", get_adres(False), get_telefon(), "shans@mail.ru", "Раздрогов Максим Олегович"]
        insert_organization(apps, parameters)
        parameters = ["ООО Щит", get_adres(False), get_telefon(), "shchit@mail.ru", "Климов Никита Васильевич"]
        insert_organization(apps, parameters)
        parameters = ["ТО Эволюция", get_adres(False), get_telefon(), "evolyuciya@mail.ru", "Жуков Максим Андреевич"]
        insert_organization(apps, parameters)
        parameters = ["Континент", get_adres(False), get_telefon(), "kontinent@mail.ru", "Федорцов Андрей Геннадьевич"]
        insert_organization(apps, parameters)
        parameters = ["АО Яблоко", get_adres(False), get_telefon(), "yabloko@mail.ru", "Сорока Андрей Андреевич"]
        insert_organization(apps, parameters)
        parameters = ["ООО Багира", get_adres(False), get_telefon(), "bagira@mail.ru", "Гончарова Елена Андреевна"]
        insert_organization(apps, parameters)
        parameters = ["ООО Вагонтрейд", get_adres(False), get_telefon(), "vagontrejd@mail.ru", "Овсянников Станислав Валерьевич"]
        insert_organization(apps, parameters)
        parameters = ["ООО Газавтоцентр", get_adres(False), get_telefon(), "gazavtocentr@mail.ru", "Авдеева Екатерина Викторовна"]
        insert_organization(apps, parameters)
        parameters = ["ООО Даймонд", get_adres(False), get_telefon(), "dajmond@mail.ru", "Панова Наталья Александровна"]
        insert_organization(apps, parameters)
        parameters = ["ООО Еврахим", get_adres(False), get_telefon(), "evrahim@mail.ru", "Тоболина Анжелика Александровна"]
        insert_organization(apps, parameters)

        # Водители
        parameters = ["Афанасьев Андрей Владимирович", "1980-01-01 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Жуков Максим Андреевич", "1981-02-02 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Федорцов Андрей Геннадьевич", "1982-03-03 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Воронцов Вадим Борисович", "1983-04-04 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Кожанов Владимир Сергеевич", "1984-05-05 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Ковганюк Андрей Алексеевич", "1985-06-06 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Батаев Евгений Валентинович", "1986-07-07 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Васильев Илья Андреевич", "1987-08-08 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Серкин Роман Владимирович", "1988-09-09 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        parameters = ["Гнедченко Алексей Викторович", "1989-10-10 00:00:00", get_telefon(), "B, C, CE"]
        insert_driver(apps, parameters)
        
        # Автомобиль
        parameters = ["ГАЗ Next C41R13", "A123BE78RU", 1]
        insert_automobile(apps, parameters)
        parameters = ["ГАЗ Next C41R13", "S852DF78RU", 2]
        insert_automobile(apps, parameters)
        parameters = ["КамАЗ 43255-69", "G962FG78RU", 3]
        insert_automobile(apps, parameters)
        parameters = ["КамАЗ 43255-69", "M952FG78RU", 4]
        insert_automobile(apps, parameters)
        parameters = ["SHACMAN SX5256GJBDR384", "E854DF78RU", 5]
        insert_automobile(apps, parameters)
        parameters = ["SHACMAN SX5256GJBDR384", "W963WE78RU", 6]
        insert_automobile(apps, parameters)
        parameters = ["FAW CA 4180 P66K24E4", "H963FD78RU", 7]
        insert_automobile(apps, parameters)
        parameters = ["FAW CA 4180 P66K24E4", "L925JM78RU", 8]
        insert_automobile(apps, parameters)
        parameters = ["JAC C1721 Gallop", "D214FG78RU", 9]
        insert_automobile(apps, parameters)
        parameters = ["JAC C1721 Gallop", "K236HJ78RU", 10]
        insert_automobile(apps, parameters)
       
        # Приходные накладные
        parameters = [datetime.now() - timedelta(days=30) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 1, 1, 1]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=29) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 2, 2, 2]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=28) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 3, 3, 3]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=27) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 4, 4, 4]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=26) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 5, 5, 5]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=25) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 6, 6, 6]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=24) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 7, 7, 7]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=23) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 8, 8, 8]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=22) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 9, 9, 9]
        insert_coming(apps, parameters) 
        parameters = [datetime.now() - timedelta(days=21) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 10, 10, 10]
        insert_coming(apps, parameters) 

        #1 Каталог parameters - товар, (накладная, категория, название, описание, цена, количество, склад)
        parameters = [1, get_category(apps, "Покрытия для пола"), "Ламинат виниловый KRONOSPAN Kronostep SPC Z212 Sand Dune Oak Class 32/AC8. 1280*192*4", """
Длина (мм) 1280
Класс износостойкости 32
Количество в упаковке (шт) 8
Наличие фаски да
Площадь в упаковке (м²) 1.96
Поверхность матовая
Рисунок однополосный
Текстура дуб
Толщина (мм) 4
Ширина (мм) 192""", 3000, 100, "шт.", "images/catalog1.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [1, get_category(apps, "Покрытия для пола"), "Линолеум TARKETT ENERGY BOIL 2 3,5м 1 класс", """
Класс износостойкости 23/31
Материал основы пена+полиэстер
Материал покрытия ПВХ
Тип линолеума бытовой
Толщина защитного слоя (мм) 0.40
Толщина (мм) 3.0
Ширина (м) 3.5""", 500, 100, "шт.", "images/catalog2.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [2, get_category(apps, "Водоэмульсии"), "Краска PUFAS Матовая латексная Matt-Latex Classic 10л", """
Материал обработки бетон
Моющиеся да
Область применения для внутренних работ, для наружных работ, для обоев, для потолков, для стен
Объем (л) 10.0
Расход (м²) 7.0
Степень глянца матовая""", 3200, 100, "шт.", "images/catalog3.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [2, get_category(apps, "Водоэмульсии"), "Краска РАДУГА-114 ЭКСТРА акриловая суперстойкая для фасадов и интерьеров база С 9л", """
Моющиеся да
Область применения фасадная
Объем (л) 9.0
Расход (м²) 6-8
Степень глянца матовая""", 2300, 100, "шт.", "images/catalog4.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [3, get_category(apps, "Краски"), "Краска PUFAS Металл Эффект Orient gold 750мл", """
Вес (кг) 0.75
Время высыхания (ч) 12
Количество слоев 1
Область применения для металла
Стойкость к мытью да
Цвет золото
Эффект orient""", 600, 100, "шт.", "images/catalog5.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [3, get_category(apps, "Краски"), "Краска декоративная РАДУГА-34 акриловая с мелкой фракцией влагост PROFI 25кг", """
Время высыхания (ч) 6-8
Покрытие фактурное""", 3200, 100, "шт.", "images/catalog6.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [4, get_category(apps, "Лаки"), "Лак РАСЦВЕТ для наружных работ алкидный 1,9кг", """
Вес (кг) 1.9
Время высыхания (ч) 36
Материал обработки дерево, камень, металл
Область применения для наружных работ
Основа алкидный
Расход (г/м2) 70-75
Степень блеска высокоглянцевый
Тип лак""", 900, 100, "шт.", "images/catalog7.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [4, get_category(apps, "Лаки"), "Лак GRAND VICTORY акриловый б/ц Platinum 1л", """
Материал обработки дерево
Область применения для внутренних работ, для наружных работ
Объем (л) 1.0
Основа акриловая
Степень блеска полуглянцевый""", 510, 100, "шт.", "images/catalog8.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [5, get_category(apps, "Эмали"), "Эмаль РАДУГА Arcobaleno Castello ультрастойкая для фасадов и интерьеров 9л", """
Область применения детских комнат, для интерьеров, для обоев, для фасадов
Степень блеска матовая""", 7100, 100, "шт.", "images/catalog9.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [5, get_category(apps, "Эмали"), "Эмаль КВИЛ ПФ-115 универсальная салатн. 1,9кг", """
Вес (кг) 1.9
Область применения универсальная
Цвет зеленый""", 650, 100, "шт.", "images/catalog10.jpg", "Склад №1"]
        insert_catalog(apps, parameters)    
        parameters = [6, get_category(apps, "Ванны"), "Ванна 1,8 Сибирячка-У с ручками", """
Объем (л) 285
Особенность с ножками
Тип встраиваемая
Угловая нет
Ширина (см) 80
Материал ванны чугун
Форма ванны прямоугольная
Длина (см) 180""", 42000, 100, "шт.", "images/catalog11.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [6, get_category(apps, "Ванны"), "Ванна акриловая AM.PM Gem A1 150*70 ", """
Особенность без ножек
Ширина (см) 75
Материал ванны акрил
Форма ванны прямоугольная
Длина (см) 170""", 21000, 100, "шт.", "images/catalog12.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [7, get_category(apps, "Душевые кабины"), "Душевая кабина ER3509P-C3 900*900-2150 низкий поддон", """
Тип душевой кабины закрытая (бокс)
Формат душевой кабины 1/4 круга
Поддон низкий
Задняя стенка стекло
Материал поддона акрил
Конструкция дверей раздвижные
Опции душевой кабины зеркало, полочка, ручной душ, тропический душ
Количество створок двери 2
Стекло матовое
Габариты (см) 90х90х215""", 39500, 100, "шт.", "images/catalog13.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [7, get_category(apps, "Душевые кабины"), "Душевая кабина DOMANI-Simple high с крышей (99) 90*90*218", """
Тип душевой кабины закрытый
Поддон высокий
Материал поддона акрил
Конструкция дверей раздвижные""", 36100, 100, "шт.", "images/catalog14.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [8, get_category(apps, "Мойки кухонные"), "Мойка ГРАНИКОМ модель G-005 Сахара (800*485)", """
Монтаж мойки врезная
Материал мрамор
Размер мойки (см) 80х48.5
Форма мойки прямоугольная
Количество чаш одна
Расположение чаши справа""", 8150, 100, "шт.", "images/catalog15.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [8, get_category(apps, "Мойки кухонные"), "Кухонная мойка 600*450 арт.ST-AS6045BR матовый хром", """
Глубина мойки (см) 45
Монтаж мойки врезная
Цвет серебристый
Ширина мойки (см) 60
Материал нержавеющая сталь
Форма мойки прямоугольная
Количество чаш 1""", 8150, 100, "шт.", "images/catalog16.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [9, get_category(apps, "Смесители"), "Смеситель AM.PM для кухни LIKE с каналом для питьевой воды", """
Материал корпуса латунь
Назначение смесителя для кухни
Тип запорной арматуры керамический картридж
Тип излива высокий
Тип смесителя однорычажный
Цвет черный
Способ монтажа смесителя на мойку""", 8000, 100, "шт.", "images/catalog17.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [9, get_category(apps, "Смесители"), "Смеситель AM.PM для умывальника GEM высокий, хром", """
Материал корпуса латунь
Назначение смесителя для ванны с душем
Тип запорной арматуры керамический картридж
Тип излива короткий излив
Тип смесителя однорычажный
Цвет хром
Способ монтажа смесителя на мойку""", 11000, 100, "шт.", "images/catalog18.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [10, get_category(apps, "Плинтусы"), "Плинтус ESPUMO 80 Светло-серый ESP202 A 2,4", """
Длина (мм) 2400
Крепление клей
С кабель каналом нет
Структура поверхности гладкая
Цвет плинтуса белый""", 410, 100, "шт.", "images/catalog19.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    
        parameters = [10, get_category(apps, "Плинтусы"), "Плинтус WINART с съемной панелью 2,2м 100мм", """
Высота (мм) 100
Длина (мм) 2200
Крепление саморезы
С кабель каналом да
Структура поверхности гладкая
Цвет плинтуса белый""", 220, 100, "шт.", "images/catalog20.jpg", "Склад №2"]
        insert_catalog(apps, parameters)    

        # Расходные накладные
        parameters = [datetime.now() - timedelta(days=20) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 1, 11, 1]
        insert_outgo(apps, parameters)             
        parameters = [datetime.now() - timedelta(days=19) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 2, 12, 2]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=18) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 3, 13, 3]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=17) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 4, 14, 4]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=16) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 5, 15, 5]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=15) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 6, 16, 6]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=14) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 7, 17, 7]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=13) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 8, 18, 8]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=12) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 9, 19, 9]
        insert_outgo(apps, parameters)     
        parameters = [datetime.now() - timedelta(days=11) - timedelta(hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond), 10, 20, 10]
        insert_outgo(apps, parameters)     

        # Продажи
        parameters = [1, 1, 20]
        insert_sale(apps, parameters)     
        parameters = [1, 2, 12]
        insert_sale(apps, parameters)     
        parameters = [2, 3, 10]
        insert_sale(apps, parameters)     
        parameters = [2, 4, 10]
        insert_sale(apps, parameters)     
        parameters = [3, 5, 11]
        insert_sale(apps, parameters)     
        parameters = [3, 6, 15]
        insert_sale(apps, parameters)     
        parameters = [4, 7, 5]
        insert_sale(apps, parameters)     
        parameters = [4, 8, 7]
        insert_sale(apps, parameters)     
        parameters = [5, 9, 21]
        insert_sale(apps, parameters)     
        parameters = [5, 10, 20]
        insert_sale(apps, parameters)     
        parameters = [6, 11, 4]
        insert_sale(apps, parameters)     
        parameters = [6, 12, 5]
        insert_sale(apps, parameters)     
        parameters = [7, 13, 4]
        insert_sale(apps, parameters)     
        parameters = [7, 14, 4]
        insert_sale(apps, parameters)     
        parameters = [8, 15, 7]
        insert_sale(apps, parameters)     
        parameters = [8, 16, 7]
        insert_sale(apps, parameters)     
        parameters = [9, 17, 9]
        insert_sale(apps, parameters)     
        parameters = [9, 18, 9]
        insert_sale(apps, parameters)     
        parameters = [10, 19, 10]
        insert_sale(apps, parameters)     
        parameters = [10, 20, 10]
        insert_sale(apps, parameters)     


    except Exception as error:
        print(error)


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(new_data),
      migrations.RunSQL("""CREATE VIEW view_coming AS
        SELECT coming.id, coming.datec, coming.numb, coming.organization_id, organization.name AS organization, coming.automobile_id, automobile.replica AS replica, automobile.reg_number AS reg_number, 
        (SELECT SUM((price*quantity)) FROM catalog WHERE catalog.coming_id=coming.id) AS total 
        FROM coming LEFT JOIN organization ON coming.organization_id = organization.id
        LEFT JOIN automobile ON coming.automobile_id = automobile.id"""),

        migrations.RunSQL("""CREATE VIEW view_catalog AS
        SELECT catalog.id, catalog.coming_id, catalog.category_id, category.title AS category, catalog.title,catalog.details, catalog.price, catalog.quantity, (catalog.price*catalog.quantity) AS total, catalog.unit, catalog.photo, catalog.storage, 
        (SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id) AS sale_quantity,
        CASE 
        WHEN (catalog.quantity - (SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id)) IS NULL 
        THEN catalog.quantity 
        ELSE (catalog.quantity - (SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id)) 
        END
        AS available
        FROM catalog LEFT JOIN category ON catalog.category_id = category.id
        WHERE catalog.quantity > 0
        ORDER BY catalog.title,  catalog.title"""),        
        
        migrations.RunSQL("""CREATE VIEW view_outgo AS
        SELECT o.id, o.dateo, o.numb, o.organization_id, organization.name AS organization, o.automobile_id, automobile.replica AS replica, automobile.reg_number AS reg_number, 
        (SELECT SUM(sale.quantity*catalog.price)
        FROM sale LEFT JOIN catalog ON sale.catalog_id=catalog.id
        LEFT JOIN outgo ON sale.outgo_id=outgo.id
        WHERE outgo_id=o.id)  AS total 
		FROM outgo o LEFT JOIN organization ON o.organization_id = organization.id
        LEFT JOIN automobile ON o.automobile_id = automobile.id"""),
        
        migrations.RunSQL("""CREATE VIEW view_sale AS
        SELECT sale.id, sale.outgo_id, view_outgo.dateo, view_outgo.numb, view_outgo.organization, view_outgo.replica, view_outgo.reg_number, sale.catalog_id, view_catalog.category, view_catalog.title, view_catalog.details,
        view_catalog.price, sale.quantity, view_catalog.unit, view_catalog.photo, view_catalog.storage, (sale.quantity*view_catalog.price) AS total
        FROM sale LEFT JOIN view_outgo ON sale.outgo_id=view_outgo.id
        LEFT JOIN view_catalog ON sale.catalog_id=view_catalog.id"""),     
        

    ]

