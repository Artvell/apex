from django import forms
from .models import *
from django.db.models import Q

class NaklForm(forms.Form):
    def __init__(self,nak, *args, **kwargs):
        super(NaklForm, self).__init__(*args, **kwargs)
        ch=[int(n.nak_id) for n in nak]
        ch=set(ch)
        ch=sorted(list(ch))
        self.fields['nak_id'] = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class NaklForm2(forms.Form):
    def __init__(self,nak, *args, **kwargs):
        super(NaklForm2, self).__init__(*args, **kwargs)
        ch=[int(n.nak_id) for n in nak]
        ch=set(ch)
        ch=sorted(ch)[::-1]
        self.fields['nak_id'] = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class Zagot(forms.Form):
    def __init__(self,nak, *args, **kwargs):
        super(Zagot, self).__init__(*args, **kwargs)
        print(nak)
        ch=[int(n.nak_id) for n in nak]
        ch=[max(ch)]
        self.fields["nak_id"] = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class GetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GetForm, self).__init__(*args, **kwargs)
        self.fields['kol']=forms.FloatField(label="Количество")
        #shtrih=forms.IntegerField(label="Штрих код")
        #self.fields['srok']=forms.DateField(label="Срок годности")
        self.fields['shtr_kol']=forms.IntegerField(label="Количество штрих-кодов")

class GetForm2(forms.Form):
    kol=forms.FloatField(label="Количество")

class BarcodeForm(forms.Form):
    name=forms.CharField(label="Штрих-код")

class Zakup(forms.Form):
    def __init__(self,nak, *args, **kwargs):
        super(Zakup, self).__init__(*args, **kwargs)
        #kol=forms.IntegerField()
        ch=[n.nak_id for n in nak]
        cd=[int(d) for d in ch]
        ch=[max(cd)]
        print("ch=",ch)
        date=nak[len(nak)-1].date
        print(date)
        self.fields['nak_id'] = forms.ChoiceField(choices=[(n,"№ "+str(n)+"  "+str(date)) for n in ch],label="Номер накладной")

class ZakupForm(forms.Form):
    def __init__(self,salers_list,*args,**kwargs):
        if "s" in kwargs:
            sal=kwargs.pop("s")
        else:
            sal=0
        super(ZakupForm,self).__init__(*args, **kwargs)
        salers=list(set([s.saler for s in salers_list]))
        self.fields["srok"]=forms.DateField(label="Срок годности",required=False)
        self.fields["kol"]=forms.FloatField(label="Количество",required=False)
        self.fields["cost"]=forms.FloatField(label="Общая цена",required=False)
        #print("##",salers[0])
        self.fields["saler"]=forms.ChoiceField(choices=[(s,s) for s in salers],label="Продавец")
        if int(sal)!=0:
            self.fields["saler"].initial=[(1,1)]

class Add_Product_for_saler(forms.Form):
    def __init__(self,salers,*args,**kwargs):
        super(Add_Product_for_saler,self).__init__(*args, **kwargs)
        sallers=[s.name for s in salers]
        s_id=[s.id for s in salers]
        #sallers=list(set(sallers))
        for i in range(len(sallers)):
            self.fields[f"saler_{s_id[i]}"]=forms.FloatField(label=f"Продавец: {sallers[i]}\n Цена:",required=False)


class Add_Saler(forms.Form):
    name=forms.CharField(label="Имя")
    firm_name=forms.CharField(label="Название фирмы")
    phone=forms.CharField(label="Телефон")
    place=forms.CharField(label="Расположение")
    cost=forms.FloatField(label="Цена")


class SpisForm(forms.Form):
    def __init__(self,rec, *args, **kwargs):
        if "n" in kwargs:
            name=kwargs.pop("n")
            f=True
        else:
            f=False
        super(SpisForm, self).__init__(*args, **kwargs)
        if f:
            receiver=[r.receiver for r in rec if r.receiver==name]
        else:
            receiver=[r.receiver for r in rec]
        self.fields['receiv']=forms.ChoiceField(choices=[(r,r) for r in receiver],label="Объект списания")

