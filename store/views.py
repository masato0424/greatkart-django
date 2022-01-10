from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category ,is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()

    context = {
        'products' : products,
        'products_count' : products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product' : product,
    }

    return render(request, 'store/product_detail.html', context)
    
