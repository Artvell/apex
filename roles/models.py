from django.db import models
from django.contrib.auth.models import User
#импорты для изменения данных одновременно с юзер
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Units(models.Model):
    unit=models.Manager()
    edizm=models.CharField(verbose_name="Обозначение",max_length=20)
    opis=models.CharField(verbose_name="Описание",max_length=50)
    def __str__(self):
        return self.edizm
    class Meta:
        verbose_name="Единица измерения"
        verbose_name_plural="Единицы измерения"


class Products(models.Model):
    artikul=models.CharField(verbose_name="Артикул",max_length=6)
    name=models.CharField(verbose_name="Название товара",max_length=100)
    image=models.ImageField(verbose_name="Изображение")
    edizm=models.ForeignKey(Units,on_delete=models.CASCADE,verbose_name="Ед.измерения",null=True)
    prigot=models.BooleanField(verbose_name="Приготавливаемый товар?")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"


class Pizzerias(models.Model):
    pr=models.Manager()
    name=models.CharField(verbose_name="Название пиццерии",max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="Пиццерия"
        verbose_name_plural="Пиццерии"
    
class Postavsh(models.Model):
    pos=models.Manager()
    firm_name=models.CharField(max_length=50,verbose_name="Фирма-поставщик",default="")
    name=models.CharField(max_length=20,verbose_name="Контактное лицо",default="")
    contact=models.CharField(max_length=50,verbose_name="Контактные данные",default="")
    place=models.TextField(verbose_name="Расположение",default="")
    class Meta:
        verbose_name="Поставщик"
        verbose_name_plural="Поставщики"

class Stock(models.Model):
    st=models.Manager()
    name=models.OneToOneField(Products,on_delete=models.CASCADE,verbose_name="Товар",null=True)
    kolvo=models.IntegerField(verbose_name="Кол-во")
    scena=models.IntegerField(verbose_name="Ср.цена",default=1)
    summ=models.FloatField(verbose_name="Сумма",default=0.0)
    rashod=models.IntegerField(verbose_name="Ср.расход в день",default=1)
    ostat=models.FloatField(verbose_name="Осталось на складе",default=0.0)
    shtrih=models.IntegerField(verbose_name="Штрих-код")
    #ostat=models.IntegerField(verbose_name="Остаток на дни",default=kolvo/rashod,editable=False)
    maks_zakup=models.IntegerField(verbose_name="Закупка на дни",default=1)
    min_zakup=models.IntegerField(verbose_name="Миним.дни для закупки",default=1)
    class Meta:
        verbose_name=" На склад"
        verbose_name_plural="Склад"

class Purchase(models.Model):
    pur=models.Manager()
    nak_id=models.CharField(verbose_name="Номер накладной",max_length=50)
    name=models.OneToOneField(Products,on_delete=models.CASCADE,verbose_name="Товар")
    last_cost=models.FloatField(verbose_name="Последняя цена")
    kolvo=models.FloatField(verbose_name="Требуемое кол-во")
    min_srok=models.IntegerField(verbose_name="Мин.срок годности")
    is_accepted=models.BooleanField(verbose_name="Накладная принята?")
    purchased_kol=models.FloatField(verbose_name="Купленное кол-во")
    new_cost=models.FloatField(verbose_name="Цена")
    summ=models.FloatField(verbose_name="Сумма",default=0.0)
    fact_kol=models.FloatField(verbose_name="Фактическое кол-во")
    srok=models.DateField(verbose_name="Срок годности",null=True)
    shtrih=models.IntegerField(verbose_name="Штрих-код")
    is_delivered=models.BooleanField(verbose_name="Поступил на склад?")
    class Meta:
        verbose_name="Накладная для закупки"
        verbose_name_plural="Накладная для закупки"

class Money(models.Model):
    objects=models.Manager()
    nak_id=models.CharField(max_length=37,verbose_name="№ накладной")
    dat=models.DateField(verbose_name="Дата накладной",auto_now=True)
    nsumma=models.IntegerField(verbose_name="Требуемая сумма для закупки")
    dsumma=models.IntegerField(verbose_name="Выданная сумма")
    isumma=models.IntegerField(verbose_name="Истраченная сумма")
    psumma=models.IntegerField(verbose_name="Прочие расходы")
    rsumma=models.IntegerField(verbose_name="Итого расход")
    vsumma=models.IntegerField(verbose_name="Сумма возврата/выдачи")
    is_calculated=models.BooleanField(verbose_name="Расчет произведен?")
    class Meta:
        verbose_name="Деньги для закупки"
        verbose_name_plural="Деньги для закупки"
    
class Dop_types(models.Model):
    objects=models.Manager()
    name=models.CharField(verbose_name="Название прочего расхода",max_length=50)
    min_summ=models.IntegerField(verbose_name="Минимальная сумма")
    max_summ=models.IntegerField(verbose_name="Максимальная сумма")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="Тип дополнительных расходов"
        verbose_name_plural="Типы дополнительных расходов"

class Dop_money(models.Model):
    objects=models.Manager()
    nak_id=models.ForeignKey(Purchase,on_delete=models.CASCADE,verbose_name="Номер накладной")
    dop_type=models.ForeignKey(Dop_types,on_delete=models.CASCADE,verbose_name="Тип расхода")
    money=models.IntegerField(verbose_name="Сумма")
    class Meta:
        verbose_name="Дополнительные расходы"
        verbose_name_plural="Дополнительные расходы"
    
class Nakl_for_zagot(models.Model):
    name=models.OneToOneField(Products,on_delete=models.CASCADE,verbose_name="Товар")
    tkolvo=models.FloatField(verbose_name="Требуемое количество")
    is_accepted=models.BooleanField(verbose_name="Накладная принята?")
    pkolvo=models.FloatField(verbose_name="Приготовленное количество")
    price=models.FloatField(verbose_name="Цена")
    summ=models.FloatField(verbose_name="Сумма",default=0.0)
    is_maked=models.BooleanField(verbose_name="Товар приготовлен?")
    ac_kolvo=models.FloatField(verbose_name="Принятое количество")
    srok=models.DateField(verbose_name="Срок годности")
    shtrih=models.IntegerField(verbose_name="Штрих-код")
    in_stock=models.BooleanField(verbose_name="Поступил на склад?")
    class Meta:
        verbose_name="Накладная для заготовщика"
        verbose_name_plural="Накладные для заготовщика"

class Ingredients(models.Model):
    product=models.ForeignKey(Products,related_name="product",on_delete=models.CASCADE,verbose_name="Заготовляемый товар")
    ingr=models.ForeignKey(Products,related_name="ingr",on_delete=models.CASCADE,verbose_name="Ингридиент")
    kolvo=models.IntegerField(verbose_name="Кол-во на 1 удиницу товара")
    class Meta:
        verbose_name="Ингридиент для приготовляемых товаров"
        verbose_name_plural="Ингридиенты для приготовляемых товаров"    

class Roles(models.Model):
    choices=[
        (1,"Завсклад"),
        (2,"Кассир"),
        (3,"Закупщик"),
        (4,"Заготовщик"),
        (5,"Пиццемейкер"),
        (6,"Пиццедоставщик"),
        (7,"Пиццекассир")
    ]
    profile=models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="Работник")
    place = models.ForeignKey(Pizzerias,on_delete=models.CASCADE,verbose_name="Пиццерия",null=True,blank=True)
    role = models.IntegerField(blank=True,verbose_name="Роль",choices=choices,null=True)
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

###################
