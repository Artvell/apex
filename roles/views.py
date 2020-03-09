# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.http import Http404
from .models import *
from .tables import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django_tables2 import RequestConfig
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import datetime as d
from datetime import datetime,timedelta,timezone
from escpos.printer import Network
import requests
import barcode
from barcode.writer import ImageWriter
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError

from pyzbar.pyzbar import decode
from PIL import Image
import xlwt

def generate_barcode(pid,date):
    i=str(pid).zfill(4)
    d=datetime.strftime(date,"%d%m%Y")
    sh=str(i)+str(d)
    return sh

def print_barcode(product,d,barcod,prim,edizm): #печать чеков у заготовщика при приготовлении товара
    try:
        ip=Printers.objects.get(id=2).ip_address
        print("ip1=",ip)
        code = Network(ip)
        d=datetime.strftime(d,r"%d-%m-%Y")
        try:
            product=translit(product,reversed=True)
        except LanguageDetectionError:
            product=product
        try:
            edizm=translit(edizm,reversed=True)
        except LanguageDetectionError:
            edizm=edizm
        code.set(align="center")
        code.text("---------- \n")
        code.text(" \n")
        code.text(f"{product}\nProizvedeno: {d}\n{edizm}:{prim}\n")
        code.barcode(barcod, 'EAN13',48, 2,align_ct=False)
        #code.text(" \n")
        code.text("__________ \n")

    except Exception as e:
        print(e)
    #code.cut()

def print_barcode_2(product,d,barcod,prim,edizm): #печать чеков на складе (от закупщика)
    try:
        ip=Printers.objects.get(id=1).ip_address
        print("ip1=",ip)
        code = Network(ip)
        d=datetime.strftime(d,r"%d-%m-%Y")
        try:
            product=translit(product,reversed=True)
        except LanguageDetectionError:
            product=product
        try:
            edizm=translit(edizm,reversed=True)
        except LanguageDetectionError:
            edizm=edizm
        code.set(align="center")
        code.text("-------- \n")
        code.text(" \n")
        code.text(f"{product}\nProizvedeno: {d}\n{edizm}:{prim}\n")
        code.barcode(barcod, 'EAN13',42, 2,align_ct=False)
        #code.text(" \n")
        code.text("________ \n")
    except Exception as e:
        print(e)
    #code.cut()

def trash(): # пустой чек для закупщика
    print("here")
    try:
        ip=Printers.objects.get(id=1).ip_address
        code = Network(ip)
        code.set(align="center")
        #code.cut()
        code.text(" \n")
        code.text(" \n")
        #code.text(" \n")
        code.text(" \n")
        code.barcode("000000000000", 'EAN13',50, 2,align_ct=False)
        code.text(" \n")
        code.text(" \n")
    except Exception as e:
        print(e)

def trash2(): # пустой чек для заготовщика
    print("here")
    try:
        ip=Printers.objects.get(id=2).ip_address
        code = Network(ip)
        code.set(align="center")
        code.text(" \n")
        code.text(" \n")
        #code.text(" \n")
        code.text(" \n")
        code.barcode("000000000000", 'EAN13',48, 2,align_ct=False)
        code.text(" \n")
        code.text(" \n")
    except Exception as e:
        print(e)



#    ip=Printers.objects.get(id=2).ip_address
#    code = Network(ip)

#    code = Network("192.168.100.218")
#    code.set(align="center")

def draw_barcode(barcod):
    EAN = barcode.get_barcode_class('ean')
    ean=EAN(barcod,writer=ImageWriter())
    fullname = ean.save('ean13_barcode')
    return fullname

def create_xls_search_results(f,result):
    try:
        book = xlwt.Workbook('utf8')
        sheet = book.add_sheet('results')
        sheet.write(0,0,'№ накладной')
        sheet.write(0,1,'Продукт')
        sheet.write(0,2,'Кол-во')
        if f==1:
            sheet.write(0,3,'Закупщик')
        elif f==2:
            sheet.write(0,3,"Кому списано")
        sheet.write(0,4,'Дата')
        i=1
        if f==1:
            for r in result:
                print(r.name.name)
                sheet.write(i,0,r.nak_id)
                sheet.write(i,1,r.name.name)
                sheet.write(i,2,r.fact_kol)
                sheet.write(i,3,r.purchase.username)
                sheet.write(i,4,datetime.strftime(r.date,"%d-%m-%Y"))
                i+=1
            book.save("media/prihod.xls")
            print("ok")
        elif f==2:
            for r in result:
                sheet.write(i,0,r.nak_id)
                sheet.write(i,1,r.product_name)
                sheet.write(i,2,r.kol)
                sheet.write(i,3,r.receiver.receiver)
                sheet.write(i,4,datetime.strftime(r.date,"%d-%m-%Y"))
                i+=1
            book.save("media/spis.xls")
        print(len(result))
    except Exception as e:
        print(e)

def create_xls_rediscount(result,date,average,summ,plus,minus):
    try:
        book = xlwt.Workbook('utf8')
        sheet = book.add_sheet("rediscount")
        sheet.write(0,0,datetime.strftime(date,"%d-%m-%Y"))
        sheet.write(1,0,'Продукт')
        sheet.write(1,1,'Кол-во на складе')
        sheet.write(1,2,'Ср.цена')
        sheet.write(1,3,'Сумма')
        sheet.write(1,4,'+')
        sheet.write(1,5,'-')
        i=2
        ind=0
        for r in result:
            sheet.write(i,0,r.name.name)
            sheet.write(i,1,r.st_kol)
            sheet.write(i,2,average[ind])
            sheet.write(i,3,summ[ind])
            sheet.write(i,4,plus[ind])
            sheet.write(i,5,minus[ind])
            i+=1
            ind+=1
        book.save(f'media/rediscount_{datetime.strftime(date,"%d-%m-%Y")}.xls')
    except Exception as e:
        print(e)



roles={
    1:"sklad.html",
    2:"kassir.html",
    3:"zakup.html",
    4:"zagotov.html",
    5:"pizzamaker.html",
    6:"dostavka.html",
    7:"pizzakassir.html",
    8:"admin.html"
}

# Create your views here.
@login_required
def profile(request):
    n=request.user.first_name
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    url=request.get_full_path().split("/")
    print(url)
    if j==1 or (url[3]=="sklad" and j==8):
        print("!!!!!!!!")
        table=StockTable(Stock.objects.all())
        RequestConfig(request).configure(table)
        nak_id=int(Nakl_for_zagot.objects.all()[len(Nakl_for_zagot.objects.all())-1].nak_id)
        print(nak_id)
        not_given=Nakl_for_zagot.objects.filter(Q(nak_id=68)&Q(is_given=False))
        rediscounts=Rediscount_info.objects.filter(is_closed=True).order_by('rediscount__red_id')
        spis_nakl=Spis.objects.filter(is_removed=False).order_by('nak_id')
        n=spis_nakl.last().nak_id
        if rediscounts.count()==0:
            r_id=1
        else:
            last_rediscount=rediscounts.last()
            r_id=last_rediscount.rediscount.red_id+1
        if len(not_given)==0:
            return render(request,roles[1],{"user":n,"job":job,"table":table,"id":r_id,"n":n})
        else:
            return render(request,roles[1],{"indic":1,"nak_id":nak_id,"user":n,"job":job,"table":table,"id":r_id,"n":n})
    elif j==3 or (url[3]=="zakup" and j==8):
        if request.method!="POST":
            form=Zakup(Purchase.objects.filter(is_accepted_zakup=True))
            products=Purchase.objects.filter(is_accepted_zakup=False)
            print("!!!",len(products))
            indic=0
            ppurch=Purchase.objects.filter(Q(purchased_kol=0.0)&Q(is_accepted_zakup=True))
            int_ppurch=[int(pp.nak_id) for pp in ppurch]
            max_nakl=max(int_ppurch)
            print("*****",max_nakl)
            purch=Purchase.objects.filter(Q(purchased_kol=0.0)&Q(is_accepted_zakup=True)&Q(nak_id=str(max_nakl)))
            print([p.nak_id for p in purch])
            cost=0.0
            print(purch)
            for pur in purch:
                cost+=round((float(pur.last_cost)*pur.kolvo),3)
            cost=round(cost,3)
            print("#########",cost)
            all_money=Nakl_money_zakup.objects.filter(Q(name__username=request.user.username)&Q(types__types="Наличные"))
            money=0.0
            for m in all_money:
                money+=m.kolvo
            money=round(money,3)
            b=Buyer_Balans.objects.get(buyer__username=request.user.username)
            balans=round(b.balans,3)
            not_accepted=Purchase.objects.filter(Q(is_accepted=False)&Q(purchased_kol__gt=0.0)&Q(is_borrowed=False))
            debt=round(b.debt,3)
            unrealized=Purchase.objects.filter(Q(is_accepted_zakup=True)&Q(purchased_kol=0.0)&Q(is_borrowed=False))
            unrealized_uniq=[]
            unrealized_uniq_id=[]
            for u in unrealized:
                if u.nak_id not in unrealized_uniq_id:
                    unrealized_uniq_id.append(u.nak_id)
                    unrealized_uniq.append(u)
            if len(products)!=0:
                idd=products[0].nak_id
                indic=1
                return render(request,"zakup.html",{"indic":indic,"job":job,"form":form,"id":idd,"cost":cost,"all":money,"balans":balans,"debt":debt,"unrealized":unrealized_uniq})
            else:
                return render(request,"zakup.html",{"indic":indic,"job":job,"form":form,"cost":cost,"all":money,"balans":balans,"debt":debt,"unrealized":unrealized_uniq})
    elif j==4 or (url[3]=="zagot" and j==8):
        j=request.user.roles.role
        products=Nakl_for_zagot.objects.filter(is_accepted=False)
        accepted=Nakl_for_zagot.objects.filter(is_accepted=True)
        if len(accepted)!=0:
            form=Zagot(accepted)
        else:
            form=None
        zagot_nakls=Nakl_for_zagot.objects.filter(Q(is_accepted=True)&Q(user__user=request.user))
        #zagot_nakls=Nakl_for_zagot.objects.filter(Q(is_accepted=True))
        l_id=[int(n.nak_id) for n in zagot_nakls]
        try:
            last_id=max(l_id)
        except ValueError:
            last_id=0
        given_products=Nakl_for_zagot.objects.filter(Q(is_accepted=True)&Q(nak_id=last_id)&Q(is_given=True)&Q(is_taken=False)&Q(user__user=request.user))
        print("!!!",given_products)
        if len(given_products)>0:
            f=1
        else:
            f=0
        if len(products)>0:
            indic=1
        else:
            indic=0
        w=Without_nakl.objects.filter(is_accepted=False)
        if w.count()!=0:
            w_nak_id=w.last().nak_id
        else:
            w=Without_nakl.objects.filter(is_accepted=True)
            w_nak_id=int(w.last().nak_id)+1
        return render(request,roles[4],{"job":job,"form":form,"indic":indic,"f":f,"last_id":last_id,"nak_id":w_nak_id})
    elif j==2 or (url[3]=="kassir" and j==8):
        abs_nakl=Purchase.objects.all()
        nakl=Purchase.objects.filter(Q(is_accepted=False)&Q(is_delivered=True))
        nakl_money=Nakl_money_zakup.objects.filter(types__types="Наличные")
        nakl_money_other=Nakl_money_other.objects.all()
        nakl_closed=Purchase.objects.filter(Q(is_accepted=True)&Q(is_delivered=True))
        table=NaklTable(abs_nakl)
        all_nak=[]
        for nak in abs_nakl:
            if nak.nak_id not in all_nak:
                all_nak.append(nak.nak_id)
        not_accepted=[]
        for n in nakl:
            if n.nak_id not in not_accepted:
                not_accepted.append(n.nak_id)
        all_n=len(all_nak)
        accepted=len(all_nak)
        not_acc=len(not_accepted)
        for k in not_accepted:
            if k in all_nak:
                accepted-=1
        other=all_n-accepted
        money=0.0
        money2={t.types:0.0 for t in Types_of_money.objects.all()}
        closed=0.0
        print(money2)
        for nak in nakl_money:
            money+=nak.kolvo
        print(money2)
        for n in nakl_money_other:
            print(money2)
            print(money2[n.types.types],type(money2[n.types.types]))
            money2[n.types.types]+=n.kolvo
            #money2[n.types.types]=format(money2[n.types.types],".3f")
        for p in nakl_closed:
            closed+=p.summ
        money=format(money,".3f")
        print("@@@@@ ",money2)
        closed=format(closed,".3f")
        balans=Moneys.objects.all()
        return render(request,roles[2],{"all":all_n,"accepted":accepted,"other":other,"money":money,"money2":money2,"closed":closed,"job":job,"balans":balans})
    elif j==8:
        stock=Stock.objects.all()
        product_summ=0
        product_debt=0
        for st in stock:
            try:
                c=LastCost.objects.get(product=st.name).average
                if c==0.0:
                    c=LastCost.objects.get(product=st.name).cost
                product_summ+=(st.ostat*c)
            except ObjectDoesNotExist:
                #product_summ+=(st.ostat*LastCost.objects.get(product=st.name).cost)
                continue
        debted=Purchase.objects.filter(is_borrowed=True)
        for d in debted:
            product_debt+=d.summ
        product_summ=round(product_summ,3)
        product_debt=round(product_debt,3)
        rediscount=Rediscount.objects.all().last()
        plus,minus=0,0
        for r in Rediscount.objects.filter(red_id=rediscount.red_id):
            if r.kol>0:
                plus+=1
            elif r.kol<0:
                minus+=1
        buyed=Purchase.objects.filter(Q(purchased_kol__gt=0)&Q(is_borrowed=False)&Q(is_ordered=False)&Q(is_delivered=True)).count()
        spis=Spis.objects.filter(is_removed=False).count()
        nakl_money_other=Nakl_money_other.objects.all()
        nakl_zakup=Nakl_money_zakup.objects.all()
        n1=0
        n2=0
        for n in nakl_money_other:
            n1+=n.kolvo
        for n in nakl_zakup:
            n2+=n.kolvo
        n1=round(n1,3)
        n2=round(n2,3)
        summ=round(n1+n2,3)
        rec=Receiving_Money.objects.all()
        rec_summ=0
        for r in rec:
            rec_summ+=r.kolvo
        rec_summ=round(rec_summ,3)
        money=Moneys.objects.all()
        nal=money[0].kolvo
        beznal=money[1].kolvo
        return render(request,"admin.html",{
            "product_summ":product_summ,
            "product_debt":product_debt,
            "rediscount":rediscount,
            "plus":plus,
            "minus":minus,
            "buyed":buyed,
            "spis":spis,
            "taken":rec_summ,
            "gaven":summ,
            "zak":n1,
            "oth":n2,
            "r_id":rediscount.red_id,
            "nal":nal,
            "beznal":beznal
            })
    else:
        return render(request,roles[j],{"user":n,"job":job})

