from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_create_view, name="create"),
    path("qr-promptpay/<int:pk>/", views.qr_promptpay_view, name="qr_promptpay"),
    path("receipt-invalid/<int:pk>/", views.receipt_invalid_view, name="receipt_invalid"),
    path("success/<int:pk>/", views.order_success_view, name="success"),
    path("export/excel/", views.download_excel_view, name="export_excel"),
]
