from django.shortcuts import render
from django.http import Http404
from .models import *
from .tables import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django_tables2 import RequestConfig
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

nk_id={}
now_id={}
now_id_zakup={}
nk_id_zakup={}

roles={
    1:"sklad.html",
    2:"kassir.html",
    3:"zakup.html",
    4:"zagotov.html",
    5:"pizzamaker.html",
    6:"dostavka.html",
    7:"pizzakassir.html"
}

# Create your views here.
@login_required
def profile(request):
    n=request.user.first_name
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    if j==1:
        table=StockTable(Stock.objects.all())
        RequestConfig(request).configure(table)
        return render(request,roles[j],{"user":n,"job":job,"table":table})
    elif j==3:
        if request.method!="POST":
            print(1111111111111111111)
            form=Zakup()
            products=Purchase.objects.filter(is_accepted=False)
            table=ZakupTable(products)
            RequestConfig(request).configure(table)
            #return render(request,"zakup.html",{"form":form})
            return render(request,"zakup.html",{"job":job,"form":form,"table":table})
    elif j==4:
        if request.method=="POST":
            #print(request.POST)
            form_qict=request.POST.dict()
            for key, value in form_qict.items():
                if value=="Отправить":
                    prod_id=key
            kolvo=form_qict[f"product_{prod_id}"]

            #button=str(request.body).split("&")[-1]
            #prod_id=button.split("=")[0].split("_")[-1]
            #print(prod_id)
        else:
            zagotovka=Nakl_for_zagot.objects.filter(~Q(is_accepted=True))
            table=ZagotTable(zagotovka)
            ids=[product.id for product in zagotovka]
            products=[product.name for product in zagotovka]
            kol=[product.tkolvo for product in zagotovka]
            forms=[]
            for i in range(len(ids)):
                forms.append(ZagotForm(ids[i],products[i]))
            print(forms)
            return render(request,roles[j],{"indic":1,"forms":forms,"kol":kol,"products":products,"job":job,"range":range(len(ids)),"table":table,"ids":ids})
    else:
        return render(request,roles[j],{"user":n,"job":job})

@login_required
def list_naklad(request):
    id=request.user.id
    naklad=Purchase.objects.all()
    ch=[n.nak_id for n in naklad]
    ch=set(ch)
    naklad=list(ch)
    return render(request,"list_naklad.html",{"naklad":naklad})

@login_required
def get_products(request):
    if request.method=="POST":
        j=request.user.roles.role
        if j==1:
            n_id=now_id.get(request.user.id,0)
            if n_id!=0:
                kol=request.POST.get("kol")
                srok=request.POST.get("srok")
                prod=Purchase.objects.get(id=n_id)
                prod.fact_kol=kol
                prod.srok=srok
                prod.is_delivered=True
                prod.is_accepted=True
                prod.save()
                Codes(prod).save()
                name=prod.name
                sk=Stock.objects.get(name=name)
                sk.kolvo=kol
                sk.ostat+=float(kol)
                sk.save()
            if nk_id.get(request.user.id,0)==0:
                nak_id=request.POST.get("nak_id")
                nk_id[request.user.id]=nak_id
            else:
                nak_id=nk_id[request.user.id]
            print(nak_id,n_id)
            products=Purchase.objects.filter(Q(nak_id=nak_id)&Q(id__gt=n_id)&Q(is_delivered=False))
            table=NaklTable(Purchase.objects.all())
            RequestConfig(request).configure(table)
            if len(products)==0:
                return render(request,"sklad_succes.html",{"table":table})
            else:
                table=NaklTable(Purchase.objects.all())
                RequestConfig(request).configure(table)
                form=GetForm()
                n_id=products[0].id
                now_id[request.user.id]=n_id
                print(n_id)
                product=products[0].name
                print(product)
                link=product.image
                print(link)
                return render(request,"get_products.html",{"table":table,"link":link,"product":product,"form":form})
        else:
            raise Http404
    else:
        j=request.user.roles.role
        if j==1:
            form=NaklForm()
            return render(request,"get_nak_id.html",{"form":form})
        else:
            raise Http404

@login_required
def spis(request):
    j=request.user.roles.role
    job=Roles.choices[j-1][1]
    st=Stock.objects.filter(ostat__gt=-0.0)
    table=StockTable(st)
    if request.method=="POST":
        kol=request.POST.get("kol")
        name=request.POST.get("name")
        rec=request.POST.get("receiv")
        name,shtrih=name.replace(" ","").split("|")
        codes=Codes.objects.filter(name=Products.objects.get(name=name))
        f_c=True
        cods=[int(c.shtrih) for c in codes]
        for cod in cods:
            if cod<int(shtrih):
                f_c=False
                break
        if f_c:
            stk=Stock.objects.get(name=Products.objects.get(name=name))
            codd=Codes.objects.get(shtrih=shtrih)
            if stk.ostat<float(kol):
                return render(request,"spis1.html",{"text":"Недостаточно на складе"})
            else:
                stk.ostat-=float(kol)
                codd.kolvo-=float(kol)
                stk.save()
                codd.save()
                nakl=Spis(product=name,kol=kol,receiver=Receivers.objects.get(receiver=rec))
                nakl.save()
                messages.success(request,"Списано")
                return render(request,"spis1.html",{"text":"Списано"})
        else:
            return render(request,"spis1.html",{"text":"Отказано!Вы пытаетесь списать более позднюю партию."})

    else:
        form=SpisForm()
        return render(request,"spis.html",{"job":job,"form":form,"table":table})

@login_required
def buy_products(request):
    j=request.user.roles.role
    if request.method=="POST":
        if j==3:
            n_id=now_id_zakup.get(request.user.id,0)
            if n_id!=0:
                kol=request.POST.get("kol")
                summ=request.POST.get("cost")
                srok=request.POST.get("srok")
                prod=Purchase.objects.get(id=n_id)
                prod.purchased_kol=kol
                prod.new_cost=summ
                prod.summ=float(summ)*float(kol)
                prod.save()
                try:
                    last_cost=LastCost.objects.get(product=prod.name)
                    last_cost.cost=summ
                    last_cost.save()
                except ObjectDoesNotExist:
                    LastCost(product=prod.name,cost=last_cost).save()
                name=prod.name
            if nk_id_zakup.get(request.user.id,0)==0:
                nak_id=request.POST.get("nak_id")
                nk_id_zakup[request.user.id]=nak_id
            else:
                nak_id=nk_id_zakup[request.user.id]
            print(n_id,nak_id)
            products=Purchase.objects.filter(Q(nak_id=nak_id)&Q(id__gt=n_id)&Q(is_delivered=False))
            table=NaklTable(Purchase.objects.all())
            RequestConfig(request).configure(table)
            if len(products)==0:
                return render(request,"zakup_succes.html",{"table":table})
            else:
                table=NaklTable(Purchase.objects.all())
                RequestConfig(request).configure(table)
                form=ZakupForm()
                n_id=products[0].id
                now_id_zakup[request.user.id]=n_id
                product=products[0].name
                link=product.image
                return render(request,"get_products.html",{"table":table,"link":link,"product":product,"form":form})
        else:
            raise Http404
    else:
        j=request.user.roles.role
        if j==3:
            form=Zakup()
            return render(request,"zakup.html",{"form":form})
        else:
            raise Http404

