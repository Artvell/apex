from django.contrib import admin
from roles.models import *
# Register your models here.

class DontLog:
    def log_deletion(self, *args):
        return

class StockAdmin(DontLog,admin.ModelAdmin):
    list_display=("name","kolvo","summ","ostat")
class RolesAdmin(admin.ModelAdmin):
    list_display=("user",'place','role')

class PizAdmin(admin.ModelAdmin):
    list_display=("id","name")

class ProductAdmin(admin.ModelAdmin):
    list_display=("id","name","scena","rashod","maks_zakup","min_zakup","edizm","prigot")

class UnitAdmin(admin.ModelAdmin):
    list_display=("edizm","opis")

class PostavshAdmin(admin.ModelAdmin):
    list_display=("firm_name","name","contact","place")

class IngrAdmin(admin.ModelAdmin):
    list_display=("product","ingr","kolvo")

class PurchaseAdmin(admin.ModelAdmin):
    list_display=("nak_id","name","last_cost","kolvo","min_srok","is_accepted","purchased_kol","new_cost","summ","fact_kol","srok","shtrih","is_delivered")

class MoneyAdmin(admin.ModelAdmin):
    list_display=("nak_id","dat","nsumma","dsumma","isumma","psumma","rsumma","vsumma","is_calculated")

class NaklAdmin(admin.ModelAdmin):
    list_display=("name","tkolvo","is_accepted","pkolvo","price","summ","is_maked","ac_kolvo","srok","shtrih","in_stock")

class Dop_types_Admin(admin.ModelAdmin):
    list_display=("name","min_summ","max_summ")

class Dop_money_Admin(admin.ModelAdmin):
    list_display=("nak_id","dop_type","money")

admin.site.register(Roles,RolesAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Units,UnitAdmin)
admin.site.register(Pizzerias,PizAdmin)
admin.site.register(Ingredients,IngrAdmin)
admin.site.register(Postavsh,PostavshAdmin)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Money,MoneyAdmin)
admin.site.register(Nakl_for_zagot,NaklAdmin)
admin.site.register(Dop_types,Dop_types_Admin)
admin.site.register(Dop_money,Dop_money_Admin)