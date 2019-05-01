from django.db import models
from django.contrib.auth.models import User
#импорты для изменения данных одновременно с юзер
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
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
    objects=models.Manager()
    artikul=models.CharField(verbose_name="Артикул",max_length=6,default="",editable=False)
    name=models.CharField(verbose_name="Название товара",max_length=100)
    image=models.ImageField(verbose_name="Изображение")
    edizm=models.ForeignKey(Units,on_delete=models.PROTECT,verbose_name="Ед.измерения",null=True)
    rashod=models.IntegerField(verbose_name="Ср.расход в день",default=1)
    #ostat=models.IntegerField(verbose_name="Остаток на дни",default=kolvo/rashod,editable=False)
    maks_zakup=models.IntegerField(verbose_name="Закупка на дни",default=1)
    min_zakup=models.IntegerField(verbose_name="Миним.дни для закупки",default=1)
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
    pos1=models.Manager()
    firm_name=models.CharField(max_length=50,verbose_name="Фирма-поставщик",default="")
    name=models.CharField(max_length=20,verbose_name="Контактное лицо",default="")
    contact=models.CharField(max_length=50,verbose_name="Контактные данные",default="")
    place=models.TextField(verbose_name="Расположение",default="")
    class Meta:
        verbose_name="Поставщик"
        verbose_name_plural="Поставщики"

class Codes(models.Model):
    objects=models.Manager()
    name=models.ForeignKey(Products,on_delete=models.PROTECT,verbose_name="Товар",null=True)
    shtrih=models.CharField(verbose_name="Штрих-код",editable=False,max_length=50,default="")
    kolvo=models.FloatField(verbose_name="Кол-во",default=0.0)
    def save(self,*args,**kwargs):
        name=self.name.name
        d=datetime.datetime.strftime(datetime.datetime.now(),"%d%m%Y")
        i=str(self.name.id).zfill(3)
        sh=str(i)+str(d)
        self.shtrih=sh
        self.kolvo=round(self.kolvo,3)
        super(Codes,self).save(*args,**kwargs)
    class Meta:
        verbose_name="Штрих код"
        verbose_name_plural="Штрих коды"    

class CustomDelete(models.QuerySet):
    def delete(self,*args,**kwargs):
        for obj in self:
            if obj.ostat==0.0:
                obj.delete()

class Stock(models.Model):
    objects=CustomDelete.as_manager()
    name=models.OneToOneField(Products,on_delete=models.PROTECT,verbose_name="Товар",null=True)
    kolvo=models.FloatField(verbose_name="Кол-во")
    summ=models.FloatField(verbose_name="Сумма",default=0.0)
    ostat=models.FloatField(verbose_name="Осталось на складе",default=0.0,editable=False)
    def save(self,*args,**kwargs):
        self.kolvo=round(self.kolvo,3)
        self.ostat=round(self.ostat,3)
        self.ostat+=self.kolvo
        self.ostat=round(self.ostat,3)
        super(Stock,self).save(*args,**kwargs)
    def delete(self,*args,**kwargs):
        if self.ostat==0.0:
            super(Stock,self).delete(*args,**kwargs)
    def __str__(self):
        return self.name.name
    class Meta:
        verbose_name=" На склад"
        verbose_name_plural="Склад"

class Purchase(models.Model):
    objects=models.Manager()
    nak_id=models.IntegerField(verbose_name="Номер накладной")
    name=models.ForeignKey(Products,on_delete=models.PROTECT,verbose_name="Товар")
    last_cost=models.FloatField(verbose_name="Последняя цена")
    kolvo=models.FloatField(verbose_name="Требуемое кол-во")
    min_srok=models.DateField(verbose_name="Мин.срок годности",null=True)
    is_accepted=models.BooleanField(verbose_name="Накладная принята?",default=False)
    purchased_kol=models.FloatField(verbose_name="Купленное кол-во",default=0.0)
    new_cost=models.FloatField(verbose_name="Цена",default=0.0)
    summ=models.FloatField(verbose_name="Сумма",default=0.0)
    fact_kol=models.FloatField(verbose_name="Фактическое кол-во",default=0.0)
    srok=models.DateField(verbose_name="Cрок годности",null=True)
    is_delivered=models.BooleanField(verbose_name="Поступил на склад?",default=False)
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
    nak_id=models.ForeignKey(Purchase,on_delete=models.PROTECT,verbose_name="Номер накладной")
    dop_type=models.ForeignKey(Dop_types,on_delete=models.PROTECT,verbose_name="Тип расхода")
    money=models.IntegerField(verbose_name="Сумма")
    class Meta:
        verbose_name="Дополнительные расходы"
        verbose_name_plural="Дополнительные расходы"
    
class Nakl_for_zagot(models.Model):
    name=models.ForeignKey(Products,on_delete=models.PROTECT,limit_choices_to={"prigot":True},verbose_name="Товар")
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

class Receivers(models.Model):
    objects=models.Manager()
    receiver=models.CharField(max_length=100,verbose_name="Объект списания")
    def __str__(self):
        return self.receiver
    class Meta:
        verbose_name="Отгрузка"
        verbose_name_plural="Отгрузка"

class Spis(models.Model):
    objects=models.Manager()
    nak_id=models.AutoField(primary_key=True,verbose_name="ID накладной")
    product=models.CharField(max_length=100,verbose_name="Что")
    receiver=models.ForeignKey(Receivers,on_delete=models.PROTECT,verbose_name="Кому")
    kol=models.IntegerField(verbose_name="Сколько")
    class Meta:
        verbose_name="Накладная на списание"
        verbose_name_plural="Накладные на списание"


class Ingredients(models.Model):
    objects=models.Manager()
    product=models.ForeignKey(Products,related_name="product",limit_choices_to={"prigot":True},on_delete=models.PROTECT,verbose_name="Заготовляемый товар")
    ingr=models.ForeignKey(Products,related_name="ingr",on_delete=models.PROTECT,verbose_name="Ингридиент")
    kolvo=models.IntegerField(verbose_name="Кол-во на 1 удиницу товара")
    class Meta:
        verbose_name="Ингридиент для приготовляемых товаров"
        verbose_name_plural="Ингридиенты для приготовляемых товаров"    

class LastCost(models.Model):
    objects=models.Manager()
    product=models.ForeignKey(Products,on_delete=models.PROTECT,verbose_name="Продукт")
    cost=models.FloatField(verbose_name="Последняя цена",default=0.0)
    def save(self,*args,**kwargs):
        self.cost=round(self.kolvo,3)
        super(LastCost,self).save(*args,**kwargs)


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
    user = models.OneToOneField(User, on_delete=models.PROTECT,verbose_name="Работник")
    place = models.ForeignKey(Pizzerias,on_delete=models.PROTECT,verbose_name="Пиццерия",null=True,blank=True)
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