@csrf_exempt
@login_required
def printing_barcodes(request):
    j=request.user.roles.role
    if j==1 or j==8:
        if request.method=="POST":
            barcod=request.POST.get("barcod")
            #kol,prim=request.POST.get("kol").split()
            kol=request.POST.get("kol")
            text=kol.split("/")
            if len(text)==1:
                kol=int(kol)
                com=""
            else:
                kol=int(text[0])
                com=text[1]
            #date=f"{barcod[-8:-6]}-{barcod[-6:-4]}-{barcod[-4:]}"
            #ddate=datetime.strptime(date,r"%d-%m-%Y").date()
            #print(ddate)
            #print(barcod)
            #print("$$$$$$$$$$$$$$$$",int(barcod[:-8]))
            product=Products.objects.get(id=int(barcod[:-8]))
            code = Codes.objects.get(shtrih=barcod)
            for i in range(kol):
                print_barcode_2(product.name,code.date,barcod,com,product.edizm.edizm)
            trash()
            return None
        else:
            return None
    elif j==4 or j==8:
        if request.method=="POST":
            barcod=request.POST.get("barcod")
            kol=int(request.POST.get("kol"))
            date=f"{barcod[-8:-6]}-{barcod[-6:-4]}-{barcod[-4:]}"
            ddate=datetime.strptime(date,r"%d-%m-%Y").date()
            product=Products.objects.get(id=int(barcod[:-8])).name
            for i in range(kol):
                print_barcode(product,"@",ddate,barcod)
            trash2()
            return None
        else:
            return None

@csrf_exempt
@login_required
def product_name(request):
    j=request.user.roles.role
    if j==1 or j==8:
        if request.method=="POST":
            barcode=request.POST.get('clickId')
            try:
                product=Products.objects.get(id=int(barcode[:3]))
                b=""
                f=0
                if len(barcode)==12:
                    code="0"+barcode[:-1]
                else:
                    code=barcode
                print(code)
                kol=Codes.objects.get(shtrih=code).kolvo
                ccodes=Codes.objects.filter(name=product)
                ccodes=[datetime.strptime(c.shtrih[-8:],r"%d%m%Y").date() for c in ccodes]
                if len(ccodes)>0:
                    barcode_date=datetime.strptime(code[-8:],r"%d%m%Y").date()
                    for cod in ccodes:
                        if cod<barcode_date:
                            f=1
                            b="Вы пытаетесь списать более позднюю партию."
                            break
                otv=f"{b}{product.name}({kol} {product.edizm.edizm})"
                return JsonResponse({"clickId":otv,'f':f})
            except ObjectDoesNotExist:
                return JsonResponse({"clickId":"Нет в базе! Проверьте штрих-код!"})



