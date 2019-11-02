import django_tables2 as tables
from .models import *

class StockTable(tables.Table):
    class Meta:
        model = Stock
        template_name = 'django_tables2/bootstrap.html'

class NaklTable(tables.Table):
    class Meta:
        model=Purchase
        template_name = 'django_tables2/bootstrap.html'

class NaklTable2(tables.Table):
    class Meta:
        model=Nakl_for_zagot
        template_name = 'django_tables2/bootstrap.html'

class ZakupTable(tables.Table):
    nak_id=tables.Column()
    name=tables.Column()
    kolvo=tables.Column()
    last_cost=tables.Column()
    purchased_kol=tables.Column()
    new_cost=tables.Column()
    summ=tables.Column()
    class Meta:
        model=Purchase
        template_name = 'django_tables2/bootstrap.html'

class ZagotTable(tables.Table):
    id=tables.Column()
    name=tables.Column()
    tkolvo=tables.Column()
    class Meta:
        model = Nakl_for_zagot
        template_name = 'django_tables2/bootstrap.html'