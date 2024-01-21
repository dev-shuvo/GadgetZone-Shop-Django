import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from cart.models import Cart, CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderedItem, Payment
import stripe
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY
BACKEND_DOMAIN = settings.BACKEND_DOMAIN


@login_required(login_url="login")
def place_order(request, subtotal=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect("store")

    grand_total = 0
    tax = 0

    for item in cart_items:
        subtotal += item.product.discount_price * item.quantity
        quantity += item.quantity

    tax = (2 * subtotal) / 100
    delivery_fee = 2 * quantity
    grand_total = subtotal + tax + delivery_fee
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order_form = Order()
            order_form.first_name = form.cleaned_data["first_name"]
            order_form.last_name = form.cleaned_data["last_name"]
            order_form.phone_number = form.cleaned_data["phone_number"]
            order_form.email = form.cleaned_data["email"]
            order_form.address_line_1 = form.cleaned_data["address_line_1"]
            order_form.address_line_2 = form.cleaned_data["address_line_2"]
            order_form.city = form.cleaned_data["city"]
            order_form.pin_code = form.cleaned_data["pin_code"]
            order_form.state = form.cleaned_data["state"]
            order_form.country = form.cleaned_data["country"]
            order_form.order_note = form.cleaned_data["order_note"]
            order_form.grand_total = grand_total
            order_form.tax = tax
            order_form.delivery_fee = delivery_fee
            order_form.ip = request.META.get("REMOTE_ADDR")
            order_form.user = current_user
            order_form.save()

            year = int(datetime.date.today().strftime("%Y"))
            date = int(datetime.date.today().strftime("%d"))
            month = int(datetime.date.today().strftime("%m"))
            d = datetime.date(year, month, date)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(order_form.id)

            order_form.order_number = order_number
            order_form.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number
            )
            data = {
                "order": order,
                "cart_items": cart_items,
                "subtotal": subtotal,
                "tax": tax,
                "delivery_fee": delivery_fee,
                "grand_total": grand_total,
            }
            return render(request, "orders/place_order.html", data)
    else:
        return redirect("checkout")


@login_required(login_url="login")
def payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    quantity = 0

    for item in cart_items:
        subtotal += item.product.discount_price * item.quantity
        quantity += item.quantity

    tax = (2 * subtotal) / 100
    delivery_fee = 2 * quantity
    order_number = request.GET.get("order_number", None)

    items = []
    for item in cart_items:
        items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.product.product_name},
                    "unit_amount": int(item.product.discount_price * 100),
                },
                "quantity": item.quantity,
            }
        )

    tax_amount_cents = int(tax * 100)

    items.append(
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Tax",
                },
                "unit_amount": tax_amount_cents,
            },
            "quantity": 1,
        }
    )

    delivery_fee_cents = int(delivery_fee * 100)

    items.append(
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Delivery Fee",
                },
                "unit_amount": delivery_fee_cents,
            },
            "quantity": 1,
        }
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url=BACKEND_DOMAIN
        + f"/order/payment/success?session_id={{CHECKOUT_SESSION_ID}}&order_number={order_number}",
        cancel_url=BACKEND_DOMAIN
        + f"/order/payment/cancel?session_id={{CHECKOUT_SESSION_ID}}&order_number={order_number}",
    )

    return redirect(session.url)


@login_required(login_url="login")
def payment_success(request):
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    transaction_id = session.payment_intent
    order_number = request.GET.get("order_number", None)

    payment = Payment.objects.create(
        user=request.user,
        transaction_id=transaction_id,
        amount=session.amount_total / 100,
        status="Paid",
    )

    order = get_object_or_404(Order, user=request.user, order_number=order_number)
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user).order_by("created_at")
    for item in cart_items:
        ordered_item = OrderedItem()
        ordered_item.order = order
        ordered_item.payment = payment
        ordered_item.user = request.user
        ordered_item.product = item.product
        ordered_item.quantity = item.quantity
        ordered_item.price = item.product.discount_price
        ordered_item.total_amount = item.product.discount_price * item.quantity
        ordered_item.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variations = cart_item.variations.all()

        ordered_item = OrderedItem.objects.get(id=ordered_item.id)
        ordered_item.variation.set(product_variations)
        ordered_item.save()

        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject = "Thank you for your order."
    message = render_to_string(
        "orders/emails/order_received_email.html",
        {
            "user": request.user,
            "order": order,
        },
    )
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    return redirect(
        "order_complete",
        order_number=order_number,
        transaction_id=transaction_id,
    )


@login_required(login_url="login")
def payment_cancel(request):
    return render(request, "orders/order_cancelled.html")


@login_required(login_url="login")
def order_complete(request, order_number, transaction_id):
    order = Order.objects.get(
        order_number=order_number,
        payment__transaction_id=transaction_id,
        is_ordered=True,
    )
    ordered_items = OrderedItem.objects.filter(order=order)

    subtotal = 0
    for item in ordered_items:
        subtotal += item.price * item.quantity
    data = {
        "order": order,
        "ordered_items": ordered_items,
        "transaction_id": transaction_id,
        "subtotal": subtotal,
    }
    return render(request, "orders/order_complete.html", data)