@login_required
def table_of_barcodes(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8:
        codes=Codes.objects.all()
        products=[c.name.name for c in codes]
        barcodes=[c.shtrih for c in codes]
        kolvo=[c.kolvo for c in codes]
        return render(request,"codes_table.html",{"range":range(len(codes)),"products":products,"codes":barcodes,"kolvo":kolvo})
    else:
        return redirect("/accounts/profile")


@login_required
def select_receiver(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        return render(request,"select_receiver.html")
    else:
        return redirect(".")

@login_required
def give_money_zakup(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        if request.method=="POST":
            name=request.POST.get("name")
            user=User.objects.get(username=name)
            money=request.POST.get("money")
            types=request.POST.get("type")
            money=round(float(money),3)
            m=Moneys.objects.get(types__types=types)
            if m.kolvo<money:
                return redirect("/accounts/profile/give_money/zakup?e=1")
            m.kolvo-=money
            m.save()
            t=Types_of_money.objects.get(types=types)
            date=datetime.now().date()
            Nakl_money_zakup(name=user,kolvo=money,types=t,date=date).save()
            try:
                b=Buyer_Balans.objects.get(buyer=user)
                b.balans+=money
                b.debt+=money
                b.save()
            except ObjectDoesNotExist:
                Buyer_Balans(buyer=user,balans=money,debt=money).save()
            return redirect("..")
        else:
            e=request.GET.get("e","!")
            money_receivers=User.objects.filter(roles__role=3)
            print(money_receivers)
            types=Moneys.objects.filter(kolvo__gt=0.0)
            form=KassirForm(money_receivers,types)
            if e=="1":
                return render(request,"give_money.html",{"indic":1,"form":form,"job":job})
            else:
                return render(request,"give_money.html",{"form":form,"job":job})

@login_required
def give_money_other(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        if request.method=="POST":
            name=request.POST.get("name")
            for_why=request.POST.get("for_why")
            money=request.POST.get("money")
            types=request.POST.get("type")
            m=Moneys.objects.get(types__types=types)
            m.kolvo-=round(float(money),3)
            m.save()
            t=Types_of_money.objects.get(types=types)
            date=datetime.now().date()
            Nakl_money_other(name=name,kolvo=round(float(money),3),for_why=for_why,types=t,date=date).save()
            return redirect("..")
        else:
            types=Moneys.objects.filter(kolvo__gt=0.0)
            form=KassirForm2(types)
            return render(request,"give_money.html",{"form":form,"job":job})

@login_required
def take_money(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        if request.method=="POST":
            types=request.POST.get("type")
            print("hhhhh ",type(types))
            kolvo=round(float(request.POST.get("kolvo")),3)
            print("KKK ",kolvo)
            t=Types_of_money.objects.get(types=types)
            try:
                m=Moneys.objects.get(types__types=types)
                m.kolvo+=kolvo
                m.save()
            except ObjectDoesNotExist:
                t=Types_of_money.objects.get(types=types)
                Moneys(types=t,kolvo=kolvo).save()
            Receiving_Money(kolvo=kolvo,types=t,date=datetime.now().date()).save()
            return redirect("/accounts/profile/")
        else:
            types=Types_of_money.objects.all()
            form=KassirTakeMoney(types)
            return render(request,"take_money.html",{"form":form})

@login_required
def choose_naklad(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        form=NaklForm2(Purchase.objects.filter(Q(is_accepted=False)&Q(is_delivered=True)))
        return render(request,"kassir_select_nakl.html",{"form":form})
    else:
        raise Http404

@login_required
def accept_naklad(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        if request.method=="POST":
            nak_id=request.POST.get("nak_id")
            products=Purchase.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=False)&Q(is_delivered=True)&Q(is_borrowed=False))
            cost=0.0
            print("PPP=",len(products))
            for p in products:
                cost+=(p.fact_kol*p.new_cost)
                #print("cost=",cost,p.fact_kol,p.new_cost,p.fact_kol*p.new_cost)
            dop_money=DopMoney.objects.filter(nak_id=nak_id)
            for d in dop_money:
                cost+=d.money
            cost=round(cost,3)
            return render(request,"kassir_accept_nakl.html",{"cost":cost,"nak_id":nak_id})
    else:
        return redirect("/accounts/profile")

@login_required
def accepted_naklad(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8 and request.method=="GET":
        nak_id=request.GET.get("nak_id")
        nakl=Purchase.objects.filter(Q(nak_id=nak_id)&Q(is_delivered=True)&Q(is_borrowed=False))
        summ=0.0
        for n in nakl:
            try:
                b=Buyer_Balans.objects.get(buyer=n.purchase)
                b.debt-=(n.fact_kol*n.new_cost)
                dop_money=DopMoney.objects.filter(Q(nak_id=nak_id)&Q(purchaser=n.purchase))
                for d in dop_money:
                    b.debt-=d.money
                b.debt=round(b.debt,3)
                b.save()
            except ObjectDoesNotExist:
                continue
        nakl.update(is_returned=False,is_accepted=True)
        return redirect("/accounts/profile/")
    else:
        return redirect("/accounts/profile/")


@login_required
def converter(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==2 or j==8:
        if request.method!="POST":
            money=Moneys.objects.all()
            e=request.GET.get("e","!")
            if e!="!":
                return render(request,"converter.html",{"indic":int(e),"money":money})
            else:
                return render(request,"converter.html",{"money":money})
        else:
            from_t=request.POST.get("from")
            to_t=request.POST.get("to")
            from_m=float(request.POST.get("from_m"))
            to_m=float(request.POST.get("to_m"))
            kolvo=float(request.POST.get("kolvo"))
            if from_t==to_t:
                return redirect("/accounts/profile/converter?e=1")
            else:
                fromm=Moneys.objects.get(types__types=from_t)
                too=Moneys.objects.get(types__types=to_t)
                kol=(kolvo/from_m)*to_m
                kol=round(kol,3)
                if fromm.kolvo<kolvo:
                    return redirect("/accounts/profile/converter?e=2")
                else:
                    fromm.kolvo-=kolvo
                    too.kolvo+=kol
                    fromm.save()
                    too.save()
                    return redirect("/accounts/profile")


@login_required
def list_naklad(request):
    id=request.user.id
    naklad=Purchase.objects.all()
    ch=[n.nak_id for n in naklad]
    ch=set(ch)
    naklad=sorted(ch)
    return render(request,"list_naklad.html",{"naklad":naklad})

@login_required
def get_products(request):
    if request.method=="POST":
        j=request.user.roles.role
        if j==1 or j==8:
            nak_id=request.POST.get("nak_id")
            print(nak_id)
            url=request.get_full_path().split("/")
            if url[3]=="zakup":
                request.session['_old_post_zakup'] = request.POST
                nak_id=request.POST.get("nak_id")
                products=Purchase.objects.filter(Q(nak_id=nak_id)&~Q(purchased_kol=0)&Q(is_returned=False))
                products1=[]
                for pr in products:
                    if pr.fact_kol==None:
                        pr.fact_kol=0.0
                    if pr.fact_kol>pr.purchased_kol:
                        continue
                    else:
                        products1.append(pr)
                return render(request,"get_products.html",{"indic":1,"products":products1})
            elif url[3]=="zagot":
                request.session['_old_post_zagot'] = request.POST
                nak_id=request.POST.get("nak_id")
                form=BarcodeForm()
                #products=Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)&~Q(pkolvo=0))
                return render(request,"get_products.html",{"indic":0,"form":form})
        else:
            raise Http404
    else:
        j=request.user.roles.role
        url=request.get_full_path().split("/")
        print(url)
        if j==1 or j==8:
            if url[3]=="zakup":
                if request.session.get("_old_post_zakup","!")!="!":
                    nak_id=request.session.get("_old_post_zakup").get("nak_id")
                    products=Purchase.objects.filter(Q(nak_id=nak_id)&~Q(purchased_kol=0)&Q(is_returned=False))
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    products1=[]
                    for pr in products:
                        if pr.fact_kol==None:
                            pr.fact_kol=0.0
                        if pr.fact_kol>pr.purchased_kol:
                            print(pr.fact_kol,pr.purchased_kol,pr.name.name)
                            continue
                        else:
                            products1.append(pr)
                    return render(request,"get_products.html",{"indic":1,"products":products1})
                else:
                    form=NaklForm(Purchase.objects.filter(is_delivered=0).order_by("nak_id"))
            elif url[3]=="zagot":
                al=request.GET.get("al")
                if request.session.get("_old_post_zagot","!")!="!":
                    nak_id=request.session.get("_old_post_zagot").get("nak_id")
                    form=BarcodeForm()
                    if al=="1":
                        return render(request,"get_products.html",{"indic":0,"form":form,"al":1})
                    else:
                        return render(request,"get_products.html",{"indic":0,"form":form})
                else:
                    form=NaklForm(Nakl_for_zagot.objects.filter(Q(is_maked=True)&Q(is_returned=False)).order_by("nak_id"))
            return render(request,"get_nak_id.html",{"form":form})
        else:
            raise Http404

@login_required
def reset_nak_id(request):
    j=request.user.roles.role
    url=request.get_full_path().split("/")
    if j==1 or j==8:
        if url[3]=="zakup":
            request.session["_old_post_zakup"]="!"
            return redirect("/accounts/profile/zakup/nak_id")
        elif url[3]=="zagot":
            request.session["_old_post_zagot"]="!"
            return redirect("/accounts/profile/zagot/nak_id")
        else:
            return redirect("/accounts/profile/")
    else:
        return redirect("/accounts/profile/")

@login_required
def get_barcode(request):
    if request.method=="POST" and request.user.roles.role==1:
        barcode=request.POST.get("name")
        if len(barcode)==13:
            barcode=barcode[:-1]
        else:
            barcode="0"+barcode[:-1]
        nak_id=request.session.get("_old_post_zagot").get("nak_id")
        print("!!!",int(barcode[:-9]),nak_id)
        try:
            product=Harvester_Barcodes.objects.get(Q(barcode=barcode)&Q(nak_id=nak_id))
        except ObjectDoesNotExist:
            return redirect("/accounts/profile/zagot/get_products?al=1")
        return redirect(f"/accounts/profile/zagot/get_product?n={nak_id}&id={product.product_id}")
    else:
        return redirect("/accounts/profile")

@login_required
def list_product_without_nakl(request):
    url=request.get_full_path().split("/")
    j=request.user.roles.role
    products=Products.objects.filter(prigot=True)
    if j==1 or j==8:
        nakl=Without_nakl.objects.all()
        nakl=list(nakl)[::-1]
        nnakl=[]
        nakl_id=[]
        for n in nakl:
            if n.nak_id not in nakl_id:
                nnakl.append(n)
                nakl_id.append(n.nak_id)
        return render(request,"list_no_nakl.html",{"nakl":nnakl})

@login_required
def products_without_nakl(request):
    url=request.get_full_path().split("/")
    j=request.user.roles.role
    products=Products.objects.filter(prigot=True)
    if j==1 or j==8 or j==4:
        nak_id=request.GET.get("n")
        products=Without_nakl.objects.filter(Q(nak_id=nak_id))
        status="Отправлена" if products[0].is_accepted==True else "Не отправлена"
        return render(request,"products_no_nakl.html",{"products":products,"n":nak_id,"date":products[0].date,"status":status})

@login_required
def get_product_without_nakl(request):
    url=request.get_full_path().split("/")
    j=request.user.roles.role
    products=Products.objects.filter(prigot=True)
    if j==1 or j==8 or j==4:
        nak_id=request.GET.get("n")
        nakl=Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=False))
        if request.method!="POST":
            return render(request,"sklad_no_nakl.html",{"products":products,"nakl":nakl,"nak_id":nak_id,"ind":j})
        else:
            product=request.POST.get("product")
            kol=request.POST.get("kol")
            kol=round(float(kol),3)
            #date=request.POST.get("date")
            date_now=datetime.now().date()
            shtr_kol=request.POST.get("shtr_kol",0)
            text=shtr_kol.split("/")
            print(text,len(text))
            if len(text)==1:
                shtr_kol=int(shtr_kol)
                com=""
            else:
                shtr_kol=int(text[0])
                com=text[1]
            #srok=datetime.strptime(date,r"%Y-%m-%d").date()
            print("!!",product)
            prod=Products.objects.get(name=product)
            barcod=generate_barcode(prod.id,d.date(2025,12,12))
            '''try:
                c=Codes.objects.get(shtrih=barcod)
                c.kolvo+=kol
                c.save()
            except ObjectDoesNotExist:
                Codes(name=prod,kolvo=kol,shtrih=barcod).save()
            '''
            print(j)
            if j==4:
                for i in range(shtr_kol):
                    print_barcode(product,date_now,barcod,com,prod.edizm.edizm)
                trash2()
            else:
                for i in range(shtr_kol):
                    print_barcode_2(product,date_now,barcod,com,prod.edizm.edizm)
                trash()
            print(4)
            #trash()
            '''
            try:
                st=Stock.objects.get(name=prod)
                st.ostat+=kol
                st.save()
            except ObjectDoesNotExist:
                Stock(name=prod,ostat=kol).save()
            '''
            Without_nakl(nak_id=nak_id,name=prod,srok=d.date(2025,12,12),fact_kol=kol,purchase=request.user,date=date_now).save()
            return render(request,"sklad_no_nakl.html",{"products":products,"nakl":nakl,"nak_id":nak_id,"ind":j})

@login_required
def delete_product_without_nakl(request):
    url=request.get_full_path().split("/")
    j=request.user.roles.role
    products=Products.objects.filter(prigot=True)
    if j==1 or j==8 or j==4:
        nak_id=int(request.GET.get("n"))
        p_id=int(request.GET.get("id"))
        product=Without_nakl.objects.get(Q(id=p_id)&Q(nak_id=nak_id))
        product.delete()
        return redirect(f"/accounts/profile/no_nakl?n={nak_id}")


@login_required
def accept_product_without_nakl(request):
    url=request.get_full_path().split("/")
    j=request.user.roles.role
    products=Products.objects.filter(prigot=True)
    if j==1 or j==8:
        nak_id=int(request.GET.get("n"))
        products=Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=False))
        for p in products:
            barcod=generate_barcode(p.name.id,d.date(2025,12,12))
            try:
                c=Codes.objects.get(shtrih=barcod)
                c.kolvo+=p.fact_kol
                c.save()
            except ObjectDoesNotExist:
                Codes(name=p.name,kolvo=p.fact_kol,shtrih=barcod).save()
            try:
                st=Stock.objects.get(name=p.name)
                st.ostat+=p.fact_kol
                st.save()
            except ObjectDoesNotExist:
                Stock(name=p.name,ostat=p.fact_kol).save()
            p.is_accepted=True
            p.save()
        return redirect("/accounts/profile/")

@login_required
def get_product(request):
    url=request.get_full_path().split("/")
    if request.method=="POST":
        j=request.user.roles.role
        if j==1 or j==8:
            nak_id=int(request.GET.get("n"))
            pid=int(request.GET.get("id"))
            if url[3]=="zakup":
                product=Purchase.objects.get(Q(nak_id=nak_id)&Q(id=pid))
                kol=float(request.POST.get("kol"))
                srok="2025-12-12"
                shtr_kol=request.POST.get("shtr_kol")
                text=shtr_kol.split("/")
                if len(text)==1:
                    shtr_kol=int(shtr_kol)
                    com=""
                else:
                    shtr_kol=int(text[0])
                    com=text[1]
                srok=datetime.strptime(srok,r"%Y-%m-%d").date()
                print(srok)
                if srok<product.min_srok:
                    print("!!!!!!!!")
                    return redirect(f"/accounts/profile/zakup/return_product?n={nak_id}&id={pid}")
                else:
                    fact_kol=round(kol,3)
                    if request.session.get("_zakup_fact_kol","!")=="!":
                        request.session["_zakup_fact_kol"]=fact_kol
                    else:
                        request.session["_zakup_fact_kol"]+=fact_kol
                    if request.session.get("_zakup_pur_kol","!")=="!":
                        request.session["_zakup_pur_kol"]=product.purchased_kol
                        print(333,request.session.get("_zakup_pur_kol"))
                    now_date=datetime.now().date()
                    product.fact_kol=fact_kol
                    product.srok=now_date
                    product.is_delivered=True
                    product.is_returned=False
                    barcod=generate_barcode(product.name.id,srok)
                    try:
                        print(")))))))))))))))))")
                        c=Codes.objects.get(shtrih=barcod)
                        print("1",barcod)
                        c.kolvo+=fact_kol
                        print(2)
                        c.save()
                        print(3)
                    except ObjectDoesNotExist:
                        Codes(name=product.name,kolvo=fact_kol,shtrih=barcod).save()
                        print("!@##$$@!@!@")
                    print("####")
                    for i in range(shtr_kol):
                        print_barcode_2(product.name.name,now_date,barcod,com,product.name.edizm.edizm)
                    print(4)
                    trash()
                    if fact_kol<product.purchased_kol:
                        print("????????",product.name)
                        product.purchased_kol=round(product.purchased_kol-fact_kol,3)
                        product.save()
                        try:
                            st=Stock.objects.get(name=product.name)
                            st.ostat+=round(kol,3)
                            st.save()
                        except ObjectDoesNotExist:
                            Stock(name=product.name,ostat=round(float(fact_kol),3)).save()
                        return redirect(f"/accounts/profile/zakup/get_product?n={nak_id}&id={pid}")
                    else:
                        print("#####",request.session.get("_zakup_pur_kol"))
                        print(request.session.get("_zakup_fact_kol"))
                        if round(kol,3)>product.purchased_kol:
                            print("^^^^^^^^^^")
                            product.fact_kol=round(kol,3)
                            product.srok=now_date
                            product.is_delivered=True
                            product.is_returned=False
                            product.save()
                            fact_kol=round(kol,3)
                        else:
                            print("((((((((")
                            product.purchased_kol=round(request.session.get("_zakup_pur_kol"),3)
                            product.fact_kol=round(float(request.session.get("_zakup_fact_kol")),3)
                            product.save()
                        try:
                            st=Stock.objects.get(name=product.name)
                            print('$$$$',fact_kol)
                            st.ostat+=fact_kol
                            st.ostat=round(st.ostat,3)
                            st.save()
                            request.session["_zakup_fact_kol"]=0.0
                            request.session["_zakup_pur_kol"]="!"
                            print("##",request.session.get("_zakup_pur_kol"))
                        except ObjectDoesNotExist:
                            Stock(name=product.name,ostat=round(float(request.session.get("_zakup_fact_kol")),3)).save()
                            request.session["_zakup_fact_kol"]=0.0
                            request.session["_zakup_pur_kol"]="!"
                            print("###",request.session.get("_zakup_pur_kol"))
                        return redirect("/accounts/profile/zakup/get_products")
            elif url[3]=="zagot":
                product=Nakl_for_zagot.objects.get(Q(nak_id=nak_id)&Q(id=pid))
                kol=float(request.POST.get("kol"))
                fact_kol=round(kol,3)
                #srok=request.POST.get("srok")
                #shtr_kol=int(request.POST.get("shtr_kol"))
                #srok=datetime.datetime.strptime(srok,r"%Y-%m-%d").date()
                product.ac_kolvo+=round(kol,3)
                #product.srok=srok
                product.in_stock=True
                product.is_returned=False
                product.save()
                barcod=Harvester_Barcodes.objects.get(Q(nak_id=nak_id)&Q(product_id=pid)).barcode
                try:
                    c=Codes.objects.get(shtrih=barcod)
                    c.kolvo+=fact_kol
                    c.save()
                except ObjectDoesNotExist:
                    Codes(name=product.name,kolvo=fact_kol,shtrih=product.shtrih).save()
                try:
                    st=Stock.objects.get(name=product.name)
                    st.ostat+=fact_kol
                    st.save()
                except ObjectDoesNotExist:
                    Stock(name=product.name,ostat=fact_kol).save()
                return redirect("/accounts/profile/zagot/get_products")

        else:
            raise Http404
    else:
        j=request.user.roles.role
        if j==1 or j==8:
            nak_id=int(request.GET.get("n"))
            pid=int(request.GET.get("id"))
            if url[3]=="zakup":
                product_purchase=Purchase.objects.get(Q(nak_id=nak_id)&Q(id=pid))
                product=product_purchase.name
                link=product.image
                kolvo=product_purchase.kolvo
                min_srok=product_purchase.min_srok
                zakup=product_purchase.purchased_kol
                ed_izm=product_purchase.name.edizm.edizm
                form=GetForm()
                return render(request,"get_product.html",{"indic":1,"form":form,"product":product,"link":link,"n":nak_id,"id":pid,"kolvo":kolvo,"min":min_srok,"zakup":zakup,"ed_izm":ed_izm})
            elif url[3]=="zagot":
                product_zagot=Nakl_for_zagot.objects.get(Q(nak_id=nak_id)&Q(id=pid))
                product=product_zagot.name
                link=product.image
                kolvo=product_zagot.tkolvo
                zakup=product_zagot.pkolvo
                ed_izm=product_zagot.name.edizm.edizm
                form=GetForm2()
                return render(request,"get_product.html",{"indic":0,"form":form,"product":product,"link":link,"n":nak_id,"id":pid,"kolvo":kolvo,"zakup":zakup,"ed_izm":ed_izm})
        else:
            raise Http404

@login_required
def return_product(request):
    j=request.user.roles.role
    url=request.get_full_path().split("/")
    if j==1 or j==8:
        nak_id=int(request.GET.get("n"))
        pid=int(request.GET.get("id"))
        if url[3]=="zakup":
            product_purchase=Purchase.objects.get(Q(nak_id=nak_id)&Q(id=pid))
            product_purchase.is_returned=True
            product_purchase.save()
            request.session["_zakup_fact_kol"]=0.0
            request.session["_zakup_pur_kol"]="!"
            return redirect("/accounts/profile/zakup/get_products")
        elif url[3]=="zagot":
            product=Nakl_for_zagot.objects.get(Q(nak_id=nak_id)&Q(id=pid))
            product.is_returned=True
            product.save()
            return redirect("/accounts/profile/zagot/get_products")
    else:
        raise Http404

@login_required
def returned_list(request):
    j=request.user.roles.role
    url=request.get_full_path().split("/")
    if url[-1]=="zakup":
        if j==3 or j==8:
            products=Purchase.objects.filter(is_returned=True)
            return render(request,"returned.html",{"indic":1,"products":products})
        else:
            return redirect("/accounts/profile")
    elif url[-1]=="zagot":
        if j==4 or j==8:
            products=Nakl_for_zagot.objects.filter(is_returned=True)
            return render(request,"returned.html",{"indic":2,"products":products})
        else:
            return redirect("/accounts/profile")
    elif url[-1]=="sklad":
        if j==1 or j==8:
            products=Purchase.objects.filter(is_returned=True)
            prod=Nakl_for_zagot.objects.filter(is_returned=True)
            return render(request,"returned.html",{"indic":int(3),"products":products,"prod":prod})
        else:
            return redirect("/accounts/profile")



@login_required
def spis(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if request.method=="POST":
        rec=request.POST.get("receiv")
        kol=dict(request.POST).get("kol")
        name=dict(request.POST).get("name")
        zagot_id=request.POST.get("zagot_id","!")
        if zagot_id!="!":
            f=True
        else:
            f=False
        errors={}
        spis_codes=[]
        s_codes=[]
        l_name=[]
        print(name)
        try:
            last_id=max([int(s.nak_id) for s in Spis.objects.all()])
        except ValueError:
            last_id=0
        for i in range(len(name)):
            if len(name[i])==13:
                bar=name[i][1:]
                bar2=name[i][:-1]
            else:
                bar=name[i]
                bar2="0"+name[i][:-1]
            if (name[i]=="") or (kol[i]==""):
                continue
            print("bbb",bar,bar2)
            s_codes.append(bar2)
            try:
                codes=Codes.objects.get(shtrih=bar2)
            except ObjectDoesNotExist:
                pr=Products.objects.get(id=bar2[:4])
                cd=[]
                cds=Codes.objects.filter(name=pr)
                for c in cds:
                    cd.append(c.shtrih)
                cd=",".join(cd)
                errors["Нет такого штрих-кода"]=f"Нет такого штрих-кода. Другие штрих-коды для {pr}:{cd}"
                continue
            spis_codes.append(codes)
            product=Products.objects.get(name=codes.name)
            l_name.append(product)
            print(l_name)
            ccodes=Codes.objects.filter(name=product)
            ccodes=[datetime.strptime(c.shtrih[-8:],r"%d%m%Y").date() for c in ccodes]
            print(type(product),product)
            print("ccc",ccodes)
            try:
                print(333333333)
                stk=Stock.objects.get(name=product)
                if stk.ostat<float(kol[i]):
                    print(1)
                    errors[product]="Недостаточно на складе"
                    print("???",errors)
                    continue
                    #return render(request,"spis1.html",{"text":f"{product}! Недостаточно на складе"})
                elif codes.kolvo<float(kol[i]):
                    print(2)
                    errors[product]="Недостаточно в партии"
                    continue
                    #return render(request,"spis1.html",{"text":f"{product}! Недостаточно в партии"})
                elif len(ccodes)>0:
                    print(3)
                    barcode_date=datetime.strptime(bar2[-8:],r"%d%m%Y").date()
                    for cod in ccodes:
                        print("@@@",kol[i])
                        if cod<barcode_date:
                            errors[product]="Отказано!Вы пытаетесь списать более позднюю партию."
                            break
                            #return render(request,"spis1.html",{"text":f"{product}! Отказано!Вы пытаетесь списать более позднюю партию."})
            except ObjectDoesNotExist:
                errors[product]="Нет на складе"
        print(4)
        print(kol[i])
        print(errors)
        if len(errors)==0:
            print("1111111")
            for i in range(len(l_name)):
                stk=Stock.objects.get(name=l_name[i])
                try:
                    cons=Daily_Consumption.objects.get(name=l_name[i])
                    cons.consumption+=round(float(kol[i]),3)
                    cons.consumption=round(cons.consumption,3)
                    cons.save()
                except ObjectDoesNotExist:
                    Daily_Consumption(name=l_name[i],consumption=round(float(kol[i]),3)).save()
                codes=spis_codes[i]
                stk.ostat=round(stk.ostat-float(kol[i]),3)
                codes.kolvo=round(codes.kolvo-float(kol[i]),3)
                stk.save()
                codes.save()
                if codes.kolvo==0.0:
                    codes.delete()
                if stk.ostat==0.0:
                    stk.delete()
                #print("$$$$$$$$$$$$",Receivers.objects.get(receiver=rec),kol)
                try:
                    user_name=translit(request.user.username,reversed=True)
                except LanguageDetectionError:
                    user_name=request.user.username
                print("!!!!!",rec)
                nakl=Spis(nak_id=last_id+1,product=s_codes[i],kol=kol[i],receiver=Receivers.objects.get(receiver=rec),user=user_name,date=datetime.now()).save()
                print("!!!!!!!")
                if f:
                    Zagot_products(nak_id=zagot_id,product=l_name[i],kol=float(kol[i]),user=Zagot_types.objects.filter(user__username=rec).first(),kolvo=0.0).save()
                    Nakl_for_zagot.objects.filter(Q(nak_id=zagot_id)&Q(user=Zagot_types.objects.filter(user__username=rec).first())&Q(name=l_name[i])).update(is_given=True)
                    try:
                        stock=Harvester_Stock.objects.get(Q(user=User.objects.get(username=rec))&Q(product=l_name[i]))
                    except ObjectDoesNotExist:
                        Harvester_Stock(user=User.objects.get(username=rec),product=l_name[i],kol=round(float(kol[i]),3)).save()
                        continue
                    stock.kol+=round(float(kol[i]),3)
                    stock.save()
            #return render(request,"spis1.html",{"text":"Списано"})
                #return render(request,"spis1.html",{"text":f"{product}! Нет на складе"})
            return redirect(f"../nakl_order/?nak_id={last_id+1}")
        else:
            return render(request,"spis1.html",{"indic":1,"text":errors})
    else:
        rec=Receivers.objects.all()
        form=SpisForm(rec)
        return render(request,"spisanie.html",{"job":job,"form":form})

@login_required
def query_to_remove_spis(request):
    j=request.user.roles.role
    if j==1 or j==8:
        if request.method!="POST":
            nak_id=int(request.GET.get("n"))
            products=Spis.objects.filter(Q(nak_id=nak_id)&Q(is_removed=False))
            names=[Products.objects.get(id=int(p.product[:4])) for p in products]
            kolvo=[p.kol for p in products]
            if (datetime.now(timezone.utc)-products.first().date).seconds<=3600:
                return render(request,"removed_spis.html",{"names":names,"nak_id":nak_id,"kol":kolvo,"range":range(len(names))})
            else:
                return render(request,"removed_spis.html",{"indic":1})
        else:
            nak_id=int(request.POST.get("nak_id"))
            products=Spis.objects.filter(Q(nak_id=nak_id)&Q(is_removed=False))
            for p in products:
                try:
                    if User.objects.get(username=p.receiver.receiver).roles==4:
                        harvester_p=Harvestar_Stock.objects.get(product__name=p.product)
                        st=Stock.objects.get(name__id=int(p.product[:4]))
                        if harvester_p.kol<p.kol:
                            st.ostat+=harvester_p.kol
                            harvester_p.kol=0.0
                        else:
                            st.ostat+=p.kolvo
                            harvester_p.kol-=p.kol
                        st.ostat=round(st.ostat,3)
                        harvester_p.kol=round(harvester_p.kol,3)
                        st.save()
                        harvester_p.save()
                    else:
                        st=Stock.objects.get(name__id=int(p.product[:4]))
                        st.ostat+=p.kol
                        st.ostat=round(st.ostat,3)
                        st.save()
                        code=Codes.objects.filter(shtrih=p.product)
                        if code.count()==0:
                            Codes(shtrih=p.product,kolvo=p.kol,name=Products.objects.get(id=int(p.product[:4]))).save()
                        else:
                            code.first().kolvo+=p.kol
                            code.first().save()
                except Exception as e:
                        st=Stock.objects.get(name__id=int(p.product[:4]))
                        st.ostat+=p.kol
                        st.ostat=round(st.ostat,3)
                        st.save()
                        code=Codes.objects.get(shtrih=p.product)
                        print(code)
                        try:
                            code.kolvo+=p.kol
                            code.save()
                            print("!!!!!")
                        except ObjectDoesNotExist:
                            Codes(shtrih=p.product,kolvo=p.kol,name=Products.objects.get(id=int(p.product[:4]))).save()
                        #import traceback
                        #print(traceback.format_exc())
                products.update(is_removed=True)

            return redirect("/accounts/profile")



@login_required
def spis_zagot(request):
    j=request.user.roles.role
    if j==1 or j==8:
        nak_id=int(request.GET.get("n"))
        zagot_name=[]
        zagot_users=[]
        for p in Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)&Q(is_given=False)):
            if p.user.user.username not in zagot_name:
                zagot_name.append(p.user.user.username)
                zagot_users.append(p.user.user)
        return render(request,"spis_zagot.html",{"zagot":zagot_users,"nak_id":nak_id})

@login_required
def spis_create_nakl(request):
    j=request.user.roles.role
    if j==1 or j==8:
        if request.method!="POST":
            nak_id=int(request.GET.get("n"))
            uid=int(request.GET.get("u"))
            products=Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)&Q(is_given=False)&Q(user__id=uid))
            name=User.objects.get(id=uid).username
            print(name)
            try:
                Receivers.objects.get(receiver=name)
            except ObjectDoesNotExist:
                Receivers(receiver=name).save()
            kol=[]
            ingreds=[]
            for p in products:
                print(type(p.name))
                ingrs=Ingredients.objects.filter(product=p.name)
                print(ingrs)
                #ingr=[(i.ingr.name,round(float(i.kolvo)*p.tkolvo,3)) for i in ingrs]
                for ing in ingrs:
                    ingreds.append((ing.ingr.name,round(float(ing.kolvo)*p.tkolvo,3)))
            print(request.user.username)
            rec=Receivers.objects.all()
            form=SpisForm(rec,n=name)
            return render(request,"spisanie.html",{"indic":1,"ingr":ingreds,"name":name,"nak_id":nak_id,"form":form})


