from django.contrib import admin
from .models import Category
from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.category_image:
            return format_html(
                "<img src={} style='border-radius: 5px; border: 1px solid #cacaca' width='50px'/>".format(
                    object.category_image.url
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

    prepopulated_fields = {"slug": ("category_name",)}
    list_display = (
        "thumbnail",
        "category_name",
        "slug",
        "popular_category",
        "created_at",
    )
    list_display_links = ("thumbnail", "category_name")
    list_editable = ("popular_category",)


admin.site.register(Category, CategoryAdmin)
