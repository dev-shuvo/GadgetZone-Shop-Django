from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserForm, UserProfileForm
from accounts.models import UserProfile
from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value=value,
                )
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)

        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, cart=cart, user=request.user
            )
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    return redirect("cart")


def minus_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def delete_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id
        )
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect("cart")


def cart(request, subtotal=0, delivery_fee=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(
                user=request.user, is_active=True
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            subtotal += item.product.discount_price * item.quantity
            quantity += item.quantity

        tax = (2 * subtotal) / 100
        delivery_fee = 2 * quantity
        grand_total = subtotal + tax + delivery_fee
    except ObjectDoesNotExist:
        pass

    data = {
        "subtotal": subtotal,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
    }

    return render(request, "store/cart.html", data)


@login_required(login_url="login")
def checkout(request, subtotal=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(
                user=request.user, is_active=True
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            subtotal += item.product.discount_price * item.quantity
            quantity += item.quantity

        tax = (2 * subtotal) / 100
        delivery_fee = 2 * quantity
        grand_total = subtotal + tax + delivery_fee
    except ObjectDoesNotExist:
        pass

    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    data = {
        "subtotal": subtotal,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "store/checkout.html", data)