@login_required
def nakl_orders(request):
    j=request.user.roles.role
    if j==1 or j==8:
        if request.method!="POST":
            nakl=int(Spis.objects.all().last().nak_id)
            naks=Spis.objects.filter(nak_id__gt=(nakl-101))
            nak=[]
            products=Products.objects.all()
            n_id=[]
            e=request.GET.get("e","!")
            for n in naks:
                if n.nak_id not in n_id:
                    nak.append(n)
                    n_id.append(n.nak_id)
            nak=nak[::-1]
            if e=="1":
                return render(request,"nakl_orders.html",{"naks":nak,"products":products,"indic":1,"nak_id":nakl})
            else:
                return render(request,"nakl_orders.html",{"naks":nak,"products":products,"nak_id":nakl})
        else:
            name=request.POST.get("product")
            try:
                product=Products.objects.get(name=name)
            except ObjectDoesNotExist:
                return redirect("/accounts/profile/nakl_orders/?e=1")
            prod_id=str(product.id).zfill(4)
            print(prod_id)
            spis=Spis.objects.filter(product__startswith=prod_id)
            all_spis=sum([s.kol for s in spis])
            all_spis=round(all_spis,3)
            return render(request,"nakl_order_stats.html",{"spis":spis,"product":product,"all_spis":all_spis})
    else:
        return redirect("/accounts/profile")

@login_required
def nakl_order(request):
    j=request.user.roles.role
    if j==1 or j==8:
        nak_id=int(request.GET.get("nak_id"))
        nak=Spis.objects.filter(nak_id=nak_id)
        receiver=nak[0].receiver.receiver
        ingr=[s.product for s in nak]
        kolvo=[s.kol for s in nak]
        prod=[]
        ed_izm=[]
        for p in ingr:
            print(Products.objects.get(id=int(p[:4])))
            prod.append(Products.objects.get(id=int(p[:4])).name)
            ed_izm.append(Products.objects.get(id=int(p[:4])).edizm)
        return render(request,"nakl_order.html",{"range":range(len(ingr)),"ingr":prod,"kolvo":kolvo,"izm":ed_izm,"name":nak[0].user,"n":nak_id,"date":nak[0].date,"receiver":receiver})
    else:
        return redirect("/accounts/profile")

