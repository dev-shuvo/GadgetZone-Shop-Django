from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages, auth
from accounts.models import User, UserProfile
from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import Order, OrderedItem
from .forms import SignupForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Please, Activate your account."
            message = render_to_string(
                "accounts/emails/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect("/account/login/?command=verification&email=" + email)
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SignupForm()
    data = {
        "form": form,
    }
    return render(request, "accounts/signup.html", data)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item:
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect("login")
    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations, Your account is now activated.")

        return redirect("login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("signup")


def update_user_profile(request, user_form, profile_form):
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Your profile has been updated.")
        return True
    else:
        for errors in user_form.errors.values():
            for error in errors:
                messages.error(request, error)
        for errors in profile_form.errors.values():
            for error in errors:
                messages.error(request, error)
    return False


def change_password(request):
    current_password = request.POST.get("current_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")
    user = User.objects.get(username__exact=request.user.username)

    if new_password == confirm_password:
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return True
        else:
            messages.error(request, "The password you entered was incorrect!")
            return redirect("change_password")
    else:
        messages.error(request, "Passwords do not match!")
        return redirect("change_password")


@login_required(login_url="login")
def dashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if update_user_profile(request, user_form, profile_form):
            return redirect("dashboard")

        if change_password(request):
            return redirect("login")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    data = {
        "orders": orders,
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
        "total_orders": orders.count(),
    }
    return render(request, "accounts/dashboard.html", data)


@login_required(login_url="login")
def order_details(request, order_number):
    order = Order.objects.get(
        order_number=order_number,
        is_ordered=True,
    )
    ordered_items = OrderedItem.objects.filter(order=order)

    subtotal = 0
    for item in ordered_items:
        subtotal += item.price * item.quantity
    data = {
        "order": order,
        "ordered_items": ordered_items,
        "subtotal": subtotal,
    }
    return render(request, "accounts/order_details.html", data)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset your password."
            message = render_to_string(
                "accounts/emails/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "A password reset link has been sent to your Email Address."
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exist!")
            return redirect("forgot_password")

    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Enter a new password.")
        return redirect("reset_password")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Your password has been changed successfully.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")
    else:
        return render(request, "accounts/reset_password.html")


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    print(orders)
    data = {
        "orders": orders,
    }
    return render(request, "accounts/dashboard.html", data)
