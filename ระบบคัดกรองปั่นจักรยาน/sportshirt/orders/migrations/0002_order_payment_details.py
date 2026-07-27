from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_amount",
            field=models.PositiveIntegerField(default=690, verbose_name="จำนวนเงินที่ชำระ"),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[("bank_transfer", "โอนผ่านบัญชีธนาคาร"), ("qr_promptpay", "QR PromptPay")],
                default="bank_transfer",
                max_length=30,
                verbose_name="ช่องทางชำระเงิน",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[("pending", "รอการตรวจสอบ"), ("verified", "ยืนยันแล้ว"), ("rejected", "ปฏิเสธ")],
                default="pending",
                max_length=20,
                verbose_name="สถานะชำระเงิน",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="slip_image",
            field=models.ImageField(blank=True, null=True, upload_to="slips/", verbose_name="สลิปการชำระเงิน"),
        ),
    ]
