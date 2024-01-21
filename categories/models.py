from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to="images/categories/", blank=True)
    popular_category = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_url(self):
        return reverse("products_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name
