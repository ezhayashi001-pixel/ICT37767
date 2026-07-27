from django.core.management.base import BaseCommand
from orders.excel_utils import resync_all_orders


class Command(BaseCommand):
    help = "สร้างไฟล์ Excel ใหม่ทั้งหมดจากข้อมูลคำสั่งซื้อใน Django database (ใช้เวลาไฟล์ Excel หาย/เสีย)"

    def handle(self, *args, **options):
        path = resync_all_orders()
        self.stdout.write(self.style.SUCCESS(f"ซิงค์ข้อมูลสำเร็จ -> {path}"))
