from django.shortcuts import render
from django.http import Http404
from .models import *
from .tables import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django_tables2 import RequestConfig
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
        table=StockTable(Stock.st.all())
        RequestConfig(request).configure(table)
        return render(request,roles[j],{"user":n,"job":job,"table":table})
    elif j==3:
        if request.method!="POST":
            print(1111111111111111111)
            form=Zakup()
            products=Purchase.pur.filter(is_accepted=False)
            table=ZakupTable(products)
            RequestConfig(request).configure(table)
            #return render(request,"zakup.html",{"form":form})
            return render(request,"zakup.html",{"job":job,"form":form,"table":table})
    else:
        return render(request,roles[j],{"user":n,"job":job})

@login_required
def list_naklad(request):
    id=request.user.id
    naklad=Purchase.pur.all()
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
                shtrih=request.POST.get("shtrih")
                srok=request.POST.get("srok")
                prod=Purchase.pur.get(id=n_id)
                prod.fact_kol=kol
                prod.shtrih=shtrih
                prod.srok=srok
                prod.is_delivered=True
                prod.is_accepted=True
                prod.save()
                name=prod.name
                sk=Stock.st.get(name=name)
                sk.kolvo=kol
                sk.ostat+=float(kol)
                sk.shtrih=shtrih
                sk.save()
            if nk_id.get(request.user.id,0)==0:
                nak_id=request.POST.get("nak_id")
                nk_id[request.user.id]=nak_id
            else:
                nak_id=nk_id[request.user.id]
            print(nak_id,n_id)
            products=Purchase.pur.filter(Q(nak_id=nak_id)&Q(id__gt=n_id)&Q(is_delivered=False))
            table=NaklTable(Purchase.pur.all())
            RequestConfig(request).configure(table)
            if len(products)==0:
                return render(request,"sklad_succes.html",{"table":table})
            else:
                table=NaklTable(Purchase.pur.all())
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
    st=Stock.st.filter(ostat__gt=-0.1)
    table=StockTable(st)
    if request.method=="POST":
        kol=request.POST.get("kol")
        name=request.POST.get("name")
        rec=request.POST.get("receiv")
        print(name)
        stk=Stock.st.filter(name=name)
        st=stk[0]
        if st.kol<kol:
            return render(request,"spis1.html",{"text":"Недостаточно на складе"})
        else:
            st.kol-=kol
            stk.save()
            nakl=Spis(product=name,kol=kol,receiver=rec)
            nakl.save()
            return render(request,"spis1.html",{"text":"Списано"})

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
                prod=Purchase.pur.get(id=n_id)
                prod.purchased_kol=kol
                prod.new_cost=summ
                prod.summ=float(summ)*float(kol)
                prod.save()
                name=prod.name
            if nk_id_zakup.get(request.user.id,0)==0:
                print(111111111111111111111111)
                nak_id=request.POST.get("nak_id")
                print(nak_id)
                nk_id_zakup[request.user.id]=nak_id
            else:
                nak_id=nk_id_zakup[request.user.id]
            print(n_id,nak_id)
            products=Purchase.pur.filter(Q(nak_id=nak_id)&Q(id__gt=n_id)&Q(is_delivered=False))
            table=NaklTable(Purchase.pur.all())
            RequestConfig(request).configure(table)
            if len(products)==0:
                return render(request,"zakup_succes.html",{"table":table})
            else:
                table=NaklTable(Purchase.pur.all())
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