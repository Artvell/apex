from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField


class Categories(models.Model):
    objects=models.Manager()
    category = models.CharField(max_length=50,verbose_name="Категории")
    def __str__(self):
        return self.category
    class Meta:
        db_table = 'roles_categories'
        verbose_name="Категория"
        verbose_name_plural="Категории"


class Codes(models.Model):
    objects=models.Manager()
    shtrih = models.CharField(max_length=50,verbose_name="Штрих-код")
    kolvo = models.FloatField(verbose_name="Кол-во")
    name = models.ForeignKey('Products', on_delete=models.PROTECT, blank=True, null=True,verbose_name="Продукт")
    def __str__(self):
        return self.name.name
    class Meta:
        db_table = 'roles_codes'
        verbose_name="Штрих-код"
        verbose_name_plural="Штрих-коды"


class Consuption(models.Model):
    objects=models.Manager()
    class Meta:
        db_table = 'roles_consuption'
        verbose_name=""
        verbose_name_plural=""


class DopMoney(models.Model):
    objects=models.Manager()
    nak_id = models.IntegerField(verbose_name="Номер накладной")
    dop_type = models.ForeignKey('DopTypes', models.DO_NOTHING,verbose_name="Тип расхода")
    purchaser = models.ForeignKey(User,limit_choices_to={"roles__role":3},on_delete=models.PROTECT, blank=True, null=True,verbose_name="Закупщик")
    money = models.IntegerField(verbose_name = "Потрачено")

    class Meta:
        db_table = 'roles_dop_money'
        verbose_name="Дополнительные расходы"
        verbose_name_plural="Дополнительные расходы"


class DopTypes(models.Model):
    objects=models.Manager()
    name = models.CharField(max_length=50,verbose_name = "Тип расхода")
    min_summ = models.IntegerField(verbose_name = "Минимальная сумма")
    max_summ = models.IntegerField(verbose_name = "Максимальная сумма")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'roles_dop_types'
        verbose_name="Тип доп.расходов"
        verbose_name_plural="Типы доп.расходов"


class Ingredients(models.Model):
    objects=models.Manager()
    kolvo = models.FloatField(verbose_name="Кол-во")
    ingr = models.ForeignKey('Products',related_name="ingr",on_delete=models.PROTECT,verbose_name="Ингридиент")
    product = models.ForeignKey('Products',on_delete=models.PROTECT,verbose_name="Продукт")
    def __str__(self):
        return self.product.name
    class Meta:
        db_table = 'roles_ingredients'
        verbose_name="Ингридиент"
        verbose_name_plural="Ингридиенты"


class Ingredients_dop_info(models.Model):
    objects=models.Manager()
    srok = models.FloatField()
    procent = models.FloatField()
    product = models.ForeignKey('Products',on_delete=models.PROTECT)

    class Meta:
        db_table = 'roles_ingredients_dop_info'


class LastCost(models.Model):
    objects=models.Manager()
    cost = models.FloatField(verbose_name="Последняя цена")
    product = models.ForeignKey('Products', models.DO_NOTHING)
    average = models.FloatField(verbose_name="Средняя цена",default=0.0)
    kol = models.FloatField(verbose_name="Купленное кол-во единиц",default=0.0)
    def __str__(self):
        return self.product.name
    class Meta:
        db_table = 'roles_lastcost'
        verbose_name="Последняя цена"
        verbose_name_plural="Последняя цена"


class Money(models.Model):
    objects=models.Manager()
    dat = models.DateField()
    dsumma = models.IntegerField()
    is_calculated = models.IntegerField()
    isumma = models.IntegerField()
    nak_id = models.CharField(max_length=37)
    nsumma = models.IntegerField()
    psumma = models.IntegerField()
    rsumma = models.IntegerField()
    vsumma = models.IntegerField()

    class Meta:
        db_table = 'roles_money'


class MoneyReceivers(models.Model):
    objects=models.Manager()
    name = models.CharField(max_length=50,verbose_name="Объекты списания")

    class Meta:
        db_table = 'roles_money_receivers'


