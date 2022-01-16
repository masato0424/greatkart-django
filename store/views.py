from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def _paginator(request, products):
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return paged_products

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category ,is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        products_count = products.count()
    paged_products = _paginator(request, products)

    context = {
        'products' : paged_products,
        'products_count' : products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    context = {
        'product' : product,
        'in_cart' : in_cart,
    }

    return render(request, 'store/product_detail.html', context)
    
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
                ).order_by('-created_date')
        else:
            products = Product.objects.all()
        products_count = products.count()

    context = {
        'products' : products,
        'products_count' : products_count,
    }
    return render(request, "store/store.html", context)
