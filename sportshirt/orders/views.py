from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
import os

from .forms import OrderForm, SlipUploadForm
from .models import Order
from .excel_utils import append_order_to_excel
from .receipt_utils import is_receipt_image


def order_create_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            # If user chose QR PromptPay, redirect to QR confirmation page
            if order.payment_method == "qr_promptpay":
                append_order_to_excel(order)
                return redirect(reverse("orders:qr_promptpay", args=[order.pk]))

            # For bank transfer, we check the slip immediately
            if order.payment_method == "bank_transfer":
                if order.slip_image and is_receipt_image(order.slip_image.path):
                    order.payment_status = "verified"
                    order.save()
                    append_order_to_excel(order)
                    return redirect(reverse("orders:success", args=[order.pk]))
                else:
                    order.payment_status = "rejected"
                    order.save()
                    return redirect(reverse("orders:receipt_invalid", args=[order.pk]))
    else:
        form = OrderForm()

    return render(request, "orders/order_form.html", {"form": form})


def order_success_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_success.html", {"order": order})


def qr_promptpay_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.payment_method != "qr_promptpay":
        return redirect(reverse("orders:success", args=[order.pk]))

    if request.method == "POST":
        form = SlipUploadForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            if order.slip_image and is_receipt_image(order.slip_image.path):
                order.payment_status = "verified"
                order.save()
                return redirect(reverse("orders:success", args=[order.pk]))
            else:
                order.payment_status = "rejected"
                order.save()
                return redirect(reverse("orders:receipt_invalid", args=[order.pk]))
    else:
        form = SlipUploadForm(instance=order)

    return render(request, "orders/qr_promptpay.html", {"order": order, "form": form})


def receipt_invalid_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/receipt_invalid.html", {"order": order})


def download_excel_view(request):
    """ดาวน์โหลดไฟล์ Excel ปัจจุบัน (ไฟล์เดียวกับที่ UiPath ใช้อ่าน)"""
    path = settings.ORDERS_EXCEL_PATH
    if not os.path.exists(path):
        raise Http404("ยังไม่มีไฟล์ Excel ถูกสร้างขึ้น")
    return FileResponse(
        open(path, "rb"),
        as_attachment=True,
        filename="orders.xlsx",
    )
