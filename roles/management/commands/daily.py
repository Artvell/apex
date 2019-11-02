from django.core.management.base import BaseCommand, CommandError
from roles.models import Daily_Consumption,Products_Consumption,Products
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
class Command(BaseCommand):
    help="Закрывает день"
    def handle(self,*args,**kwargs):
        daily=Daily_Consumption.objects.all()
        for d in daily:
            try:
                total=Products_Consumption.objects.get(name=d.name)
                consumption=total.consumption
                if len(consumption)<total.days:
                    consumption.append(round(float(d.consumption),3))
                    total.day+=1
                    total.save()
                    total_consumpt=round(sum(total.consumption)/len(consumption),3)
                else:
                    consumption[total.day%total.days-1]=round(float(d.consumption),3)
                    total.day+=1
                    total.save()
                    total_consumpt=round(sum(total.consumption)/total.days,3)
            except ObjectDoesNotExist:
                Products_Consumption(name=d.name,days=30,day=2,consumption=[round(float(d.consumption),3)]).save()
                total_consumpt=round(float(d.consumption),3)
            finally:
                d.name.rashod=total_consumpt
                d.name.save()
        daily.update(consumption=0.0)


