from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Order, PROVINCE_CHOICES, SIZE_CHOICES, PAYMENT_METHOD_CHOICES, REGISTRATION_FEE

# สไตล์ input สำหรับธีมนีออนพื้นหลังมืด
TEXT_INPUT_CLASS = (
    "w-full rounded-lg bg-slate-900/60 border border-purple-500/40 px-4 py-2.5 text-sm "
    "text-gray-100 placeholder-gray-500 "
    "focus:outline-none focus:ring-2 focus:ring-fuchsia-500 focus:border-fuchsia-400 "
    "focus:shadow-[0_0_12px_2px_rgba(217,70,239,0.55)] transition-shadow"
)


class OrderForm(forms.ModelForm):
    shirt_size = forms.ChoiceField(
        label="ไซส์เสื้อที่ระลึก",
        choices=SIZE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "peer sr-only"}),
        required=True,
    )
    payment_method = forms.ChoiceField(
        label="ช่องทางชำระเงิน",
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "peer sr-only"}),
        required=True,
    )
    payment_amount = forms.IntegerField(
        label="จำนวนเงินที่ชำระ",
        min_value=1,
        initial=REGISTRATION_FEE,
        widget=forms.NumberInput(attrs={"class": TEXT_INPUT_CLASS, "readonly": True}),
    )

    class Meta:
        model = Order
        fields = [
            "full_name", "phone", "email", "shirt_size",
            "house_no", "village_building", "moo", "soi", "road",
            "province", "district", "subdistrict", "postal_code",
            "expected_delivery_date",
            "payment_method", "payment_amount", "slip_image",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น สมชาย ใจดี"
            }),
            "phone": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น 0891234567",
                "maxlength": "10", "inputmode": "numeric"
            }),
            "email": forms.EmailInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น example@email.com"
            }),
            "house_no": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น 123/45"
            }),
            "village_building": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น หมู่บ้านแสนสุข เฟส 2"
            }),
            "moo": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น หมู่บ้านแสนสุข เฟส 2"
            }),
            "soi": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น ซอยมิตรภาพ 4"
            }),
            "road": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น ถนนมิตรภาพ"
            }),
            "province": forms.Select(attrs={"class": TEXT_INPUT_CLASS}),
            "district": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น เมืองนนทบุรี"
            }),
            "subdistrict": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น ท่าทราย"
            }),
            "postal_code": forms.TextInput(attrs={
                "class": TEXT_INPUT_CLASS, "placeholder": "เช่น 11000",
                "maxlength": "5", "inputmode": "numeric"
            }),
            "expected_delivery_date": forms.DateInput(attrs={
                "class": TEXT_INPUT_CLASS, "type": "date",
                "min": date.today().isoformat(),
            }),
            "slip_image": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-purple-100 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-fuchsia-600 file:text-white file:font-medium hover:file:bg-fuchsia-500",
                "accept": "image/*",
            }),
        }
        labels = {
            "full_name": "ชื่อ - นามสกุล",
            "phone": "เบอร์โทรศัพท์ (ตัวเลข 10 หลัก)",
            "email": "อีเมล",
            "house_no": "บ้านเลขที่",
            "village_building": "หมู่บ้าน / อาคาร / คอนโด (ถ้ามี)",
            "moo": "หมู่ (ถ้ามี)",
            "soi": "ซอย (ถ้ามี)",
            "road": "ถนน (ถ้ามี)",
            "province": "จังหวัด",
            "district": "อำเภอ / เขต",
            "subdistrict": "ตำบล / แขวง",
            "postal_code": "รหัสไปรษณีย์",
            "expected_delivery_date": "ประมาณวันที่ต้องการรับสินค้า",
            "payment_method": "ช่องทางชำระเงิน",
            "payment_amount": "จำนวนเงินที่ชำระ",
            "slip_image": "สลิปการชำระเงิน",
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("กรุณากรอกเบอร์โทรศัพท์เป็นตัวเลข 10 หลัก")
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data["postal_code"].strip()
        if not postal_code.isdigit() or len(postal_code) != 5:
            raise ValidationError("กรุณากรอกรหัสไปรษณีย์เป็นตัวเลข 5 หลัก")
        return postal_code

    def clean_expected_delivery_date(self):
        d = self.cleaned_data["expected_delivery_date"]
        if d < date.today():
            raise ValidationError("ไม่สามารถเลือกวันที่ผ่านมาแล้วได้ กรุณาเลือกวันที่ปัจจุบันหรืออนาคต")
        return d

    def clean_payment_amount(self):
        amount = self.cleaned_data["payment_amount"]
        if amount != REGISTRATION_FEE:
            raise ValidationError("จำนวนเงินต้องเป็น 690 บาท")
        return amount

    def clean_slip_image(self):
        slip = self.cleaned_data.get("slip_image")
        payment_method = self.cleaned_data.get("payment_method")
        # For bank transfers, slip is required. For QR PromptPay, it can be uploaded later.
        if payment_method == "bank_transfer" and not slip:
            raise ValidationError("กรุณาอัปโหลดสลิปการชำระเงิน")
        return slip


class SlipUploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["slip_image"]
        widgets = {
            "slip_image": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-purple-100 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-fuchsia-600 file:text-white file:font-medium hover:file:bg-fuchsia-500",
                "accept": "image/*",
            }),
        }
        labels = {
            "slip_image": "สลิปการชำระเงิน",
        }

    def clean_slip_image(self):
        slip = self.cleaned_data.get("slip_image")
        if not slip:
            raise ValidationError("กรุณาอัปโหลดสลิปการชำระเงิน")
        return slip
