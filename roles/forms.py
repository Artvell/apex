from django import forms
from .models import *

class NaklForm(forms.Form):
    #nak_id=forms.CharField(label="Введите ID накладной")
    nak=Purchase.pur.filter(is_accepted=0)
    ch=[n.nak_id for n in nak]
    ch=set(ch)
    ch=list(ch)
    nak_id = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class GetForm(forms.Form):
    kol=forms.IntegerField(label="Количество")
    shtrih=forms.IntegerField(label="Штрих код")
    srok=forms.DateField(label="Срок годности")

class Zakup(forms.Form):
    nak=Purchase.pur.filter(is_accepted=0)
    ch=[n.nak_id for n in nak]
    ch=set(ch)
    ch=list(ch)
    nak_id = forms.ChoiceField(choices=[(n,n) for n in ch],label="Номер накладной")

class ZakupForm(forms.Form):
        kol=forms.IntegerField(label="Количество")
        cost=forms.IntegerField(label="Цена")

class SpisForm(forms.Form):
    st=Stock.st.filter(ostat__gt=-0.1)
    s=[n.name for n in st]
    rec=Receivers.objects.all()
    receiver=[r.name for r in rec]
    name=forms.ChoiceField(choices=[(k,k) for k in s],label="Товар")
    receiv=forms.ChoiceField(choices=[(r,r) for r in receiver])
    kol=forms.IntegerField(label="Количество")