            form_qict=request.POST.dict()
            for key, value in form_qict.items():
                print(value)
                if value=="Выбрать":
                    f=1
                    print(f)
                    break
                elif value=="Отправить":
                    f=0
                    print(f)
                    prod_id=key
                    break
            if f==1:
                nak_id=form_qict["nak_id"]
                prod=Purchase.objects.filter(Q(nak_id=nak_id)&Q(purchased_kol=0.0))
                prod=prod.order_by("id")
                if len(prod)==0:
                    return render(request,"buy_products.html",{"indic":0})
                else:
                    products=[pr.name.name for pr in prod]
                    kol=[pr.kolvo for pr in prod]
                    ids=[pr.id for pr in prod]
                    l_cost=[pr.last_cost for pr in prod]
                    dates=[pr.min_srok for pr in prod]
                    forms=[]
                    for product in prod:
                        forms.append(ZakupForm(product))
                    print(range(len(ids)))
                    return render(request,"buy_products.html",{"job":job,"indic":1,"products":products,"kol":kol,"ids":ids,"forms":forms,"dates":dates,"last_cost":l_cost,"range":range(len(ids))})
            elif f==0:
                product=Purchase.objects.get(id=prod_id)
                srok=form_qict[f'{prod_id}_srok']
                sr=datetime.strptime(srok,r"%Y-%m-%d")
                sr=sr.date()
                print(sr,type(sr))
                if sr<product.min_srok:
                    return redirect(".")
                else:
                    kol=form_qict[f"{prod_id}_kol"]
                    cost=form_qict[f"{prod_id}_cost"]
                    product.srok=srok
                    product.purchased_kol=kol
                    product.new_cost=cost
                    product.summ=round(float(kol)*float(cost),3)
                    product.save()
                    try:
                        last_cost=LastCost.objects.get(product=product.name)
                        last_cost.cost=cost
                        last_cost.save()
                    except ObjectDoesNotExist:
                        LastCost(product=product.name,cost=cost).save()
                prod=Purchase.objects.filter(Q(nak_id=product.nak_id)&Q(purchased_kol=0.0))
                if len(prod)==0:
                    return render(request,"buy_products.html",{"indic":0})
                else:
                    products=[pr.name.name for pr in prod]
                    kol=[pr.kolvo for pr in prod]
                    ids=[pr.id for pr in prod]
                    l_cost=[pr.last_cost for pr in prod]
                    dates=[pr.min_srok for pr in prod]
                    forms=[]
                    for product in prod:
                        forms.append(ZakupForm(product))
                    return render(request,"buy_products.html",{"job":job,"indic":1,"products":products,"kol":kol,"ids":ids,"forms":forms,"dates":dates,"last_cost":l_cost,"range":range(len(ids))})