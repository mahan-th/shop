from django.shortcuts import render ,redirect
from .models import *
# Create your views here.
from django.http import HttpResponse
from django.db.models import Q ,Min,Max
from django.core.paginator import Paginator



def products(request):

    products = Product.objects.all()


    search = request.GET.get('q')
    if search:
        products = products.filter(title__icontains =request.GET.get('q')) 
        
    # min_max =products.aggregate(min=Min('final_price'),max=Max('final_price'))
    # print(min_max)

    start_range = request.GET.get('start_range')
    end_range = request.GET.get('end_range')
    
    

    if start_range and end_range:
        products = products.filter(
            Q(price__gte=int(start_range)) & Q(price__lte=int(end_range))
        )

    sort = request.GET.get('sorte')
    if sort == "1":
        products = products.order_by("price")
    elif sort == "2":
        products = products.order_by("-price")
    else:
        products = products.order_by("-id")

    paginator = Paginator(products,1)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    query_parmas = request.GET.copy()
    if 'page' in query_parmas:
        del query_parmas['page']
    query_str = query_parmas.urlencode()

    
    context ={
        'product':products,
        'base_url':f"?{query_str}&" if query_str else "?",
    }

    return render(request,'product.html',context)


def porduct_detale(request,**kwargs):

    try:
        product = Product.objects.get(id=kwargs['pk'])

    except:
        return render(request,"404.html")
    attribut = AttrbiuteProduct.objects.filter(product=product)
    image = ProductImage.objects.filter(product=product)
    coller = ProdctColler.objects.filter(product=product)

    context = {
        'product': product,
        'attribute':attribut,
        'image' : image,
        'coller': coller

    }
    return render(request,'product_datale.html',context)

