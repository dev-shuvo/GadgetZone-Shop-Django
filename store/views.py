from django.shortcuts import redirect, render, get_object_or_404
from cart.models import CartItem
from cart.views import _cart_id
from categories.models import Category
from orders.models import OrderedItem
from store.forms import ReviewForm
from store.models import Product, ProductReview
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def store(request, category_slug=None):
    categories = Category.objects.all()
    warranty = Product.objects.values("warranty").distinct()
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True
        ).order_by("-id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("-id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        products_count = products.count()

    data = {
        "products": paged_products,
        "products_count": products_count,
        "warranty": warranty,
    }
    return render(request, "store/store.html", data)


def product_details(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(
                product=product, user=request.user
            ).exists()
        else:
            in_cart = CartItem.objects.filter(
                cart__cart_id=_cart_id(request), product=product
            ).exists()

    except Exception as e:
        raise e

    reviews = ProductReview.objects.filter(product_id=product.id, is_active=True)
    reviews_count = reviews.count()

    if request.user.is_authenticated:
        try:
            is_ordered = OrderedItem.objects.filter(
                user=request.user, product_id=product.id
            ).exists()
        except OrderedItem.DoesNotExist:
            is_ordered = None
    else:
        is_ordered = None

    data = {
        "product": product,
        "in_cart": in_cart,
        "reviews": reviews,
        "reviews_count": reviews_count,
        "is_ordered": is_ordered,
    }
    return render(request, "store/product_details.html", data)


def search(request):
    categories = Category.objects.all()
    warranty = Product.objects.values("warranty").distinct()
    products = Product.objects.all()
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )

    if "order_by" in request.GET:
        keyword = request.GET["order_by"]
        if keyword == "best_sellers":
            products = products.filter(best_seller=True)
        elif keyword == "low_to_high":
            products = products.order_by("discount_price")
        elif keyword == "high_to_low":
            products = products.order_by("-discount_price")

    if "category" in request.GET:
        keyword = request.GET["category"]
        if keyword:
            products = products.filter(category=keyword)

    if "warranty" in request.GET:
        keyword = request.GET["warranty"]
        if keyword:
            products = products.filter(warranty=keyword)

    else:
        products = products

    data = {
        "products": products,
        "products_count": products.count(),
        "categories": categories,
        "warranty": warranty,
    }
    return render(request, "store/store.html", data)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            review = ProductReview.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except ProductReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ProductReview()
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