@login_required
def choose_type(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8:
        n=Without_nakl.objects.filter(is_accepted=False)
        if n.count()!=0:
            nak_id=n.last().nak_id
        else:
            n=Without_nakl.objects.filter(is_accepted=True)
            nak_id=int(n.last().nak_id)+1
        return render(request,"sklad_select_type.html",{"nak_id":nak_id})
    else:
        return redirect("/accounts/profile")

@login_required
def barcode_for_rediscount(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8 or j==8:
        r_id=int(request.GET.get("id"))
        if request.method!="POST":
            stock=Stock.objects.all()
            redisc=Rediscount.objects.filter(red_id=r_id)
            status=f"{redisc.count()}/{stock.count()}"
            print(redisc)
            other=[]
            for st in stock:
                f=0
                for r in redisc:
                    if st.name==r.name:
                        print("@@")
                        f=1
                if f!=1:
                    other.append(st.name)
            return render(request,"pereuchet.html",{"id":r_id,"date":datetime.now().date(),"other":other,"progress":status})
        else:
            bar=request.POST.get("bar")
            if len(bar)==12:
                bar="0"+bar[:-1]
            code_id=Codes.objects.get(shtrih=bar).id
            return redirect(f"/accounts/profile/product_rediscount/?c_id={code_id}&r_id={r_id}")

@login_required
def product_for_rediscount(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8 or j==8:
        code_id=int(request.GET.get("c_id"))
        r_id=int(request.GET.get("r_id"))
        code=Codes.objects.get(id=code_id)
        if request.method=="POST":
            new_kol=float(request.POST.get("kol"))
            difference=(-1)*(code.kolvo-new_kol)
            stock=Stock.objects.get(name=code.name)
            code.kolvo+=difference
            stock.ostat+=difference
            stock.ostat=round(stock.ostat,3)
            code.kolvo=round(code.kolvo,3)
            code.save()
            stock.save()
            try:
                r=Rediscount.objects.get(Q(red_id=r_id)&Q(name=code.name))
                r.kol=round((difference+r.kol),3)
                r.st_kol=round(float(stock.ostat),3)
                r.save()
            except ObjectDoesNotExist:
                Rediscount(red_id=r_id,name=code.name,kol=round(difference,3),st_kol=round(float(stock.ostat),3)).save()
            return redirect(f"/accounts/profile/rediscount/?id={r_id}")
        else:
            return render(request,"product_rediscount.html",{"code":code})

@login_required
def close_rediscount(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8:
        if request.method=="POST":
            red_id=int(request.POST.get("id"))
            rediscounts=Rediscount.objects.filter(red_id=red_id).count()
            if rediscounts==0:
                return JsonResponse({"result":"first"})
            else:
                products=Stock.objects.all().count()
                progress=f"{rediscounts}/{products}"
                Rediscount_info(rediscount=Rediscount.objects.filter(red_id=red_id).first(),progress=progress,date=datetime.now().date(),user=request.user,is_closed=True).save()
                return JsonResponse({"result":"ok"})


@login_required
def info_about_rediscount(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1 or j==8:
        r_id=request.GET.get("r","")
        if r_id=="":
            r_id=Rediscount.objects.all().last().red_id
        else:
            r_id=int(r_id)
        try:
            rediscount_info=Rediscount_info.objects.get(rediscount__red_id=r_id)
            b=0
        except ObjectDoesNotExist:
            b=1
        rediscount=Rediscount.objects.filter(red_id=r_id)
        products=[r.name for r in rediscount]
        kol=[]
        for r in rediscount:
            try:
                kolvo=round(float(r.st_kol),3)
            except ObjectDoesNotExist:
                kolvo=0.0
            kol.append(kolvo)
        average=[]
        for r in rediscount:
            #print(r.name)
            try:
                av=round(float(LastCost.objects.get(product=r.name).average),3)
                if av==0.0:
                    average.append(round(float(LastCost.objects.get(product=r.name).cost),3))
                else:
                    average.append(av)
            except ObjectDoesNotExist:
                #average.append(0)
                prod=Ingredients.objects.filter(product=r.name)
                print(r.name)
                if prod.count()==0:
                    average.append(0)
                else:
                    ccost=0.0
                    for p in prod:
                        try:
                            print("!",p.ingr)
                            cost=round(float(LastCost.objects.get(product=p.ingr).average),3)
                            if cost==0.0:
                                cost=round(float(LastCost.objects.get(product=p.ingr).cost),3)
                            ccost+=cost
                        except ObjectDoesNotExist:
                            ccost=0.0
                    average.append(ccost)
                    #LastCost(cost=ccost,average=ccost,product=r.name).save()
        summ=[]
        ssumm=0
        for i in range(rediscount.count()):
            ssumm+=round(kol[i]*average[i],3)
            summ.append(ssumm)
            ssumm=0
        plus=[]
        minus=[]
        classes=[]
        ind=0
        for r in rediscount:
            if r.kol>0:
                plus.append(float(r.kol))
                minus.append(" ")
                classes.append("non-zero")
            elif r.kol<0:
                minus.append(float(r.kol))
                plus.append(" ")
                classes.append("non-zero")
            else:
                minus.append(" ")
                plus.append(" ")
                classes.append("zero")
        status="Закончен" if b==0 else "В процессе"
        stock=Stock.objects.all()
        redisc=Rediscount.objects.filter(red_id=r_id)
        progress=f"{redisc.count()}/{stock.count()}"
        all_summ=sum(summ)
        all_plus=0
        all_minus=0
        for i in range(rediscount.count()):
            if plus[i]!=" ":
                all_plus+=round((plus[i]*average[i]),3)
            else:
                i+=1
        for i in range(rediscount.count()):
            if minus[i]!=" ":
                all_minus+=round((minus[i]*average[i]),3)
            else:
                i+=1
        if b!=1:
            create_xls_rediscount(rediscount,rediscount_info.date,average,summ,plus,minus)
            link=f'rediscount_{datetime.strftime(rediscount_info.date,"%d-%m-%Y")}.xls'
        else:
            link=""
        return render(request,"rediscount_info.html",
            {
            "range":range(rediscount.count()),
            "classes":classes,
            #"info":rediscount_info,
            "products":products,
            "kol":kol,
            "average":average,
            "summ":summ,
            "plus":plus,
            "minus":minus,
            "all_summ":round(float(all_summ),3),
            "plus_summ":round(float(all_plus),3),
            "minus_summ":round(float(all_minus),3),
            "status":status,
            "progress":progress,
            "link":link
            })

@login_required
def all_rediscounts(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==3 or j==8:
        red=Rediscount_info.objects.all()
        numbers=[]
        for r in red:
            numbers.append(r)
        numbers=numbers[::-1]
        return render(request,"all_rediscounts_info.html",{"numbers":numbers})

@login_required
def unrealized(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==3 or j==8:
        nak_id=int(request.GET.get("n"))
        unrealized=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0))
        summ=0.0
        for u in unrealized:
            summ+=round((u.kolvo*u.last_cost),3)
        return render(request,"zakup_unrealized.html",{"unrealized":unrealized,"summ":summ})

def multi_sort(s_mas,mas_one,mas_two,mas_three):
    #mm={}
    #for m in s_mas:
    #    mm[s_mas.index(m)]=sorted(s_mas).index(m)
    #mas_indexes=[s_mas.index(m) for m in s_mas]
    #print(mas_indexes)
    #mas_indexes_after=[s_mas.index(m) for m in sorted(s_mas)]
    #print(mas_indexes_after)
    old_mas=s_mas
    n_mas=sorted(s_mas)
    leng=len(s_mas)
    print(leng)
    n_mas_one=[-1]*leng
    n_mas_two=[-1]*leng
    n_mas_three=[-1]*leng
    for i in range(leng):
        ind_do=old_mas.index(n_mas[i])
        n_mas_one[i]=mas_one[ind_do]
        n_mas_two[i]=mas_two[ind_do]
        n_mas_three[i]=mas_three[ind_do]
        old_mas[ind_do]="!"
    return n_mas_one,n_mas_two,n_mas_three

@login_required
def all_receipt(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==8:
        from itertools import chain
        s=int(request.GET.get("s","6"))
        if s==1:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)),Without_nakl.objects.filter(is_accepted=True)))
        elif s==0:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("name"),Without_nakl.objects.filter(is_accepted=True).order_by("name")))
        elif s==2:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("date"),Without_nakl.objects.filter(is_accepted=True).order_by("date")))
        elif s==3:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("summ"),Without_nakl.objects.filter(is_accepted=True)))
        elif s==4:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("purchase__username"),Without_nakl.objects.filter(is_accepted=True).order_by("purchase__username")))
        else:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)),Without_nakl.objects.filter(is_accepted=True)))
        nakls=[]
        for p in pproducts:
            if p.nak_id not in nakls:
                nakls.append(p.nak_id)
        dates=[]
        summ=[]
        purchases=[]
        for i in range(len(nakls)):
            ssum=0
            nnakls=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(nak_id=nakls[i])),Without_nakl.objects.filter(Q(is_accepted=True)&Q(nak_id=nakls[i]))))
            for n in nnakls:
                if int(n.nak_id)<8999 and int(n.nak_id)>0:
                    ssum+=n.summ
                else:
                    ssum=0
            summ.append(round(ssum,3))
            print(nnakls[0].date)
            dates.append(nnakls[0].date)
            #print("!!!",nnakls[0].purchase)
            if nnakls[0].purchase!=None:
                purchases.append(nnakls[0].purchase.username)
            else:
                purchases.append("-")
        if s==3:
            k_sum=summ
            summ=sorted(summ)
            nakls,dates,purchases=multi_sort(k_sum,nakls,dates,purchases)
        if s==4:
            k_pur=purchases
            purchases=sorted(purchases)
            nakls,dates,summ=multi_sort(k_pur,nakls,dates,summ)
        #paginator=Paginator(pproducts,100)
        #page_number = request.GET.get('page')
        #products = paginator.get_page(page_number)
        #products=Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True))
        #table=ReceiptTable(products)
        return render(request,"all_receipt.html",{"nakls":nakls,"dates":dates,"summ":summ,"purchase":purchases,"range":range(len(nakls))})

@login_required
def all_consumption(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==8:
        from itertools import chain
        s=int(request.GET.get("s","6"))
        ind=int(Spis.objects.all().last().nak_id)-100
        if s==1:
            pproducts=Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=ind))
        elif s==0:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("name"),Without_nakl.objects.filter(is_accepted=True).order_by("name")))
        elif s==2:
            pproducts=Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=ind)).order_by("date")
        elif s==3:
            pproducts=list(chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)).order_by("summ"),Without_nakl.objects.filter(is_accepted=True)))
        elif s==4:
            pproducts=Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=ind)).order_by("receiver__receiver")
        else:
            pproducts=Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=ind))
        nakls=[]
        for p in pproducts:
            if p.nak_id not in nakls:
                nakls.append(p.nak_id)
        dates=[]
        purchases=[]
        summ=[]
        k=0
        for i in range(len(nakls)):
            nnakls=Spis.objects.filter(Q(is_removed=False)&Q(nak_id=nakls[i]))
            try:
                print(nakls[i])
                #print(nnakls.first().date)
                dates.append(nnakls.first().date)
                #print("!!!",nnakls[0].purchase)
                summ.append(0)
                if nnakls.first().receiver!=None:
                    purchases.append(nnakls.first().receiver.receiver)
                else:
                    purchases.append("-")
            except Exception as e:
                k+=1
                print(e)
                continue
        if s==3:
            k_sum=summ
            summ=sorted(summ)
            nakls,dates,purchases=multi_sort(k_sum,nakls,dates,purchases)
        if s==4:
            k_pur=purchases
            purchases=sorted(purchases)
            nakls,dates,summ=multi_sort(k_pur,nakls,dates,summ)
        #paginator=Paginator(pproducts,100)
        #page_number = request.GET.get('page')
        #products = paginator.get_page(page_number)
        #products=Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True))
        #table=ReceiptTable(products)
        return render(request,"all_consumption.html",{"nakls":nakls,"dates":dates,"purchase":purchases,"range":range(len(nakls)-k)})


@login_required
def info_table(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==8:
        print("!!!")
        products=Products.objects.all()
        nakls_zakup=[]
        names_zakup=[]
        for p in Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)):
            if int(p.nak_id) not in nakls_zakup:
                nakls_zakup.append(int(p.nak_id))
        print(123)
        for u in User.objects.all():
            if u.username not in names_zakup:
                names_zakup.append(u.username)
        print(567)
        nakls_spis=[]
        names_spis=[]
        s_id=Spis.objects.filter(is_removed=False).last().nak_id
        print(Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=(s_id-50))).count())
        for s in Spis.objects.filter(Q(is_removed=False)&Q(nak_id__gte=(s_id-50))):
            if int(s.nak_id) not in nakls_spis:
                nakls_spis.append(int(s.nak_id))
            if s.receiver.receiver not in names_spis:
                names_spis.append(s.receiver.receiver)
        print(890)
        url=request.get_full_path().split("/")
        if request.method!="POST":
            if url[3]=="receipt":
                nakl=Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True))
                return render(request,"info_table.html",{"ind":1,"nak":nakl,"products":products,"nakls":nakls_zakup,"names_zakup":names_zakup})
            elif url[3]=="consumption":
                nakl=Spis.objects.filter(is_removed=False)
                return render(request,"info_table.html",{"ind":2,"nak":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
        else:
            print("!!!!")
            from itertools import chain
            nak_id=request.POST.get("nak_id","")
            date=request.POST.get("date","")
            to=request.POST.get("to","")
            name=request.POST.get("name","")
            product=request.POST.get("product","")
            date=date if date!="" else d.date(2018,1,1)
            to=to if to!="" else datetime.today()
            print(date,to)
            '''if nak_id=="" and name=="" and product=="":
                print("!")
                if url[3]=="receipt":
                    nakl=Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True))
                    return render(request,"info_table.html",{"ind":1,"nak":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(is_removed=False)
                    #create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nak":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            '''
            if nak_id!="" and name!="" and product!="":
                print("$$$$$$")
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(purchase__username=name)&Q(is_delivered=True)&Q(name__name=product)&Q(nak_id=int(nak_id))&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(purchase__username=name)&Q(date__gte=date)&Q(is_accepted=True)&Q(date__lte=to)&Q(name__name=product)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(nak_id=int(nak_id))&Q(receiver__receiver=name)&Q(product_name=product))
                    #nakl=list(nakl)
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif nak_id!="" and name!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(purchase__username=name)&Q(is_delivered=True)&Q(nak_id=int(nak_id))&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=True)&Q(purchase__username=name)&Q(date__gte=date)&Q(date__lte=to)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(nak_id=int(nak_id))&Q(receiver__receiver=name))
                    #nakl=list(nakl)
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif nak_id!="" and product!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(name__name=product)&Q(nak_id=int(nak_id))&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=True)&Q(date__gte=date)&Q(date__lte=to)&Q(name__name=product)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(nak_id=int(nak_id))&Q(product_name=product))
                    #nakl=list(nakl)
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif name!="" and product!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(purchase__username=name)&Q(is_delivered=True)&Q(name__name=product)&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(purchase__username=name)&Q(is_accepted=True)&Q(date__gte=date)&Q(date__lte=to)&Q(name__name=product)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(receiver__receiver=name)&Q(product_name=product))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif name!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(purchase__username=name)&Q(is_delivered=True)&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(purchase__username=name)&Q(is_accepted=True)&Q(date__gte=date)&Q(date__lte=to)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(receiver__receiver=name))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif nak_id!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(nak_id=int(nak_id))&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(nak_id=nak_id)&Q(is_accepted=True)&Q(date__gte=date)&Q(date__lte=to)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(nak_id=int(nak_id)))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif product!="":
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(name__name=product)&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(date__gte=date)&Q(is_accepted=True)&Q(date__lte=to)&Q(name__name=product)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(product_name=product))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif date!="":
                print("HHH")
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(date__gte=date)&Q(is_accepted=True)&Q(date__lte=to)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(date__gte=date)&Q(date__lte=to))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})
            elif to!="":
                print("ZZZ")
                if url[3]=="receipt":
                    nakl=chain(Purchase.objects.filter(Q(is_returned=False)&Q(is_delivered=True)&Q(date__gte=date)&Q(date__lte=to)),Without_nakl.objects.filter(Q(date__gte=date)&Q(is_accepted=True)&Q(date__lte=to)))
                    nakl=list(nakl)
                    create_xls_search_results(1,nakl)
                    return render(request,"info_table.html",{"ind":1,"nakl":nakl,"products":products,"nakls":nakls_zakup,"names":names_zakup})
                elif url[3]=="consumption":
                    nakl=Spis.objects.filter(Q(is_removed=False)&Q(date__gte=date)&Q(date__lte=to))
                    create_xls_search_results(2,nakl)
                    return render(request,"info_table.html",{"ind":2,"nakl":nakl,"products":products,"nakls":nakls_spis,"names":names_spis})