class Moneys(models.Model):
    objects=models.Manager()
    kolvo = models.FloatField(verbose_name="Кол-во")
    types = models.OneToOneField('Types_of_money', models.DO_NOTHING, blank=True, null=True,verbose_name="Тип")
    def __str__(self):
        return self.types.types
    class Meta:
        db_table = 'roles_moneys'
        verbose_name="Деньги"
        verbose_name_plural="Деньги"

class Buyer_Balans(models.Model):
    objects=models.Manager()
    buyer=models.OneToOneField(User,on_delete=models.PROTECT,limit_choices_to={"roles__role":3},verbose_name="Закупщик")
    balans=models.FloatField(verbose_name="Баланс",default=0.0)
    debt=models.FloatField(verbose_name="Долг",default=0.0)
    def __str__(self):
        return self.buyer.username
    class Meta:
        verbose_name="Баланс закупщика"
        verbose_name_plural="Баланс закупщиков"

class Nakl_for_zagot(models.Model):
    objects=models.Manager()
    nak_id = models.IntegerField(verbose_name="Номер накладной")
    name = models.ForeignKey('Products',on_delete=models.PROTECT,verbose_name="Продукт",blank=True,null=True)
    tkolvo = models.FloatField(verbose_name="Требуемое кол-во",default=0.0)
    pkolvo = models.FloatField(verbose_name="Приготовленное кол-во",default=0.0)
    price = models.FloatField(verbose_name="Цена",default=0.0)
    summ = models.FloatField(verbose_name="Сумма",default=0.0)
    is_maked = models.BooleanField(verbose_name="Изготовлен?",default=False)
    ac_kolvo = models.FloatField(verbose_name="Принятое кол-во",default=0.0)
    is_accepted = models.BooleanField(default=False,verbose_name="Принята?")
    is_given=models.BooleanField(default=False,verbose_name="Ингридиенты выданы?")
    is_taken=models.BooleanField(default=False,verbose_name="Ингридиенты приняты?")
    srok = models.DateTimeField(blank=True, null=True,verbose_name="Срок годности")
    in_stock = models.BooleanField(default=False,verbose_name="Поступил на склад?")
    shtrih = models.CharField(max_length=20,default="",blank=True,null=True)
    user = models.ForeignKey('Zagot_types',on_delete=models.PROTECT,verbose_name="Заготовщик",blank=True,null=True,editable=False)
    is_returned = models.BooleanField(verbose_name="Возвращен?",default=False)
    def __str__(self):
        return self.name.name
    class Meta:
        db_table = 'roles_nakl_for_zagot'
        verbose_name="Накладная для заготовщика"
        verbose_name_plural="Накладные для заготовщика"

class Zagot_products(models.Model):
    objects=models.Manager()
    nak_id=models.IntegerField()
    user = models.ForeignKey('Zagot_types',on_delete=models.PROTECT,verbose_name="Заготовщик",blank=True,null=True)
    product=models.ForeignKey('Products',on_delete=models.PROTECT)
    kol=models.FloatField(verbose_name="Списанное кол-во")
    kolvo=models.FloatField(verbose_name="Принятое кол-во")
    status=models.BooleanField(verbose_name="Принято?",default=False)
    def __str__(self):
        return str(self.nak_id)
    class Meta:
        verbose_name="Списано заготовщику"
        verbose_name_plural="Списано заготовщику"

