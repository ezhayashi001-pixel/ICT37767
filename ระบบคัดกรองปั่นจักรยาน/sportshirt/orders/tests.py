from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from orders.forms import OrderForm
from orders.models import Order


class OrderPaymentFlowTests(TestCase):
    def test_payment_fields_are_available_in_form(self):
        form = OrderForm()

        self.assertIn("payment_method", form.fields)
        self.assertIn("payment_amount", form.fields)
        self.assertIn("slip_image", form.fields)

    def test_order_can_store_uploaded_slip(self):
        payload = {
            "full_name": "สมชาย ใจดี",
            "phone": "0891234567",
            "email": "somchai@example.com",
            "shirt_size": "M",
            "house_no": "123/45",
            "village_building": "หมู่บ้านแสนสุข",
            "moo": "2",
            "soi": "4",
            "road": "ถนนมิตรภาพ",
            "province": "กรุงเทพมหานคร",
            "district": "เขตพระนคร",
            "subdistrict": "พระบรมมหาราชวัง",
            "postal_code": "10100",
            "expected_delivery_date": "2030-01-15",
            "payment_method": "bank_transfer",
            "payment_amount": "690",
        }
        image_buffer = BytesIO()
        image = Image.new("RGB", (1, 1), color="white")
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        file_obj = SimpleUploadedFile(
            "slip.png",
            image_buffer.read(),
            content_type="image/png",
        )

        form = OrderForm(data=payload, files={"slip_image": file_obj})
        self.assertTrue(form.is_valid(), form.errors)

        order = form.save()
        self.assertEqual(order.payment_method, "bank_transfer")
        self.assertEqual(order.payment_amount, 690)
        self.assertTrue(order.slip_image.name.endswith("slip.png"))
