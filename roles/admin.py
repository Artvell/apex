from django.contrib import admin
from roles.models import *
from django.contrib.admin import AdminSite
from django.urls import path,re_path
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .views import admin_view,add_ingr,edit_ingr,delete_ingr,admin_view_3
# Register your models here.

class DontLog:
    def log_deletion(self, *args):
        return


class MyAdminSite(AdminSite):
    def get_urls(self):
        urls=super(MyAdminSite,self).get_urls()
        #print(urls)
        custom_urls=[
            re_path(r"roles/ingredients/add/",self.admin_view(add_ingr)),
            re_path(r"roles/ingredients/edit/",self.admin_view(edit_ingr)),
            re_path(r"roles/ingredients/delete/",self.admin_view(delete_ingr)),
            path("roles/ingredients/",self.admin_view(admin_view)),
            #path("roles/salers/",self.admin_view(admin_view_3))
            #re_path(r"roles/ingredients/next/",self.admin_view)
        ]
        return custom_urls+urls

admin_site=MyAdminSite()

#class MyUserAdmin(UserAdmin):

class StockAdmin(DontLog,admin.ModelAdmin):
    list_display=("name","ostat",)
class RolesAdmin(admin.ModelAdmin):
    list_display=("user",'place','role')

class PizAdmin(admin.ModelAdmin):
    list_display=("id","name")

class ProductAdmin(admin.ModelAdmin):
    list_display=("id","name","rashod","maks_zakup","min_zakup","edizm","prigot")

class UnitAdmin(admin.ModelAdmin):
    list_display=("edizm","opis")

class PostavshAdmin(admin.ModelAdmin):
    list_display=("firm_name","name","contact","place")

class IngrAdmin(admin.ModelAdmin):
    list_display=("product","ingr","kolvo")

class PurchaseAdmin(admin.ModelAdmin):
    list_display=("nak_id","name","last_cost","kolvo","is_accepted","purchased_kol","new_cost","summ","fact_kol","min_srok","srok","is_delivered")

class MoneyAdmin(admin.ModelAdmin):
    list_display=("nak_id","dat","nsumma","dsumma","isumma","psumma","rsumma","vsumma","is_calculated")

class NaklAdmin(admin.ModelAdmin):
    list_display=("nak_id","user","name","tkolvo","is_accepted","pkolvo","price","summ","is_maked","ac_kolvo","srok","shtrih","in_stock")

class Nakl_rash_admin(admin.ModelAdmin):
    list_display=("nak_id","name","kol")

class Dop_types_Admin(admin.ModelAdmin):
    list_display=("name","min_summ","max_summ")

class Dop_money_Admin(admin.ModelAdmin):
    list_display=("nak_id","dop_type","money","purchaser")

class SpisAdmin(admin.ModelAdmin):
    list_display=("nak_id","product","receiver","kol")

class RecAdmin(admin.ModelAdmin):
    list_display=("id","receiver")

class CodesAdmin(admin.ModelAdmin):
    list_display=("name","shtrih","kolvo")

class ZakupshikiAdmin(admin.ModelAdmin):
    list_display=("name","user")

class SalersAdmin(admin.ModelAdmin):
    list_display=("saler","product","last_cost")

class UserAdmin(admin.ModelAdmin):
    list_display=("username","first_name","is_superuser")

class CostAdmin(admin.ModelAdmin):
    list_display=("product","cost")

class Money_zakup_Admin(admin.ModelAdmin):
    list_display=("name","types","kolvo")

class Money_other_Admin(admin.ModelAdmin):
    list_display=("name","types","kolvo")

class Money_Admin(admin.ModelAdmin):
    list_display=("types","kolvo")

class Types_of_money_Admin(admin.ModelAdmin):
    list_display=("types",)

class Zagot_types_Admin(admin.ModelAdmin):
    list_display=("product","user")

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id","category")

class Zagot_products_Admin(admin.ModelAdmin):
    list_display=("nak_id","product","user","kol","kolvo","status")

class Harvester_Stock_Admin(admin.ModelAdmin):
    list_display=("user","product","kol")

class Harvester_Barcodes_Admin(admin.ModelAdmin):
    list_display=("nak_id","product_id","barcode","date")

class Balans_Admin(admin.ModelAdmin):
    list_display=("buyer","balans","debt")

class ConsumptionAdmin(admin.ModelAdmin):
    list_display=("name","consumption","days")

class Daily_Consumption_Admin(admin.ModelAdmin):
    list_display=("name","consumption")

class PrintersAdmin(admin.ModelAdmin):
    list_display=("id","name","ip_address")

class RediscountAdmin(admin.ModelAdmin):
    list_display=('red_id',"name",'kol')

class Rediscount_info_Admin(admin.ModelAdmin):
    list_display=("rediscount","progress","date")


class Rec_money_Admin(admin.ModelAdmin):
    list_display=("types","kolvo","date")
#admin_site.unregister(User)

'''@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ['-pk']'''

admin_site.register(Roles,RolesAdmin)
admin_site.register(Stock,StockAdmin)
admin_site.register(Products,ProductAdmin)
admin_site.register(Units,UnitAdmin)
#admin_site.register(Pizzerias,PizAdmin)
admin_site.register(Ingredients,IngrAdmin)
admin_site.register(Postavsh,PostavshAdmin)
admin_site.register(Purchase,PurchaseAdmin)
#admin_site.register(Money,MoneyAdmin)
admin_site.register(Nakl_for_zagot,NaklAdmin)
admin_site.register(DopTypes,Dop_types_Admin)
admin_site.register(DopMoney,Dop_money_Admin)
admin_site.register(Spis,SpisAdmin)
admin_site.register(Receivers,RecAdmin)
admin_site.register(Codes,CodesAdmin)
admin_site.register(Rashod_zagot,Nakl_rash_admin)
admin_site.register(Zakupshiki,ZakupshikiAdmin)
admin_site.register(Salers,SalersAdmin)
admin_site.register(User,UserAdmin)
admin_site.register(LastCost,CostAdmin)
admin_site.register(Nakl_money_zakup,Money_zakup_Admin)
admin_site.register(Nakl_money_other,Money_other_Admin)
admin_site.register(Moneys,Money_Admin)
admin_site.register(Types_of_money,Types_of_money_Admin)
admin_site.register(Zagot_types,Zagot_types_Admin)
admin_site.register(Categories,CategoryAdmin)
admin_site.register(Zagot_products,Zagot_products_Admin)
admin_site.register(Harvester_Stock,Harvester_Stock_Admin)
admin_site.register(Buyer_Balans,Balans_Admin)
admin_site.register(Products_Consumption,ConsumptionAdmin)
admin_site.register(Daily_Consumption,Daily_Consumption_Admin)
admin_site.register(Harvester_Barcodes,Harvester_Barcodes_Admin)
admin_site.register(Printers,PrintersAdmin)
admin_site.register(Rediscount,RediscountAdmin)
admin_site.register(Rediscount_info,Rediscount_info_Admin)
admin_site.register(Receiving_Money,Rec_money_Admin)