class Harvester_Stock(models.Model):
    objects=models.Manager()
    product=models.ForeignKey('Products',on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Заготовщик")
    kol=models.FloatField(verbose_name='Кол-во')
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name='Склад заготовщика'
        verbose_name_plural='Склад заготовщика'

class Harvester_Barcodes(models.Model):
    objects=models.Manager()
    nak_id=models.IntegerField()
    product_id=models.IntegerField()
    barcode=models.CharField(max_length=20,default="")
    from datetime import date
    date=models.DateField(default=date.today)
    def __str__(self):
        return self.barcode

class Nakl_money_other(models.Model):
    objects=models.Manager()
    name = models.CharField(max_length=20)
    for_why = models.TextField()
    kolvo = models.FloatField()
    types = models.ForeignKey('Types_of_money', models.DO_NOTHING, blank=True, null=True)
    date=models.DateField( blank=True, null=True)

    class Meta:
        db_table = 'roles_nakl_money_other'
        verbose_name="Выдача денег(не закупщик)"
        verbose_name_plural="Выдача денег(не закупщик)"


class Nakl_money_zakup(models.Model):
    objects=models.Manager()
    kolvo = models.FloatField()
    name = models.ForeignKey(User, models.DO_NOTHING)
    date=models.DateField(blank=True, null=True)
    types = models.ForeignKey('Types_of_money', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'roles_nakl_money_zakup'
        verbose_name="Выдача денег(закупщик)"
        verbose_name_plural="Выдача денег(закупщик)"

class Receiving_Money(models.Model):
    objects=models.Manager()
    kolvo = models.FloatField(verbose_name="Кол-во")
    types = models.ForeignKey('Types_of_money', models.DO_NOTHING, blank=True, null=True,verbose_name="Типы денег")
    date=models.DateField(blank=True, null=True,verbose_name="Дата")
    class Meta:
        verbose_name="Приход денег"
        verbose_name_plural="Приход денег"

class Pizzerias(models.Model):
    objects=models.Manager()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'roles_pizzerias'
        verbose_name="Пиццерия"
        verbose_name_plural="Пиццерии"


class Postavsh(models.Model):
    objects=models.Manager()
    firm_name = models.CharField(max_length=50)
    name = models.CharField(unique=True, max_length=20)
    contact = models.CharField(max_length=50)
    place = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'roles_postavsh'
        verbose_name="Поставщик"
        verbose_name_plural="Поставщики"


class Products(models.Model):
    objects=models.Manager()
    name = models.CharField(max_length=100,verbose_name="Название")
    image = models.ImageField(verbose_name="Изображение", blank=True, null=True,)
    prigot = models.BooleanField(verbose_name="Приготовляемый товар?")
    category= models.ForeignKey(Categories,on_delete=models.PROTECT, blank=True, null=True,verbose_name="Категория")
    edizm = models.ForeignKey('Units',on_delete=models.PROTECT, blank=True, null=True,verbose_name="Ед.измерения")
    maks_zakup = models.IntegerField(verbose_name="Закупка на дни")
    min_zakup = models.IntegerField(verbose_name="Минимальные дни для закупки")
    rashod = models.FloatField(verbose_name="Расход в день")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'roles_products'
        verbose_name="Товар"
        verbose_name_plural="Товары"

class Products_Consumption(models.Model):
    objects=models.Manager()
    name=models.OneToOneField('Products',on_delete=models.PROTECT,verbose_name="Продукт")
    day=models.IntegerField(verbose_name="День",default=1,editable=False)
    days=models.IntegerField(verbose_name="Всего дней")
    #daily_consumption=models.FloatField(verbose_name="Расход за день")
    consumption=JSONField(verbose_name="Расход",default=[0])
    def __str__(self):
        return self.name.name
    class Meta:
        verbose_name="Расход продуктов"
        verbose_name_plural="Расход продуктов"

class Daily_Consumption(models.Model):
    objects=models.Manager()
    name=models.OneToOneField('Products',on_delete=models.PROTECT,verbose_name="Продукт")
    consumption=models.FloatField(verbose_name="Расход за сегодня")
    def __str__(self):
        return self.name.name
    class Meta:
        verbose_name="Дневной расход продукта"
        verbose_name_plural="Дневной расход продуктов"

class Purchase(models.Model):
    objects=models.Manager()
    nak_id = models.CharField(max_length=50,verbose_name="Номер накладной")
    name = models.ForeignKey(Products, models.DO_NOTHING,verbose_name="Название")
    last_cost = models.FloatField(verbose_name="Последняя цена")
    kolvo = models.FloatField(verbose_name="Требуемое кол-во")
    is_accepted = models.BooleanField(verbose_name="Накладная принята?",default=False)
    purchased_kol = models.FloatField(verbose_name="Купленное кол-во",default=0.0)
    fact_kol=models.FloatField(verbose_name="Фактическое кол-во",blank=True, null=True,default=0.0)
    new_cost = models.FloatField(verbose_name="Новая цена",blank=True, null=True)
    summ = models.FloatField(verbose_name="Сумма",blank=True, null=True)
    min_srok = models.DateField(blank=True, null=True,verbose_name="Минимальный срок годности")
    srok = models.DateField(blank=True, null=True,verbose_name="Срок годности")
    is_accepted_zakup = models.BooleanField(verbose_name="Принято закупщиком?",default=False)
    is_delivered = models.BooleanField(verbose_name="Куплен?",default=False)
    is_ordered=models.BooleanField(verbose_name="Заказан?",default=False)
    is_borrowed=models.BooleanField(verbose_name="Взят в долг?",default=False)
    saler=models.ForeignKey(Postavsh,on_delete=models.PROTECT,verbose_name="Продавец",blank=True, null=True)
    purchase = models.ForeignKey(User,on_delete=models.PROTECT, blank=True, null=True,verbose_name="Закупщик")
    is_returned = models.BooleanField(verbose_name="Возвращен?",default=False)
    date = models.DateField(blank=True, null=True,verbose_name="Дата накладной")
    def __str__(self):
        return self.name.name
    class Meta:
        db_table = 'roles_purchase'
        verbose_name="Накладная для закупщика"
        verbose_name_plural="Накладные для закупщика"



class Rashod_zagot(models.Model):
    objects=models.Manager()
    kol = models.IntegerField()
    nak_id = models.ForeignKey(Nakl_for_zagot, models.DO_NOTHING)
    name = models.ForeignKey(Products, models.DO_NOTHING)

    class Meta:
        db_table = 'roles_rashod_zagot'
        verbose_name="Расход заготовщика"
        verbose_name_plural="Расходы заготовщика"

class Receivers(models.Model):
    objects=models.Manager()
    receiver = models.CharField(max_length=100,verbose_name="Объект списания")
    def __str__(self):
        return self.receiver
    class Meta:
        db_table = 'roles_receivers'
        verbose_name="Объекст списания"
        verbose_name_plural="Объекты списания"

class Roles(models.Model):
    choices=[
        (1,"Завсклад"),
        (2,"Кассир"),
        (3,"Закупщик"),
        (4,"Заготовщик"),
        (5,"Пиццемейкер"),
        (6,"Пиццедоставщик"),
        (7,"Пиццекассир"),
        (8,"Администратор")
    ]
    objects=models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="Работник")
    place = models.ForeignKey(Pizzerias,on_delete=models.CASCADE,verbose_name="Пиццерия",null=True,blank=True)
    role = models.IntegerField(blank=True,verbose_name="Роль",choices=choices,null=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name="Роль"
        verbose_name_plural="Роли"

#связь  и реакция на изменения
@receiver(post_save, sender=(User,Pizzerias))
def create_user_role(sender, instance, created, **kwargs):
    if created:
        Roles.profile.create(user=instance)

@receiver(post_save, sender=(User,Pizzerias))
def save_user_role(sender, instance, **kwargs):
    instance.roles.save()
####

class Salers(models.Model):
    objects=models.Manager()
    last_cost = models.FloatField(verbose_name="Последняя цена")
    product = models.ForeignKey(Products,on_delete=models.PROTECT,verbose_name="Товар")
    saler = models.ForeignKey(Postavsh,on_delete=models.PROTECT,verbose_name="Продавец")
    def __str__(self):
        return self.saler.name
    class Meta:
        db_table = 'roles_salers'
        verbose_name="Продавец"
        verbose_name_plural="Продавцы"

class Spis(models.Model):
    objects=models.Manager()
    i = models.AutoField(primary_key=True)
    nak_id = models.IntegerField(verbose_name="Номер накладной")
    user = models.CharField(max_length=20,verbose_name="Кем выдано")
    product = models.CharField(max_length=100,verbose_name="Товар")
    kol = models.FloatField(verbose_name="Кол-во")
    date = models.DateTimeField(blank=True, null=True,verbose_name="Дата")
    receiver = models.ForeignKey(Receivers,on_delete=models.PROTECT,verbose_name="Кому")
    is_removed = models.BooleanField(verbose_name="Отменена?",default=False)
    class Meta:
        db_table = 'roles_spis'
        verbose_name="Накладная на списание"
        verbose_name_plural="Накладные на списание"

class Stock(models.Model):
    objects=models.Manager()
    name = models.OneToOneField(Products, models.DO_NOTHING, blank=True, null=True,verbose_name="Товар")
    ostat = models.FloatField(verbose_name="Кол-во")
    def __str__(self):
        return self.name.name
    class Meta:
        db_table = 'roles_stock'
        verbose_name="Склад"
        verbose_name_plural="Склад"

class Rediscount(models.Model):
    objects=models.Manager()
    red_id = models.IntegerField(verbose_name="Номер переучета",default=0)
    name=models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True,verbose_name="Товар")
    kol = models.FloatField(verbose_name="Кол-во",default=0.0)
    def __str__(self):
        return str(self.red_id)
    class Meta:
        verbose_name="Переучет"
        verbose_name_plural="Переучет"

class Rediscount_info(models.Model):
    objects=models.Manager()
    rediscount=models.OneToOneField(Rediscount,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Переучет")
    date = models.DateField(verbose_name="Дата переучета", blank=True, null=True)
    progress = models.CharField(verbose_name="Прогресс переучета",default=0.0,max_length=10)
    user= models.ForeignKey(User,verbose_name="Провел",on_delete=models.CASCADE, blank=True, null=True)
    is_closed= models.FloatField(verbose_name="Закончен?",default=False)
    def __str__(self):
        return str(self.rediscount)
    class Meta:
        verbose_name="Отчет о переучете"
        verbose_name_plural="Отчеты о переучете"

class Types_of_money(models.Model):
    objects=models.Manager()
    types = models.CharField(unique=True, max_length=50,verbose_name="Типы")
    def __str__(self):
        return self.types
    class Meta:
        db_table = 'roles_types_of_money'
        verbose_name="Тип денег"
        verbose_name_plural="Типы денег"

class Units(models.Model):
    objects=models.Manager()
    edizm = models.CharField(max_length=20,verbose_name="Ед.измерения")
    opis = models.CharField(max_length=50,verbose_name="Описание")
    def __str__(self):
        return self.edizm
    class Meta:
        db_table = 'roles_units'
        verbose_name="Ед.измерения"
        verbose_name_plural="Ед.измерения"

class Zagot_types(models.Model):
    objects=models.Manager()
    product = models.ForeignKey(Products, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    def __str__(self):
        return self.user.username
    class Meta:
        db_table = 'roles_zagot_types'
        verbose_name="Заготовщик"
        verbose_name_plural="Заготовщики"


class Zakupshiki(models.Model):
    objects=models.Manager()
    name = models.ForeignKey(Products,on_delete = models.CASCADE,verbose_name="Товар")
    user = models.ForeignKey(User,limit_choices_to={"roles__role":3},on_delete = models.CASCADE,verbose_name="Закупщик")
    class Meta:
        db_table = 'roles_zakupshiki'
        verbose_name="Закупщик"
        verbose_name_plural="Закупщики"


class Printers(models.Model):
    objects = models.Manager()
    name = models.CharField(verbose_name="Название",max_length=50)
    ip_address = models.CharField(verbose_name="IP адрес",max_length=15)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="IP принтер"
        verbose_name_plural="IP принтеры"