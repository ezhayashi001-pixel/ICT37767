from django.contrib import admin
from django.contrib import messages
from .models import Order
from .excel_utils import resync_all_orders


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "email", "phone", "shirt_size", "quantity", "total_price",
        "payment_method", "payment_status", "province", "expected_delivery_date", "order_date", "synced_to_excel",
    )
    list_filter = ("province", "shirt_size", "payment_method", "payment_status", "synced_to_excel", "order_date")
    search_fields = ("full_name", "phone", "email", "postal_code")
    readonly_fields = ("order_date",)
    actions = ["resync_selected_to_excel"]

    def resync_selected_to_excel(self, request, queryset):
        resync_all_orders()
        self.message_user(
            request,
            "ซิงค์ข้อมูลคำสั่งซื้อทั้งหมดไปยังไฟล์ Excel เรียบร้อยแล้ว",
            level=messages.SUCCESS,
        )
    resync_selected_to_excel.short_description = "ซิงค์ข้อมูลทั้งหมดไปยังไฟล์ Excel ใหม่"
