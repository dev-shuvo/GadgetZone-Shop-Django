from django.shortcuts import render
from store.models import Product, FeaturedProduct
from categories.models import Category


def index(request):
    products = Product.objects.all().filter(is_available=True)
    featured_products = FeaturedProduct.objects.all()
    popular_categories = Category.objects.all().filter(popular_category=True)
    new_launches = products[:8]

    data = {
        "products": products,
        "featured_products": featured_products,
        "popular_categories": popular_categories,
        "new_launches": new_launches,
    }
    return render(request, "index.html", data)
