from django.contrib import admin
from .models import Order, OrderedItem, Payment
from django.utils.html import format_html


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_id", "amount", "status")
    search_fields = ("transaction_id",)


class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    extra = 0
    readonly_fields = (
        "payment",
        "user",
        "product",
        "total_amount",
        "price",
        "quantity",
        "variation",
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "full_name",
        "phone_number",
        "email",
        "city",
        "grand_total",
        "created_at",
        "is_ordered",
    )
    search_fields = (
        "order_number",
        "phone_number",
        "email",
    )
    list_per_page = 20
    inlines = [OrderedItemInline]
    readonly_fields = ()


class OrderedItemAdmin(admin.ModelAdmin):
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
        "get_variations",
        "quantity",
        "order",
        "user",
        "payment",
        "total_amount",
    )
    list_display_links = (
        "thumbnail",
        "product",
    )
    search_fields = (
        "order__order_number",
        "user__email",
        "user__username",
        "payment__transaction_id",
    )

    def get_variations(self, obj):
        return ", ".join([str(variation) for variation in obj.variation.all()])


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem, OrderedItemAdmin)
