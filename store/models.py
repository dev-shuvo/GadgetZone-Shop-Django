from django.db import models
from django.urls import reverse
from accounts.models import User
from categories.models import Category
from django.db.models import Avg
from ckeditor.fields import RichTextField
from solo.models import SingletonModel


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = RichTextField(max_length=500)
    product_feature_1 = models.CharField(max_length=50)
    product_feature_2 = models.CharField(max_length=50)
    warranty = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    discount_price = models.IntegerField()
    product_image_1 = models.ImageField(upload_to="images/products/")
    product_image_2 = models.ImageField(upload_to="images/products/", blank=True)
    product_image_3 = models.ImageField(upload_to="images/products/", blank=True)
    product_image_4 = models.ImageField(upload_to="images/products/", blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    best_seller = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_details", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def average_review(self):
        reviews = ProductReview.objects.filter(product=self, is_active=True).aggregate(
            average=Avg("rating")
        )
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        else:
            avg = float(0.0)

        return avg


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(
            variation_category="color", is_active=True
        )


class Variation(models.Model):
    variation_category_choice = (("color", "color"),)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review


class FeaturedProduct(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="images/featured_products/",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WebsiteDetails(SingletonModel):
    logo = models.ImageField(upload_to="images/website/", blank=True)
    favicon = models.ImageField(upload_to="images/website/", blank=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    short_description = RichTextField(max_length=200)
    facebook = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    google_maps_embed = models.URLField(blank=True)

    model_name = "Website Details"

    def __str__(self):
        return self.model_name
