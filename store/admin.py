from django.contrib import admin
from .models import Product, Variation, ProductReview, FeaturedProduct, WebsiteDetails
from solo.admin import SingletonModelAdmin
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.product_image_1:
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    object.product_image_1.url
                )
            )
        else:
            default_image_path = "/static/images/image-placeholder.png"
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    default_image_path
                )
            )

    thumbnail.short_description = "Photo"
    list_display = (
        "thumbnail",
        "product_name",
        "price",
        "discount_price",
        "stock",
        "category",
        "updated_at",
        "is_available",
        "best_seller",
    )
    list_display_links = (
        "thumbnail",
        "product_name",
    )
    prepopulated_fields = {"slug": ("product_name",)}
    search_fields = (
        "product_name",
        "category__category_name",
    )
    list_editable = ("is_available", "best_seller")
    list_filter = ("category", "best_seller", "is_available")


class VariationAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.product.product_image_1:
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    object.product.product_image_1.url
                )
            )
        else:
            default_image_path = "/static/images/image-placeholder.png"
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    default_image_path
                )
            )

    thumbnail.short_description = "Photo"

    list_display = (
        "thumbnail",
        "product",
        "variation_category",
        "variation_value",
        "created_at",
    )
    list_display_links = ("thumbnail", "product")
    list_filter = ("product", "variation_category")


class ProductReviewAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.product.product_image_1:
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    object.product.product_image_1.url
                )
            )
        else:
            default_image_path = "/static/images/image-placeholder.png"
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    default_image_path
                )
            )

    thumbnail.short_description = "Photo"

    list_display = (
        "thumbnail",
        "product",
        "user",
        "rating",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_display_links = (
        "thumbnail",
        "product",
    )
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = (
        "product__product_name",
        "user__email",
        "user__username",
    )


class FeaturedProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    object.image.url
                )
            )
        else:
            default_image_path = "/static/images/image-placeholder.png"
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    default_image_path
                )
            )

    thumbnail.short_description = "Photo"

    list_display = ("thumbnail", "title", "product", "created_at", "updated_at")
    list_display_links = (
        "thumbnail",
        "title",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(FeaturedProduct, FeaturedProductAdmin)
admin.site.register(WebsiteDetails, SingletonModelAdmin)
