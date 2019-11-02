# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from roles.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
class Command(BaseCommand):
    help="Генерирует накладные для заготовщика"
    def handle(self,*args,**kwargs):
        products=Products.objects.filter(prigot=True)
        try:
            last_id=max([int(pur.nak_id) for pur in Nakl_for_zagot.objects.all()])
        except ValueError:
            last_id=0
        for product in products:
            #print(product.name)
            try:
                in_stock=Stock.objects.get(name=product)
                kol=in_stock.ostat
            except ObjectDoesNotExist:
                kol=0.0
            if float(kol)/float(product.rashod)<=float(product.min_zakup):
                needs=product.maks_zakup*product.rashod-kol
                needs=round(needs)
                days=round(needs/product.rashod)
                now=datetime.today()
                srok=now+timedelta(days=days)
                #self.stdout.write(product.name+"  "+str(needs)+" | ")
                try:
                    #self.stdout.write(str(product))
                    zagot=Zagot_types.objects.filter(product=product)
                    if len(zagot)!=0:
                     Nakl_for_zagot(nak_id=last_id+1,name=product,user=zagot[0],tkolvo=needs).save()#user=User.objects.get(id=21)))#.save()
                    else:
                        continue
                except ObjectDoesNotExist:
                    continue