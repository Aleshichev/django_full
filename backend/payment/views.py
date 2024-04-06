from django.contrib.auth.decorators import login_required
import weasyprint
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress
from django.template.loader import render_to_string
from django.templatetags.static import static

from cart.cart import Cart
from .tasks import send_order_confirmation


@login_required(login_url="account:login")
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None
    form = ShippingAddressForm(instance=shipping_address)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect("account:dashboard")

    context = {"form": form}
    return render(request, "payment/shipping.html", context)


def checkout(request):
    if request.user.is_authenticated:
        # shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        # if shipping_address:
        #     return render(
        #         request, "payment/checkout.html", {"shipping_address": shipping_address}
        #     )
        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user)
        return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, "payment/checkout.html")


def complete_order(request):
    if request.POST.get("action") == "payment":
        name = request.POST.get("name")
        email = request.POST.get("email")
        street_address = request.POST.get("street_address")
        apartment_address = request.POST.get("apartment_address")
        contry = request.POST.get("contry")
        zipcode = request.POST.get("zipcode")

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": name,
                "email": email,
                "street_address": street_address,
                "apartment_address": apartment_address,
                "country": contry,
                "zip": zipcode,
            },
        )

    if request.user.is_authenticated:
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            amount=total_price,
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["qty"],
                user=request.user,
            )
    else:
        order = Order.objects.create(
            shipping_address=shipping_address,
            amount=total_price,
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["qty"],
            )

    return JsonResponse({"success": True, "order_id": order.id})


def payment_success(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.paid = True
    order.save() 
    # celery task
    send_order_confirmation.delay(order_id)
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "payment/payment-success.html")


def payment_fail(request):
    return render(request, "payment/payment-fail.html")

@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404('Заказ не найден')
    html = render_to_string('payment/order/pdf/pdf_invoice.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    css_path = static('payment/css/pdf.css').lstrip('/')
    # css_path = 'static/payment/css/pdf.css'
    stylesheets = [weasyprint.CSS(css_path)]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response