@login_required
def buy_products(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if request.method=="POST":
        if j==3 or j==8:
            request.session['_old_post'] = request.POST
            nak_id=request.POST.get("nak_id")
            products=Purchase.objects.filter(nak_id=nak_id).order_by("name")
            #return render(request,"buy_products.html",{"products":products,"indic":0,"nak_id":nak_id})
            return redirect(f"/accounts/profile/buy_more_products?n={nak_id}")
        else:
            return redirect("/accounts/profile")
    else:
        if j==3 or j==8:
            nak_id=request.session.get('_old_post').get("nak_id")
            products=Purchase.objects.filter(nak_id=nak_id).order_by("name")
            sort=request.GET.get("sort")
            print(sort)
            if sort=="salers":
                sal=Salers.objects.all()
                sallers=sorted(set([s.saler.name for s in sal]))
                sorted_products={saller:[s.product.name for s in Salers.objects.filter(saler__name=saller)] for saller in sallers}
                return render(request,"buy_products.html",{"products":products,"sorted_products":sorted_products,"indic":1,"nak_id":nak_id})
            elif sort=="category":
                cat=Categories.objects.all()
                categories=[c.category for c in cat]
                print(categories)
                sorted_products={category:Purchase.objects.filter(Q(nak_id=nak_id)&Q(name__category__category=category)) for category in categories}
                del_keys=[]
                for key,value in sorted_products.items():
                    if len(value)==0:
                        del_keys.append(key)
                other_category=[]
                for p in Purchase.objects.filter(nak_id=nak_id):
                    for c in categories:
                        if p not in sorted_products[c] and p not in other_category:
                            other_category.append(p)
                other={"Прочее":other_category}
                for d in del_keys:
                    del sorted_products[d]
                sorted_products.update(other)
                #print("{}{}{}{}",sorted_products)
                return render(request,"buy_products.html",{"sorted_products":sorted_products,"indic":2,"nak_id":nak_id})
            else:
                #return render(request,"buy_products.html",{"products":products,"indic":0,"nak_id":nak_id})
                return redirect(f"/accounts/profile/buy_more_products?n={nak_id}")
        else:
            return redirect("/accounts/profile")


@login_required
def add_dop_money_for_purchase(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            types=DopTypes.objects.all()
            nak_id=request.GET.get("n")
            return render(request,"dop_types.html",{"types":types,"n":nak_id})
        else:
            d_type=int(request.POST.get("type"))
            money_type=DopTypes.objects.get(id=d_type)
            money=float(request.POST.get("summ"))
            if (money<=money_type.max_summ) and (money>=money_type.min_summ):
                money=round(float(money),3)
                nak_id=int(request.GET.get("n"))
                try:
                    DopMoney(nak_id=nak_id,dop_type=money_type,purchaser=request.user,money=money).save()
                except Exception as e:
                    print(e)
                return redirect("../")
            else:
                return render(request,"dop_types.html",{"indic":1,"min":money_type.min_summ,"max":money_type.max_summ,"types":DopTypes.objects.all()})



@login_required
def sorted_products(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if "s" in request.GET:
            n=request.GET.get("s")
            nak_id=int(request.GET.get("n"))
            another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0)&Q(is_ordered=False))
            name=Postavsh.objects.get(name=n)
            saler_other=Salers.objects.filter(Q(saler__name=name.name))
            saler_products=[s.product for s in saler_other]
            products=[an.name for an in another if an.name in saler_products]
            costs=[an.last_cost for an in another if an.name in saler_products]
            kolvo=[an.kolvo for an in another if an.name in saler_products]
            ids=[an.id for an in another if an.name in saler_products]
            srok=[datetime.strftime(an.min_srok,"%Y-%m-%d") for an in another if an.name in saler_products]
            summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
            all_summ=round(sum(summ),3)
            costs=[str(c).replace(",",".") for c in costs]
            kolvo=[str(c).replace(",",".") for c in kolvo]
            summ=[str(c).replace(",",".") for c in summ]
            return render(request,"buy_more_products.html",{"products":products,"saler":name.name,"costs":costs,"kolvo":kolvo,"ids":ids,"summ":summ,"all_summ":all_summ,"srok":srok,"range":range(len(products))})
        elif "c" in request.GET:
            nak_id=int(request.GET.get("n"))
            categ=request.GET.get("c")
            if categ=="Прочее":
                another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0)&Q(is_ordered=False)&Q(name__category=None))
            else:
                another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0)&Q(is_ordered=False)&Q(name__category__category=categ))
            products=[an.name for an in another]
            salers=[[Salers.objects.filter(product=an.name)] for an in another]
            costs=[an.last_cost for an in another]
            kolvo=[an.kolvo for an in another]
            ids=[an.id for an in another]
            srok=[datetime.strftime(an.min_srok,"%Y-%m-%d") for an in another]
            summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
            all_summ=round(sum(summ),3)
            costs=[str(c).replace(",",".") for c in costs]
            kolvo=[str(c).replace(",",".") for c in kolvo]
            summ=[str(c).replace(",",".") for c in summ]
            return render(request,"buy_more_products.html",{"products":products,"salers":salers,"ind":1,"costs":costs,"kolvo":kolvo,"ids":ids,"summ":summ,"all_summ":all_summ,"srok":srok,"range":range(len(products))})



@login_required
def buy_product(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if request.method=="GET":
        nak_id=request.GET.get("n")
        product_id=request.GET.get("id")
        #print("s" in request.GET)
        product=Purchase.objects.get(Q(nak_id=nak_id)&Q(id=product_id))
        #print("PPPPP",product.name)
        if "s" in request.GET:
            form=ZakupForm(s=request.GET.get("s"),salers_list=Salers.objects.filter(product=product.name))
        else:
            form=ZakupForm(salers_list=Salers.objects.filter(product=product.name))
        salers=Salers.objects.filter(product=product.name).order_by("last_cost")
        return render(request,"buy_product.html",{"product":product,"form":form,"salers":salers})
    elif request.method=="POST":
        f=True if "button_1" in request.POST else False
        nak_id=request.GET.get("n")
        product_id=request.GET.get("id")
        product=Purchase.objects.get(Q(nak_id=nak_id)&Q(id=product_id))
        srok=request.POST.get("srok")
        kol=request.POST.get("kol")
        summ=request.POST.get("cost")
        saler=request.POST.get("saler")
        #print("!!!!",saler)
        if saler==None:
            return redirect(f"/accounts/profile/buy_product?n={nak_id}&id={product_id}")
        days=round(float(kol)/product.name.rashod)
        #print(days)
        real_srok=datetime.today()+timedelta(days=days)
        #print(real_srok)
        '''if real_srok.date()<product.min_srok:
            allowed_kol=round((product.min_srok-datetime.strptime(srok,r"%Y-%m-%d").date()).days/product.name.rashod)
            if "s" in request.GET:
                form=ZakupForm(s=request.GET.get("s"),salers_list=Salers.objects.filter(product=product.name))
            else:
                form=ZakupForm(salers_list=Salers.objects.filter(product=product.name))
            return render(request,"buy_product.html",{"indic":1,"kol":allowed_kol,"product":product,"form":form})'''
        saler_name=Postavsh.objects.get(name=saler)
        product.srok=srok
        product.purchased_kol=round(float(kol),3)
        product.summ=round(float(summ),3)
        product.new_cost=round(float(summ)/float(kol),3)
        product.saler=saler_name
        product.purchase=request.user
        if not f:
            product.is_ordered=True
        product.save()
        b=Buyer_Balans.objects.get(buyer__username=request.user.username)
        b.balans-=round(float(summ),3)
        b.save()
        another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0))
        saler_other=Salers.objects.filter(Q(saler__name=saler))
        saler_products=[s.product for s in saler_other]
        #print(saler_products)
        another_products=[an for an in another if an.name in saler_products]
        #print("&&&&&&",another_products)
        print("FFFFF ",f)
        if f:
            try:
                last_cost=LastCost.objects.get(product=product.name.strip())
                cost=last_cost.cost
                last_cost.cost=round(float(summ)/float(kol),3)
                old_kol=last_cost.kol
                kol=float(kol)
                st=Stock.objects.get(name=product.name)
                av=(st.ostat*cost+summ)/(st.ostat+kol)
                print("@@@@",av)
                last_cost.average=av
                last_cost.average=round(last_cost.average,3)
                #last_cost.kol+=round(kol,3)
                #last_cost.kol=round(last_cost.kol,3)
                #if old_kol==0:
                #    last_cost.average=last_cost.cost
                #else:
                #    last_cost.average=last_cost.average-((last_cost.average-last_cost.cost)/last_cost.kol)
                #    last_cost.average=round(last_cost.average,3)
                #print((st.ostat*cost+summ)/(st.ostat+kol))
                last_cost.save()
            except Exception as e:
                text=f"Ошибка {e}\n{prod.name}\n{len(prod.name)}\n{len(prod.name.strip())}"
                requests.get(f"https://api.telegram.org/bot797654951:AAH5SQ-VroGR6_QaErkq0p3JD9LYqw7suMs/sendMessage?chat_id=145109083&text={text}")
                print(type(cost),type(kol))
                #LastCost(product=prod.name.strip(),cost=round(float(summ[i])/float(kol[i]),3),kol=round(kol[i],3),average=round(float(summ[i])/float(kol[i]),3)).save()
        #print("SSS",saler_other)
        if len(saler_other)!=0:
            saler_id=Postavsh.objects.get(name=saler).id
            return redirect(f"/accounts/profile/buy_more_products?n={nak_id}&s={saler_id}")
            #return render(request,"buy_product.html",{"another":another_products,"saler":saler_other[0],"product":product})
        else:
            return render(request,"buy_product.html",{"another":another_products,"product":product})

@login_required
def buy_more_products(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            nak_id=request.GET.get("n"," ")
            saler_id=request.GET.get("s"," ")
            if nak_id==" ":
                return redirect("/accounts/profile/")
            else:
                if saler_id!=" ":
                    nak_id,saler_id=int(nak_id),int(saler_id)
                    another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0)&Q(is_ordered=False)&Q(is_borrowed=False))
                    name=Postavsh.objects.get(id=saler_id)
                    saler_other=Salers.objects.filter(Q(saler__name=name.name))
                    saler_products=[s.product for s in saler_other]
                    products=[an.name for an in another if an.name in saler_products]
                    costs=[an.last_cost for an in another if an.name in saler_products]
                    kolvo=[an.kolvo for an in another if an.name in saler_products]
                    ids=[an.id for an in another if an.name in saler_products]
                    srok=[datetime.strftime(an.min_srok,"%Y-%m-%d") for an in another if an.name in saler_products]
                    summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
                    all_summ=round(sum(summ),3)
                    costs=[str(c).replace(",",".") for c in costs]
                    kolvo=[str(c).replace(",",".") for c in kolvo]
                    summ=[str(c).replace(",",".") for c in summ]
                    return render(request,"buy_more_products.html",{"products":products,"saler":name.name,"costs":costs,"kolvo":kolvo,"ids":ids,"summ":summ,"all_summ":all_summ,"srok":srok,"range":range(len(products)),"nak_id":nak_id})
                else:
                    nak_id = int(nak_id)
                    another=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0)&Q(is_ordered=False)&Q(is_borrowed=False))
                    salers={p.name:[Salers.objects.filter(product=p.name)] for p in another}
                    products=[an.name for an in another]
                    costs=[an.last_cost for an in another]
                    kolvo=[an.kolvo for an in another]
                    ids=[an.id for an in another]
                    pids=[an.name.id for an in another]
                    srok=[datetime.strftime(an.min_srok,"%Y-%m-%d") for an in another]
                    summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
                    all_summ=round(sum(summ),3)
                    costs=[str(c).replace(",",".") for c in costs]
                    kolvo=[str(c).replace(",",".") for c in kolvo]
                    summ=[str(c).replace(",",".") for c in summ]
                    return render(request,"buy_more_products.html",{"ind":2,"nak_id":nak_id,"pids":pids,"n":nak_id,"products":products,"salers":salers,"costs":costs,"kolvo":kolvo,"ids":ids,"summ":summ,"all_summ":all_summ,"srok":srok,"range":range(len(products))})

        else:
            #print(request.POST)
            if "button_1" in request.POST:
                f=1
            elif "button_3" in request.POST:
                f=3
            elif "button_4" in request.POST:
                f=4
            else:
                f=2
            check=dict(request.POST).get("check")
            products=dict(request.POST).get("products")
            saler=dict(request.POST).get("saler")
            costs=dict(request.POST).get("costs")
            kolvo=dict(request.POST).get("kolvo")
            summ=dict(request.POST).get("summ")
            check=check[1:]
            #date=dict(request.POST).get("date")
            for i in range(len(check)):
                if check[i]=="1":
                    prod=Purchase.objects.get(id=products[i])
                    #print(prod.name)
                    #d=datetime.strptime(date[i],"%Y-%m-%d").date()
                    cost=costs[i].replace(",",".")
                    kol=kolvo[i].replace(",",".")
                    summa=summ[i].replace(",",".")
                    #prod.srok=d
                    prod.purchased_kol=round(float(kol),3)
                    prod.summ=round(float(summa),3)
                    prod.new_cost=round(float(cost),3)
                    saler_name=Postavsh.objects.get(name=saler[i])
                    prod.saler=saler_name
                    prod.purchase=request.user
                    if f==2:
                        prod.is_ordered=True
                    else:
                        if f==3:
                            prod.is_borrowed=True
                        elif f==4:
                            prod.is_borrowed=False
                            b=Buyer_Balans.objects.get(buyer__username=request.user.username)
                            b.balans-=round(float(summa),3)
                            b.save()
                        elif f==1:
                                b=Buyer_Balans.objects.get(buyer__username=request.user.username)
                                b.balans-=round(float(summa),3)
                                b.save()
                        try:
                            last_cost=LastCost.objects.get(product=prod.name.strip())
                            cost=last_cost.cost
                            #print(i,len(summ),len(kol))
                            last_cost.cost=round(float(summa)/float(kol),3)
                            old_kol=last_cost.kol
                            kol=float(kol)
                            st=Stock.objects.get(name=prod.name)
                            av=(st.ostat*cost+float(summa))/(st.ostat+kol)
                            print("@@@@",av)
                            last_cost.average=av
                            last_cost.average=round(last_cost.average,3)
                            last_cost.save()
                        except Exception as e:
                            text=f"Ошибка {e}\n{prod.name}\n{len(prod.name)}\n{len(prod.name.strip())}"
                            requests.get(f"https://api.telegram.org/bot797654951:AAH5SQ-VroGR6_QaErkq0p3JD9LYqw7suMs/sendMessage?chat_id=145109083&text={text}")
                            print(type(cost),type(kol))
                            #LastCost(product=prod.name.strip(),cost=round(float(summ[i])/float(kol[i]),3),kol=round(kol[i],3),average=round(float(summ[i])/float(kol[i]),3)).save()
                    prod.save()
                else:
                    continue
            if f!=4:
                return redirect("/accounts/profile/buy_products")
            else:
                return redirect(f"/accounts/profile/list_of_debts/")

