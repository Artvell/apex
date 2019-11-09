"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login,logout
from roles import views
from roles.admin import admin_site


admin.site.site_header="Администрирование системы Apex"

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('django.contrib.auth.urls')),
    path('accounts/profile/',views.profile),
    path('about_product/',views.product_name),
    path('accounts/profile/info',views.info),
    path('accounts/profile/info/naklad',views.info_naklad),
    path('accounts/profile/info/products',views.info_products),
    path('accounts/profile/naklad',views.list_naklad),
    path('accounts/profile/select',views.choose_type),
    path('accounts/profile/sorted',views.sorted_products),
    path('accounts/profile/zakup/nak_id',views.get_products),
    path('accounts/profile/zagot/nak_id',views.get_products),
    path('accounts/profile/zakup/reset',views.reset_nak_id),
    path('accounts/profile/zagot/reset',views.reset_nak_id),
    path('accounts/profile/codes_table',views.table_of_barcodes),
    path('accounts/profile/printing_barcodes/',views.printing_barcodes),
    path('accounts/profile/spis/',views.spis),
    path('accounts/profile/spis/zagot/',views.spis_zagot),
    path('accounts/profile/spis/zagot/create_nakl/',views.spis_create_nakl),
    path('accounts/profile/nakl_order/',views.nakl_order),
    path('accounts/profile/nakl_orders/',views.nakl_orders),
    path('accounts/profile/new_product/',views.append_product_for_saler),
    path('accounts/profile/new_saler',views.append_saler),
    path('accounts/profile/zakup/get_products',views.get_products),
    path('accounts/profile/zagot/get_products',views.get_products),
    path('accounts/profile/zakup/get_product',views.get_product),
    path('accounts/profile/zagot/get_product',views.get_product),
    path('accounts/profile/zakup/return_product',views.return_product),
    path('accounts/profile/zagot/return_product',views.return_product),
    path('accounts/profile/returned/zakup',views.returned_list),
    path('accounts/profile/returned/zagot',views.returned_list),
    path('accounts/profile/returned/sklad',views.returned_list),
    path('accounts/profile/zagot/get_barcode',views.get_barcode),
    path('accounts/profile/buy_products/',views.buy_products),
    path('accounts/profile/unrealized',views.unrealized),
    path('accounts/profile/zakup/accept',views.accept_products),
    path('accounts/profile/zagot/accept_products',views.accept_zagot_products),
    path('accounts/profile/buy_product',views.buy_product),
    path('accounts/profile/buy_products/add_product',views.add_product),
    path('accounts/profile/buy_products/ordered_products',views.ordered_list),
    path('accounts/profile/buy_products/table',views.ordered_table),
    path('accounts/profile/buy_products/dop_types/',views.add_dop_money_for_purchase),
    path('accounts/profile/buy_more_products',views.buy_more_products),
    path('accounts/profile/choose',views.choose_naklad),
    path('accounts/profile/accept',views.accept_naklad),
    path('accounts/profile/accepted',views.accepted_naklad),
    path('accounts/profile/converter',views.converter),
    path('accounts/profile/give_money/zakup',views.give_money_zakup),
    path('accounts/profile/give_money/other',views.give_money_other),
    path('accounts/profile/product/',views.zagot_product),
    path('accounts/profile/zagot/accept/',views.accept_zagot),
    path('accounts/profile/zagot/list/',views.zagot_list),
    path('accounts/profile/select_receiver/',views.select_receiver),
    path('accounts/profile/take_money/',views.take_money)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
