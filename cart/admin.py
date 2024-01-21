from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "created_at")


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "get_variations",
        "user",
        "cart",
        "quantity",
        "created_at",
    )
    list_display_links = (
        "product",
        "user",
    )
    search_fields = ("user__username", "user__email")

    def get_variations(self, obj):
        return ", ".join([str(variation) for variation in obj.variations.all()])

    get_variations.short_description = "Variations"


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