@login_required
def ordered_list(request):
    j=request.user.roles.role
    if j==3 or j==8:
        nak_id=int(request.GET.get("n"))
        ordered=Purchase.objects.filter(Q(nak_id=nak_id)&Q(is_ordered=True))
        salers=[]
        salers_id=[]
        for s in ordered:
            if s.saler.id not in salers_id:
                salers.append(s)
                salers_id.append(s.saler.id)
        return render(request,"orderedproducts_sorted_list.html",{"salers":salers,"nak_id":nak_id})

@login_required
def ordered_table(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            nak_id=int(request.GET.get("n"))
            saler_id=int(request.GET.get("s"))
            products=Purchase.objects.filter(Q(nak_id=nak_id)&Q(saler__id=saler_id)&Q(is_ordered=True))
            name=Postavsh.objects.get(id=saler_id)
            prod=[p.name for p in products]
            costs=[p.last_cost for p in products]
            kolvo=[p.kolvo for p in products]
            srok=[p.min_srok for p in products]
            ids=[p.id for p in products]
            summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
            all_summ=round(sum(summ),3)
            costs=[str(c).replace(",",".") for c in costs]
            kolvo=[str(c).replace(",",".") for c in kolvo]
            summ=[str(c).replace(",",".") for c in summ]
            return render(request,"buy_more_products.html",{"products":prod,"saler":name.name,"costs":costs,"kolvo":kolvo,"ids":ids,"summ":summ,"all_summ":all_summ,"srok":srok,"range":range(len(prod)),"indic":1})
        else:
            nak_id=int(request.GET.get("n"))
            saler_id=int(request.GET.get("s"))
            '''products=Purchase.objects.filter(Q(nak_id=nak_id)&Q(saler__id=saler_id))
            name=Postavsh.objects.get(id=saler_id)
            prod=[p.name for p in products]
            costs=[p.last_cost for p in products]
            kolvo=[p.kolvo for p in products]
            srok=[p.min_srok for p in products]
            ids=[p.id for p in products]
            summ=[round(costs[i]*kolvo[i],3) for i in range(len(costs))]
            all_summ=round(sum(summ),3)
            costs=[str(c).replace(",",".") for c in costs]
            kolvo=[str(c).replace(",",".") for c in kolvo]
            summ=[str(c).replace(",",".") for c in summ]'''
            check=dict(request.POST).get("check")
            products=dict(request.POST).get("products")
            saler=dict(request.POST).get("saler")
            costs=dict(request.POST).get("costs")
            kolvo=dict(request.POST).get("kolvo")
            summ=dict(request.POST).get("summ")
            #print(check)
            check=check[1:]
            for i in range(len(check)):
                if check[i]=="1":
                    prod=Purchase.objects.get(id=products[i])
                    print(prod.name)
                    #d=datetime.strptime(date[i],"%Y-%m-%d").date()
                    cost=costs[i].replace(",",".")
                    kol=kolvo[i].replace(",",".")
                    summa=summ[i].replace(",",".")
                    #prod.srok=d
                    prod.purchased_kol=round(float(kol),3)
                    prod.summ=round(float(summa),3)
                    prod.new_cost=round(float(cost),3)
                    saler_name=Postavsh.objects.get(name=saler[i])
                    prod.saler=saler_name
                    prod.purchase=request.user
                    prod.is_ordered=False
                    prod.save()
                    print(prod.is_ordered)
                    b=Buyer_Balans.objects.get(buyer__username=request.user.username)
                    b.balans-=round(float(summa),3)
                    b.save()
            return redirect(f"/accounts/profile/buy_products/table?n={nak_id}&s={saler_id}")



@login_required
def info(request):
    j=request.user.roles.role
    if j==3 or j==8:
        month=datetime.now().month
        nakls=Purchase.objects.filter(date__month=month)
        nakls_number=[]
        for nak in nakls:
            if nak.nak_id not in nakls_number:
                nakls_number.append(nak.nak_id)
        all_n=len(nakls_number)
        vip=0
        nevip=0
        nepoln=0
        for nak_id in nakls_number:
            v=Purchase.objects.filter(Q(purchased_kol__gt=0.0)&Q(nak_id=nak_id))
            if len(v)==0:
                nevip+=1
                continue
            else:
                nev=Purchase.objects.filter(Q(purchased_kol=0.0)&Q(nak_id=nak_id))
                if len(nev)==0:
                    vip+=1
                    continue
                else:
                    nepoln+=1
                    continue
        return render(request,"info.html",{"all":all_n,"poln":vip,"nepoln":nepoln,"nevip":nevip})

def info_naklad(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            if request.GET.get("e")=="1":
                return render(request,"info_naklad.html",{"indic":0,"e":1})
            return render(request,"info_naklad.html",{"indic":0})
        else:
            nak_id=request.POST.get("nak_id")
            date=request.POST.get("date")
            if nak_id=="" and date=="":
                return redirect("/accounts/profile/info/naklad")
            elif nak_id!="":
                products=Purchase.objects.filter(nak_id=nak_id)
                if len(products)==0:
                    return redirect("/accounts/profile/info/naklad?e=1")
            elif date!="":
                #date=datetime.strptime(date,"%Y-%m-%d").date()
                products=Purchase.objects.filter(date=date)
                if len(products)==0:
                    return redirect("/accounts/profile/info/naklad?e=1")
            status="Принята" if products[0].is_accepted==True else "Не принята"
            all_p=len(products)
            nak_id=products[0].nak_id
            v=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol__gt=0.0))
            vip=len(v)
            nevip=all_p-vip
            summ=0.0
            for product in products:
                summ+=product.summ
            return render(request,"info_naklad.html",{"indic":1,"products":products,"all":all_p,"vip":vip,"nevip":nevip,"summ":summ,"nak_id":nak_id,"date":products[0].date,"status":status})

def info_products(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            products=Products.objects.filter(prigot=False)
            return render(request,"info_product.html",{"indic":0,"products":products})
        else:
            product=request.POST.get("product")
            if "min_date" not in request.POST:
                srok=Purchase.objects.filter(name__name=product).order_by("date")
                min_srok=srok[0].date
                max_srok=srok[len(srok)-1].date
                print(request.POST)
                return render(request,"info_product_1.html",{"s_product":product,"min_date":str(min_srok),"max_date":str(max_srok)})
            else:
                min_date=request.POST.get("min_date")
                max_date=request.POST.get("max_date")
                products=Purchase.objects.filter(Q(date__range=[min_date,max_date])&Q(name__name=product))
                kolvo=[]
                for p in products:
                    if p.fact_kol==None:
                        p.fact_kol=0.0
                    kolvo.append(p.fact_kol)
                start=datetime.strptime(min_date,"%Y-%m-%d")
                end=datetime.strptime(max_date,"%Y-%m-%d")
                date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
                days=[float(d.strftime("%d.%m")) for d in date_generated]
                name=Products.objects.get(name=product)
                all_k=0.0
                for p in products:
                    if p.fact_kol==None:
                        p.fact_kol=0.0
                    all_k+=float(p.fact_kol)
                all_k=round(all_k,3)
                return render(request,"info_product_1.html",{"s_product":product,"name":name,"products":products,"diapazon":days,"data":kolvo,"indic":0,"all":all_k,"min_date":min_date,"max_date":max_date})

@login_required
def add_product(request):
    j=request.user.roles.role
    if j==3 or j==8:
        if request.method!="POST":
            nak=Purchase.objects.filter(is_accepted_zakup=True)
            nak_id=max([int(n.nak_id) for n in nak])
            products=Products.objects.filter(prigot=False)
            return render(request,"add_product.html",{"nak_id":nak_id,"products":products,"edizm":Units.objects.all()})
        else:
            nak_id=int(request.POST.get("nak_id"))
            date=Purchase.objects.filter(nak_id=nak_id)[0].date
            print(date,type(date))
            name=request.POST.get("product")
            kol=float(request.POST.get("kolvo"))
            try:
                product=Products.objects.get(name=name)
            except ObjectDoesNotExist:
                products=Products.objects.filter(prigot=False)
                return render(request,"add_product.html",{"nak_id":nak_id,"products":products,"indic":1})
            days=round(kol/product.rashod)
            now=datetime.today()
            srok=now+timedelta(days=days)
            try:
                last_cost=LastCost.objects.get(product=product).cost
            except ObjectDoesNotExist:
                last_cost=0.0
            Purchase(nak_id=nak_id,name=product,kolvo=kol,min_srok=srok,last_cost=last_cost,fact_kol=0.0,date=date,is_accepted_zakup=True).save()
            return redirect("/accounts/profile/buy_products")


@login_required
def add_new_product(request):
    j=request.user.roles.role
    if j==3 or j==8 or j==8:
        if request.method=="POST":
            name=request.POST.get("name")
            edizm=request.POST.get("edizm")
            ed=Units.objects.get(id=int(edizm))
            Products(name=name,edizm=ed,prigot=False,maks_zakup=6,min_zakup=3,rashod=1).save()
            return redirect("/accounts/profile/buy_products/add_product")

@login_required
def list_of_debts(request):
    j=request.user.roles.role
    if j==3 or j==8 or j==8:
        if request.method!="POST":
            nakl=Purchase.objects.filter(Q(is_borrowed=True)&Q(purchase=request.user)).order_by("date")
            return render(request,"list_of_debts.html",{"nakl":nakl})

@login_required
def borrowed_products(request):
    j=request.user.roles.role
    if j==3 or j==8 or j==8:
        if request.method!="POST":
            nak_id=request.GET.get("n")
            nakls=Purchase.objects.filter(Q(purchase=request.user)&Q(is_borrowed=True)&Q(nak_id=nak_id))
            ids=[n.id for n in nakls]
            products=[n.name for n in nakls]
            s=[n.saler for n in nakls]
            costs=[n.last_cost for n in nakls]
            kolvo=[n.purchased_kol for n in nakls]
            srok=[datetime.strftime(n.min_srok,"%Y-%m-%d") for n in nakls]
            all_summ=1
            for i in range(len(costs)):
                all_summ+=round(float(costs[i])*float(kolvo[i]),3)
            return render(request,"borrowed_products.html",{"all_summ":all_summ,"ids":ids,"products":products,"s":s,"costs":costs,"kolvo":kolvo,"srok":srok,"range":range(nakls.count())})

@login_required
def append_product_for_saler(request):
    j=request.user.roles.role
    if j==3 or j==8:
        product=Products.objects.get(id=int(request.GET.get("id")))
        salers=Postavsh.objects.all().order_by("id")
        n=request.GET.get("n")
        pid=request.GET.get("pid")
        if request.method=="POST":
            diction=request.POST.dict()
            inform=[(k,diction.get(k)) for k in diction.keys() if k.startswith("saler")]
            print(inform)
            for info in inform:
                saler,cost=info
                if cost!="":
                    saler_id=int(saler.split("_")[1])
                    cost=float(cost)
                    print(saler_id,cost)
                    try:
                        s=Salers.objects.get(Q(saler__id=saler_id)&Q(product=product))
                        s.product=product
                        s.last_cost=round(cost,3)
                        s.save()
                    except ObjectDoesNotExist:
                        Salers(saler=Postavsh.objects.get(id=saler_id),product=product,last_cost=round(cost,3)).save()
                else:
                    print("!!!")
                    continue
            return redirect(f"../buy_more_products?n={n}")
        else:
            form=Add_Product_for_saler(salers)
            return render(request,"new_product.html",{"form":form,"id":product.id,"n":n,"pid":pid})

@login_required
def append_saler(request):
    j=request.user.roles.role
    if j==3 or j==8:
        n=request.GET.get("n")
        pid=request.GET.get("pid")
        pr_id=request.GET.get("id")
        if request.method=="POST":
            product=Products.objects.get(id=int(pr_id))
            name=request.POST.get("name")
            firm_name=request.POST.get("firm_name")
            phone=request.POST.get("phone")
            place=request.POST.get("place")
            cost=float(request.POST.get("cost"))
            postavsh=Postavsh(name=name,firm_name=firm_name,place=place,contact=phone)
            postavsh.save()
            Salers(product=product,last_cost=round(cost,3),saler=postavsh).save()
            return redirect("accounts/profile/buy_products")
        else:
            form=Add_Saler()
            return render(request,"new_saler.html",{"form":form})

@login_required
def accept_products(request):
    j=request.user.roles.role
    if request.method=="GET" and j==3 or j==8:
        nak_id=request.GET.get("n")
        nakls=Purchase.objects.filter(nak_id=nak_id).update(is_accepted_zakup=True)
        return redirect("/accounts/profile")


@login_required
def zagot_product(request):
    j=request.user.roles.role
    n=request.GET.get("n")
    pid=request.GET.get("id")
    product=Nakl_for_zagot.objects.get(Q(nak_id=n)&Q(id=pid))
    dop_info=Ingredients_dop_info.objects.get(product=product.name)
    srok=float(dop_info.srok)
    procent=float(dop_info.procent)
    now=datetime.now()
    d=now+timedelta(hours=srok)
    if j==4 or j==8:
        if request.method=="POST":
            kol=request.POST.get("product")
            k=int(request.POST.get("shtr_kol"))
            kk=k if k>0 else 1
            ingr=Ingredients.objects.filter(Q(product__name=product.name))
            spis_ingr=[prod.ingr.name for prod in ingr]
            bar=generate_barcode(product.name.id,d.date())
            product.pkolvo+=round(float(kol),3)
            product.is_maked=True
            product.user=Zagot_types.objects.filter(user=request.user)[0]
            product.srok=d
            product.shtrih=bar
            product.save()
            try:
                hb=Harvester_Barcodes.objects.get(Q(barcode=bar)&Q(nak_id=int(n))&Q(product_id=int(pid)))
            except ObjectDoesNotExist:
                Harvester_Barcodes(nak_id=int(n),product_id=int(pid),barcode=bar).save()
            for ingr in spis_ingr:
                stock=Harvester_Stock.objects.get(Q(user=request.user)&Q(product=Products.objects.get(name=ingr)))
                stock.kol-=round(float(request.POST.get(ingr)),3)
                stock.save()
                if stock.kol<=0.0:
                    stock.delete()
                Rashod_zagot(nak_id=product,name=Products.objects.get(name=ingr),kol=float(request.POST.get(ingr))).save()
            for i in range(kk):
                print_barcode(request.user.username,product.name.name,now,d,bar)
            trash2()
            return redirect("/accounts/profile/zagot/list")
        else:
            procent=Ingredients_dop_info.objects.get(product=product.name).procent
            minimum=product.tkolvo-((product.tkolvo*procent)/10)
            if product.pkolvo>=minimum:
                code=product.shtrih
                return render(request,"zagot_product.html",{"indic":0,"product":product,"code":code})
            else:
                ingr=Ingredients.objects.filter(Q(product__name=product.name))
                spis_ingr=[prod.ingr.name for prod in ingr]
                print("ss=",spis_ingr)
                print("PP=",product.tkolvo)
                ingr_kolvo=[round(float(ingrr.kolvo)*float(product.tkolvo),3) for ingrr in ingr]
                form=ZagotForm(Ingredients.objects.filter(Q(product__name=product.name)))
                return render(request,"zagot_product.html",{"indic":1,"form":form,"product":product,"range":range(len(spis_ingr)),"ingrs":spis_ingr,"needs":ingr_kolvo})
    else:
        return redirect("/accounts/profile")

@login_required
def accept_zagot(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==4 or j==8:
        products=Nakl_for_zagot.objects.filter(is_accepted=False)
        products.update(is_accepted=True)
        form=Zagot(Nakl_for_zagot.objects.filter(Q(is_maked=False)))
        return redirect("/accounts/profile")
        #return render(request,roles[j],{"job":job,"form":form,"indic":0})
    else:
        return redirect("/accounts/profile")


@login_required
def accept_zagot_products(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==4 or j==8:
        if request.method!="POST":
            nak_id=request.GET.get("n")
            e=int(request.GET.get("e",0))
            products=Zagot_products.objects.filter(Q(nak_id=nak_id)&Q(user__user__username=request.user.username)&Q(status=False)).order_by("product")
            print(products)
            return render(request,"accept_products.html",{"products":products,"nak_id":nak_id,"e":e})
        else:
            print(request.POST.get('kolvo'))
            print(request.POST)
            kolvo=dict(request.POST).get("kolvo")
            nak_id=request.GET.get("n")
            print(nak_id)
            try:
                kolvo=[float(k.replace(",",".")) for k in kolvo]
            except ValueError:
                return redirect(f"/accounts/profile/zagot/accept_products?n={nak_id}&e=1")
            zagot=Zagot_products.objects.filter(Q(nak_id=nak_id)&Q(user__user__username=request.user.username)&Q(status=False)).order_by("product")
            print("###",zagot)
            for i in range(len(zagot)):
                #print(zagot_products[i].product,zagot_products[i].kol,zagot_products[i].kolvo)
                zagot[i].kolvo=kolvo[i]
                zagot[i].status=True
                zagot[i].save()
                Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)&Q(user__user__username=request.user.username)&Q(is_taken=False)&Q(name=zagot[i].product)).update(is_taken=True)
            return redirect("/accounts/profile/")
            #print(kolvo)



@login_required
def zagot_list(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if request.method=="POST":
        nak_id=request.POST.get("nak_id")
        request.session["_old_post"]=request.POST
    else:
        nak_id=request.session.get("_old_post").get("nak_id")
    products=Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)&Q(user__user=request.user)).order_by("name")
    #products=Nakl_for_zagot.objects.filter(Q(nak_id=nak_id)).order_by("name")
    products.update(is_accepted=True)
    request.session['_old_post'] = request.POST
    prod={}
    for product in products:
        status=" Не хватает продуктов:"
        ingreds=Ingredients.objects.filter(product=product.name)
        kolvo={i.ingr:round(i.kolvo*product.tkolvo,3) for i in ingreds}
        f=True
        for ingr,kol in kolvo.items():
            if kol>0.0:
                try:
                    st=Harvester_Stock.objects.get(Q(product=ingr)&Q(user=request.user))
                except ObjectDoesNotExist:
                    f=False
                    status+=f"{ingr.name}({kol}), "
                    continue
                if st.kol<kol:
                    f=False
                    status+=f"{ingr.name}({kol-st.kol}), "
            else:
                continue
        if f:
            prod[product]=""
        else:
            prod[product]=status
    print(prod)
    return render(request,"zagot_list.html",{"job":job,"products":prod})

