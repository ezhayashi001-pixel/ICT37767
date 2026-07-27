from django.db import models

# ค่าลงทะเบียน (บาท) - รวมชุดที่ระลึกแล้ว ไม่มีค่าใช้จ่ายเพิ่มเติม
REGISTRATION_FEE = 690

# ไซส์ชุดที่ระลึก
SIZE_CHOICES = [
    ("SS", "SS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]

PAYMENT_METHOD_CHOICES = [
    ("bank_transfer", "โอนผ่านบัญชีธนาคาร"),
    ("qr_promptpay", "QR PromptPay"),
]

PAYMENT_STATUS_CHOICES = [
    ("pending", "รอการตรวจสอบ"),
    ("verified", "ยืนยันแล้ว"),
    ("rejected", "ปฏิเสธ"),
]

# 77 จังหวัดของประเทศไทย
THAI_PROVINCES = [
    "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น",
    "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย",
    "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม",
    "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน",
    "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี",
    "พระนครศรีอยุธยา", "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก",
    "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร",
    "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี",
    "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา",
    "สตูล", "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร", "สระแก้ว", "สระบุรี",
    "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "หนองคาย",
    "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี",
    "อุบลราชธานี",
]
PROVINCE_CHOICES = [("", "— เลือกจังหวัด —")] + [(p, p) for p in THAI_PROVINCES]


class Order(models.Model):
    # ข้อมูลผู้ลงทะเบียน
    full_name = models.CharField("ชื่อ - นามสกุล", max_length=150)
    phone = models.CharField("เบอร์โทรศัพท์", max_length=10)
    email = models.EmailField("อีเมล")
    shirt_size = models.CharField("ไซส์เสื้อที่ระลึก", max_length=3, choices=SIZE_CHOICES)

    # ที่อยู่จัดส่ง
    house_no = models.CharField("บ้านเลขที่", max_length=50)
    village_building = models.CharField(
        "หมู่บ้าน / อาคาร / คอนโด", max_length=150, blank=True
    )
    moo = models.CharField("หมู่ (ถ้ามี)", max_length=20, blank=True)
    soi = models.CharField("ซอย (ถ้ามี)", max_length=100, blank=True)
    road = models.CharField("ถนน (ถ้ามี)", max_length=100, blank=True)
    province = models.CharField("จังหวัด", max_length=50, choices=PROVINCE_CHOICES)
    district = models.CharField("อำเภอ / เขต", max_length=100)
    subdistrict = models.CharField("ตำบล / แขวง", max_length=100)
    postal_code = models.CharField("รหัสไปรษณีย์", max_length=5)

    # วันที่ต้องการรับสินค้า (ชุดที่ระลึก)
    expected_delivery_date = models.DateField("วันที่ต้องการรับสินค้า")

    # ข้อมูลชำระเงิน
    payment_method = models.CharField(
        "ช่องทางชำระเงิน",
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="bank_transfer",
    )
    payment_amount = models.PositiveIntegerField("จำนวนเงินที่ชำระ", default=REGISTRATION_FEE)
    slip_image = models.ImageField(
        "สลิปการชำระเงิน",
        upload_to="slips/",
        blank=True,
        null=True,
    )
    payment_status = models.CharField(
        "สถานะชำระเงิน",
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )

    # วันที่บันทึกการลงทะเบียน (auto)
    order_date = models.DateTimeField("วันที่ลงทะเบียน", auto_now_add=True)

    # สถานะการซิงค์กับ Excel / UiPath (ช่วยให้ UiPath อ่านเฉพาะแถวที่ยังไม่ประมวลผล)
    synced_to_excel = models.BooleanField(default=False)

    class Meta:
        verbose_name = "การลงทะเบียน"
        verbose_name_plural = "การลงทะเบียน"
        ordering = ["-order_date"]

    def __str__(self):
        return f"{self.full_name} ({self.order_date:%Y-%m-%d})"

    @property
    def quantity(self):
        """จำนวนชุดที่ระลึกที่ได้รับ (รวมอยู่ในค่าลงทะเบียนแล้ว ผู้ลงทะเบียน 1 คน = 1 ตัว)"""
        return 1

    @property
    def total_price(self):
        return REGISTRATION_FEE

    @property
    def full_address(self):
        parts = []
        parts.append(f"{self.house_no}")
        if self.village_building:
            parts.append(self.village_building)
        if self.moo:
            parts.append(f"หมู่ {self.moo}")
        if self.soi:
            parts.append(f"ซอย{self.soi}")
        if self.road:
            parts.append(f"ถนน{self.road}")
        parts.append(f"ตำบล/แขวง{self.subdistrict}")
        parts.append(f"อำเภอ/เขต{self.district}")
        parts.append(f"จังหวัด{self.province}")
        parts.append(self.postal_code)
        return " ".join(parts)