class ZagotForm(forms.Form):
    def __init__(self,ingr, *args, **kwargs):
        super(ZagotForm, self).__init__(*args, **kwargs)
        self.fields[f"product"] = forms.FloatField(label="Заготовлено")
        spis_ingr=[prod.ingr.name for prod in ingr]
        print(spis_ingr)
        for j in range(len(spis_ingr)):
            self.fields[spis_ingr[j]]=forms.FloatField()
        self.fields['shtr_kol']=forms.IntegerField(label="Количество штрих-кодов")

class KassirForm(forms.Form):
    def __init__(self,money_receivers,types,*args,**kwargs):
        super(KassirForm,self).__init__(*args,**kwargs)
        #n1ames=list(set(m.username for m in money_receivers))
        self.fields["name"]=forms.ChoiceField(choices=[(m,m.username) for m in money_receivers],label="Кому")
        self.fields["type"]=forms.ChoiceField(choices=[(t.types.types,t.types.types+" ("+str(t.kolvo)+")") for t in types],label="Тип денег")
        self.fields["money"]=forms.FloatField(label="Сколько")

class KassirForm2(forms.Form):
    def __init__(self,types,*args,**kwargs):
        super(KassirForm2,self).__init__(*args,**kwargs)
        self.fields["name"]=forms.CharField(label="Кому")
        self.fields["for_why"]=forms.CharField(widget=forms.Textarea,label="Зачем")
        self.fields["type"]=forms.ChoiceField(choices=[(t.types.types,t.types.types+" ("+str(t.kolvo)+")") for t in types],label="Тип денег")
        self.fields["money"]=forms.FloatField(label="Сколько")

class KassirAcceptNaklad(forms.Form):
    def __init__(self,products,*args,**kwargs):
        super(KassirAcceptNaklad,self).__init__(*args,**kwargs)
        for product in products:
            self.fields[f"product_{product.id}"]=forms.BooleanField(label=product.name.name,required=False)

class KassirTakeMoney(forms.Form):
    def __init__(self,types,*args,**kwargs):
        super(KassirTakeMoney,self).__init__(*args,**kwargs)
        self.fields["type"]=forms.ChoiceField(choices=[(t,t.types) for t in types],label="Тип денег")
        self.fields["kolvo"]=forms.FloatField(label="Кол-во")

class AdminForm(forms.Form):
    def __init__(self,k,product,ingreds,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #edizm=product.edizm.edizm
        self.fields["product"]= forms.ChoiceField(choices=[(n.name,n.name+" (1"+n.edizm.edizm+")") for n in product],label=f"Продукт (1 единица)")
        self.fields["srok"]=forms.FloatField(label="Срок годности (в часах)")
        self.fields["procent"]=forms.FloatField(label="Погрешность (%)")
        for i in range(1,int(k)+1):
            print(k)
            self.fields[f"ingr_{i}"]=forms.ChoiceField(choices=[(n.name,n.name) for n in ingreds],label="Ингридиент")
            self.fields[f"ingr_kol_{i}"]=forms.FloatField(label="Нужно")

class AdminForm3(forms.Form):
    def __init__(self,k,*args,**kwargs):
        super().__init__(*args,**kwargs)
        salers=Postavsh.objects.all()
        products=Products.objects.filter(prigot=False)
        self.fields["saler"]= forms.ChoiceField(choices=[(saler,saler.name) for saler in salers],label="Продавец")
        for i in range(1,int(k)+1):
            print(k)
            self.fields[f"prod_{i}"]=forms.ChoiceField(choices=[(prod,prod.name) for prod in products],label="Товар")
            self.fields[f"prod_cost_{i}"]=forms.FloatField(label="Последняя цена")