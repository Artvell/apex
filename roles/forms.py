from django import forms
from .models import *
from django.db.models import Q

class NaklForm(forms.Form):
    nak=Purchase.objects.filter(is_accepted=0)
    ch=[n.nak_id for n in nak]
    ch=set(ch)
    ch=list(ch)
    nak_id = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class GetForm(forms.Form):
    kol=forms.IntegerField(label="Количество")
    #shtrih=forms.IntegerField(label="Штрих код")
    srok=forms.DateField(label="Срок годности")

class Zakup(forms.Form):
    kol=forms.IntegerField()
    nak=Purchase.objects.filter(is_accepted=0)
    ch=[n.nak_id for n in nak]
    ch=set(ch)
    ch=list(ch)
    nak_id = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class ZakupForm(forms.Form):
        kol=forms.IntegerField(label="Количество")
        cost=forms.IntegerField(label="Цена")
        srok=forms.DateField(label="Срок годности")

class SpisForm(forms.Form):
    st=Codes.objects.filter(kolvo__gt=-0.1)
    s=[n.name.name+" | "+n.shtrih for n in st]
    print(s)
    rec=Receivers.objects.all()
    receiver=[r.receiver for r in rec]
    name=forms.ChoiceField(choices=[(k,k) for k in s],label="Товар")
    receiv=forms.ChoiceField(choices=[(r,r) for r in receiver],label="Объект списания")
    kol=forms.FloatField(label="Количество")

class ZagotForm(forms.Form):
    def __init__(self,i,product, *args, **kwargs):
        super(ZagotForm, self).__init__(*args, **kwargs)
        self.fields[f"product_{i}"] = forms.IntegerField(label="Заготовлено")
        ingr=Ingredients.objects.filter(Q(product__name=product))
        spis_ingr=[prod.ingr.name for prod in ingr]
        print(spis_ingr)
        for j in range(len(spis_ingr)):
            self.fields[spis_ingr[j]]=forms.IntegerField()