def barcode_image_to_text(name):
    #with open(name,"rb") as f:
    try:
        barcode=decode(Image.open(name))
        if len(barcode)>0:
            bar=barcode[0].data.decode("utf-8")
            return bar
        else:
            return "error"
    except Exception:
        return "error"

@login_required
def decode_barcode_from_image(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if request.method=="POST" and (j==1 or j==8 or j==8):
        from django.http import JsonResponse
        file=request.FILES['barcode']
        bar=barcode_image_to_text(file)
        print(bar)
        if len(bar)==13:
            bar=bar[1:]
        return JsonResponse({"result":bar})

# !!!!!!!!!!!!!!!!!!!!!!!

@login_required
def admin_view(request):
    if request.user.is_superuser:
        ingredients=Ingredients.objects.all()
        ing_names,ing=[],[]
        for ingred in ingredients:
            if ingred.product.name not in ing_names:
                print(ingred.product.name)
                ing_names.append(ingred.product.name)
                ing.append(ingred)
        return render(request,"admin_list.html",{"title":"Ингридиенты","f":1,"ingrs":ing})
    else:
        return HttpResponseForbidden("Отказано в доступе")

@permission_required("roles.add_ingridients")
def add_ingr(request):
    k=request.GET.get('k')
    print("k=",k)
    form=AdminForm(k,Products.objects.filter(prigot=True),Products.objects.all())
    last_k=int(k)-1 if int(k)-1>0 else 1
    if request.method=="POST":
        product=Products.objects.get(name=request.POST.get("product"))
        p_id=product.id
        srok=float(request.POST.get("srok"))
        procent=float(request.POST.get("procent"))
        Ingredients_dop_info(product=product,srok=srok,procent=procent).save()
        for i in range(int(k)-1):
            ingr=request.POST.get(f"ingr_{i+1}")
            print("ungr=",ingr)
            idd=Products.objects.get(name=ingr)
            print("idd ",idd)
            kol=request.POST.get(f"ingr_kol_{i+1}")
            Ingredients(product=product,ingr=idd,kolvo=kol).save()
        return redirect(f"../edit/?id={p_id}&k={int(k)}")
    else:
        return render(request,"admin_template.html",{"form":form,"indic":1,"new_k":int(k)+1,"last_k":last_k})

@permission_required("roles.change_ingridients")
def edit_ingr(request):
    p_id=request.GET.get('id')
    product=Products.objects.get(id=p_id)
    try:
        dop=Ingredients_dop_info.objects.get(product=product)
    except ObjectDoesNotExist:
        dop=Ingredients_dop_info(product=product)
        dop.save()
    ingredients=Ingredients.objects.filter(product=product)
    ing_ingrs={ing:ing.ingr for ing in ingredients}
    ing_kol={ing:ing.kolvo for ing in ingredients}
    ids=""
    for ingrr in ingredients:
        ids+=(str(ingrr.id)+",")
    len_i=len(ingredients)
    k=int(request.GET.get('k',0))
    ind=1
    new_k=k+1
    counter=k
    if k==0:
        ind=0
        k=len(ingredients)+1
        new_k=k
        counter=len(ingredients)
    last_k=int(k)-1 if int(k)-1>0 else 1
    if request.method=="POST":
        prod=Products.objects.get(name=request.POST.get("product"))
        srok=round(float(request.POST.get("srok")),3)
        procent=float(request.POST.get("procent"))
        print("$$$$$$",procent)
        procent=round(procent,3)
        if dop.srok!=srok:
            dop.srok=srok
            dop.save()
        if dop.procent!=procent:
            dop.procent=procent
            dop.save()
        for i in range(counter-1):
            print("i=",i)
            ingr=request.POST.get(f"ingr_{i+1}")
            print("ingr=",ingr)
            idd=Products.objects.get(name=ingr)
            kol=request.POST.get(f"ingr_kol_{i+1}")
            if product!=prod:
                ingred=Ingredients.objects.get(Q(product=product)&Q(ingr=idd))
                ingred.product=prod
                ingred.save()
                try:
                    dopp=Ingredients_dop_info.objects.get(product=prod)
                    dopp.srok=srok
                    dopp.procent=procent
                    dop.delete()
                    dopp.save()
                except ObjectDoesNotExist:
                    dop.delete()
                    Ingredients(product=prod,srok=srok,procent=procent).save()
            else:
                ingred=Ingredients.objects.filter(product=product)
                for j in range(i,k-1):
                    try:
                        ing=ingred[j]
                        ingg=ing_ingrs.get(ing,0)
                        if ingg!=0:
                            if ingg!=idd:
                                print("!!!")
                                print(ingg,idd)
                                ing.ingr=idd
                            else:
                                print("???")
                                print(type(ingg),type(idd))
                        kkol=ing_kol.get(ing,0)
                        if kkol!=0:
                            if kkol!=float(kol):
                                print(33333)
                                ing.kolvo=round(float(kol),3)
                        ing.save()
                        break
                    except Exception:
                        Ingredients(product=product,ingr=idd,kolvo=round(float(kol),3)).save()
                data={"product":product.name}
        ids=''
        for i in ingredients:
            ids+=(str(i.id)+',')
        return redirect(f"../edit/?id={p_id}&k={new_k-1}")
    else:
        data={"product":product.name}
        dop_info={"srok":dop.srok,"procent":dop.procent}
        ids=''
        for i in ingredients:
            ids+=(str(i.id)+',')
        print(ids)
        d={f"ingr_{i+1}":ingredients[i].ingr.name for i in range(len_i)}
        d2={f"ingr_kol_{i+1}":ingredients[i].kolvo for i in range(len_i)}
        data.update(dop_info)
        data.update(d)
        data.update(d2)
        form=AdminForm(initial=data,k=k-1,product=Products.objects.filter(prigot=True),ingreds=Products.objects.all()) if ind==0 else AdminForm(initial=data,k=k,product=Products.objects.filter(prigot=True),ingreds=Products.objects.all())
        return render(request,"admin_template.html",{"form":form,"indic":0,"new_k":new_k,"last_k":last_k,"p_id":p_id,"len_i":len_i,"id":ids,"ingredients":ingredients})

@permission_required("roles.delete_ingridients")
def delete_ingr(request):
    pid=request.GET.get('pid')
    print("!!!!",pid)
    ing_ids=request.GET.get('id').split(",")
    del ing_ids[-1]
    for ing_id in ing_ids:
        Ingredients.objects.get(id=int(ing_id)).delete()
    if len(Ingredients.objects.filter(product__id=int(pid)))==0:
        return redirect("/admin/roles/ingredients")
    else:
        return redirect(f"/admin/roles/ingredients/edit/?id={pid}")


#!!!!!!!!!!!!!!!

@login_required
def admin_view_3(request):
    if request.user.is_superuser:
        zakupshiki=User.objects.filter(roles__role=3)
        return render(request,"admin_list.html",{"title":"Закупщики","f":3,"postavshiki":pos})
    else:
        return HttpResponseForbidden("Отказано в доступе")

@permission_required("roles.add_salers")
def add_saler(request):
    k=request.GET.get('k')
    form=AdminForm3(k)
    last_k=int(k)-1 if int(k)-1>0 else 1
    if request.method=="POST":
        saler=request.POST.get("saler")
        for i in range(int(k)):
            product=request.POST.get(f"prod_{i+1}")
            print("product ",product)
            cost=round(float(request.POST.get(f"prod_cost_{i+1}")),3)
            Salers(saler=saler,product=product,last_cost=cost).save()
        return redirect("..")
    else:
        return render(request,"admin_template.html",{"form":form,"indic":1,"new_k":int(k)+1,"last_k":last_k})

@permission_required("roles.delete_ingridients")
def delete_saler(request):
    ing_ids=request.GET.get('id').split(",")
    del ing_ids[-1]
    for ing_id in ing_ids:
        Ingredients.objects.get(id=int(ing_id)).delete()
    return redirect("..")


