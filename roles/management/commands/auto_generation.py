# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from roles.models import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
class Command(BaseCommand):
    help="Генерирует накладные"
    def handle(self,*args,**kwargs):
        products=Products.objects.filter(prigot=False)
        try:
            last_id=max([int(pur.nak_id) for pur in Purchase.objects.all()])
        except ValueError:
            last_id=0
        for product in products:
            #print(product.name)
            try:
                in_stock=Stock.objects.get(name=product)
                kol=in_stock.ostat
            except ObjectDoesNotExist:
                kol=0.0
            if float(product.rashod)==0.0:
                continue
            if float(kol)/float(product.rashod)<=float(product.min_zakup):
                needs=product.maks_zakup*product.rashod-kol
                needs=round(needs)
                if needs==0.0:
                    continue
                days=round(needs/product.rashod)
                now=datetime.today()
                srok=now+timedelta(days=days)
                self.stdout.write(product.name+"  "+str(needs)+" | "+srok.strftime("%Y-%m-%d"))
                try:
                    last_cost=LastCost.objects.get(product=product).cost
                except ObjectDoesNotExist:
                    last_cost=0.0
                Purchase(nak_id=last_id+1,name=product,kolvo=needs,min_srok=srok,last_cost=last_cost,date=datetime.now().date().strftime("%Y-%m-%d"),fact_kol=0.0).save()