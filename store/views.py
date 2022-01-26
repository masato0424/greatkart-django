from django.contrib import messages
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, ReviewRating
from orders.models import Order, OrderProduct
from store.forms import ReviewForm
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

    if request.user.is_authenticated:
        try:
            is_order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id)
        except OrderProduct.DoesNotExist:
            is_order_product = None
    else:
        is_order_product = None

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'product' : product,
        'in_cart' : in_cart,
        'is_order_product' : is_order_product,
        'reviews': reviews,
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

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user=request.user, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review_rating = ReviewRating()
                review_rating.subject      = form.cleaned_data['subject']
                review_rating.rating       = form.cleaned_data['rating']
                review_rating.review       = form.cleaned_data['review']
                review_rating.ip           = request.META.get('REMOTE_ADDR')
                review_rating.user         = request.user
                review_rating.product_id = product_id
                review_rating.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)