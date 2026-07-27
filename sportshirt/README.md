# SportShirt Shop — ระบบสั่งทำเสื้อกีฬาสี (Django + Excel + UiPath)

เว็บแอปสำหรับรับคำสั่งซื้อเสื้อกีฬาสีตามฟอร์มที่ออกแบบไว้ โดย **Django เป็นฐานข้อมูลหลัก (source of truth)**
และทุกครั้งที่มีคำสั่งซื้อใหม่ ระบบจะเขียนข้อมูลลงไฟล์ **Excel (.xlsx)** โดยอัตโนมัติ เพื่อให้
**UiPath Studio** เปิดอ่านและนำไปทำงานอัตโนมัติต่อได้ (เช่น พิมพ์ใบปะหน้า, ส่ง LINE/Email แจ้งฝ่ายผลิต,
อัปเดตสต๊อก ฯลฯ)

## โครงสร้างโปรเจกต์

```
sportshirt/
├── manage.py
├── requirements.txt
├── sportshirt_project/       # ตั้งค่าโปรเจกต์ Django (settings, urls)
├── orders/                   # แอปหลัก
│   ├── models.py             # โมเดล Order (ฐานข้อมูลหลัก)
│   ├── forms.py              # ฟอร์มรับข้อมูล ตรงกับหน้าเว็บ
│   ├── views.py               # หน้าเว็บ + logic บันทึกข้อมูล
│   ├── excel_utils.py         # เขียน/ซิงค์ข้อมูลไปไฟล์ Excel (จุดเชื่อมกับ UiPath)
│   ├── admin.py               # จัดการคำสั่งซื้อผ่าน Django Admin
│   └── management/commands/resync_excel.py   # คำสั่ง sync ข้อมูลทั้งหมดใหม่
├── templates/orders/         # หน้าเว็บ (Tailwind CSS)
└── data/orders.xlsx          # ไฟล์ Excel ที่ UiPath จะอ่าน (ถูกสร้างอัตโนมัติ)
```

## วิธีติดตั้งและรันบนเครื่อง

ต้องมี Python 3.10+ ติดตั้งไว้ก่อน

```bash
cd sportshirt
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # (ไม่บังคับ) สร้างบัญชีแอดมินไว้ดูออเดอร์ผ่าน /admin/

python manage.py runserver
```

จากนั้นเปิดเบราว์เซอร์ไปที่ **http://127.0.0.1:8000/** จะเจอฟอร์มสั่งทำเสื้อกีฬาสี
และ **http://127.0.0.1:8000/admin/** สำหรับดู/จัดการคำสั่งซื้อทั้งหมด

## การทำงานร่วมกับ Excel

- ทุกครั้งที่ลูกค้ากดปุ่ม **"บันทึกข้อมูลการสั่งทำ"** สำเร็จ ระบบจะ:
  1. บันทึกข้อมูลลง Django database (SQLite ตั้งต้น — เปลี่ยนเป็น PostgreSQL/MySQL ได้ใน `settings.py`)
  2. เพิ่มแถวใหม่ 1 แถวลงไฟล์ **`data/orders.xlsx`** โดยอัตโนมัติ (ฟังก์ชัน `append_order_to_excel`
     ใน `orders/excel_utils.py`)
- คอลัมน์ในไฟล์ Excel:

  | คอลัมน์ | คำอธิบาย |
  |---|---|
  | ชื่อ-นามสกุล | ชื่อผู้ลงทะเบียน |
  | อีเมล | อีเมลติดต่อ |
  | ไซส์เสื้อ | ไซส์เสื้อที่ระลึก (SS/S/M/L/XL/XXL) |
  | เบอร์โทรศัพท์ | เบอร์ติดต่อ 10 หลัก |
  | จำนวนรวม (ตัว) | จำนวนชุดที่ระลึก (1 คน = 1 ตัว รวมอยู่ในค่าลงทะเบียนแล้ว) |
  | ราคารวม (บาท) | ค่าลงทะเบียน 690 บาท |
  | วันที่ต้องการรับสินค้า | วันที่ผู้ลงทะเบียนระบุ |
  | วันที่สั่งซื้อ | วันเวลาที่บันทึกการลงทะเบียน |
  | ที่อยู่จัดส่ง | ที่อยู่แบบเต็ม รวมทุกช่อง |
  | Order ID | เลขอ้างอิงการลงทะเบียนใน Django (ใช้ join กลับมาที่ระบบได้) |

- ดาวน์โหลดไฟล์ Excel ปัจจุบันได้ที่ `http://127.0.0.1:8000/export/excel/`
- หากไฟล์ Excel หายหรือเสีย สามารถสร้างใหม่จากข้อมูลใน Django ทั้งหมดได้ด้วยคำสั่ง:
  ```bash
  python manage.py resync_excel
  ```
  หรือเลือกออเดอร์ใน Django Admin แล้วใช้ action **"ซิงค์ข้อมูลทั้งหมดไปยังไฟล์ Excel ใหม่"**

## การเชื่อมกับ UiPath Studio

**สำคัญ: ไม่ต้องเปิด Chrome ไปที่หน้า Django Admin แล้วดึงข้อมูลจากตาราง (Extract Table Data) เลย!**
วิธีนั้นเสี่ยงพังง่าย (หน้าเว็บเปลี่ยน/โหลดช้า/ต้อง login ทุกครั้ง) และช้ากว่าที่ควรจะเป็นมาก
เพราะจริง ๆ แล้ว **Django เขียนไฟล์ Excel ให้อัตโนมัติอยู่แล้วทุกครั้งที่มีคนลงทะเบียนสำเร็จ**
(ไฟล์ `data/orders.xlsx` ที่มีอยู่แล้วในโปรเจกต์) UiPath แค่เปิดไฟล์นี้ตรง ๆ ก็พอ ไม่ต้องผ่านเบราว์เซอร์เลย

ขั้นตอนที่แนะนำใน UiPath Studio (ตัดขั้นตอน Chrome/Extract Table Data ออกจาก workflow เดิมของคุณได้เลย):

1. **ตั้งค่า path ให้ตรงกัน** — เปิด `sportshirt_project/settings.py` ดูค่า `ORDERS_EXCEL_PATH`
   (ค่าเริ่มต้นคือ `data/orders.xlsx` ในโฟลเดอร์โปรเจกต์ Django) แล้วใช้ path เดียวกันนี้ใน UiPath
   - ถ้า UiPath กับ Django รันอยู่เครื่องเดียวกัน ก็ใช้ path เต็ม เช่น
     `C:\Users\...\sportshirt\data\orders.xlsx`
   - ถ้ารันคนละเครื่อง ให้เปลี่ยน `ORDERS_EXCEL_PATH` เป็น shared folder ที่ทั้งสองฝั่งเข้าถึงได้
2. **อ่านไฟล์** — ใช้กิจกรรม **"Excel Application Scope"** หรือ **"Use Excel File"** ชี้ไปที่ path ด้านบน
   ตามด้วย **"Read Range"** (sheet ชื่อ **"ข้อมูล"**) จะได้ DataTable ของรายชื่อผู้ลงทะเบียนทั้งหมดทันที
   — ไม่ต้องมี Chrome, ไม่ต้อง login, ไม่ต้อง Extract Table Data
3. **ประมวลผลทีละแถว** — ใช้ **"For Each Row in Data Table"** วนอ่านแต่ละคนที่ลงทะเบียน
4. **ส่งอีเมลแจ้งเตือน** (ถ้าต้องการ เหมือนในสกรีนช็อตที่คุณทำไว้) — ใช้ **"Send Outlook Mail Message"**
   หรือถ้าจะใช้ Gmail ให้ใช้กิจกรรม **"Send Email"** ของ UiPath.Mail.Activities พร้อมผูก Gmail account
   แนบไฟล์ `orders.xlsx` เป็น attachment ได้เลย (ตามที่เห็นในสกรีนช็อตของคุณ ส่วนนี้ทำถูกแล้ว)
5. **แจ้งเตือนจบงาน** — ใช้ **"Message Box"** แสดงข้อความเมื่อทำงานเสร็จ (เหมือนที่คุณทำไว้อยู่แล้ว)
6. **ตั้งให้รันอัตโนมัติเป็นระยะ** — แทนที่จะกดรันเองทุกครั้ง แนะนำตั้ง **Time Trigger** ใน UiPath Assistant
   หรือ Windows Task Scheduler ให้รัน workflow นี้ทุก ๆ กี่นาที/ชั่วโมงตามที่ต้องการ
7. **กันประมวลผลซ้ำ (ถ้าต้องการ)** — คอลัมน์ **Order ID** ในไฟล์ Excel มีไว้ให้ UiPath จำได้ว่าเคยส่งอีเมล/
   ประมวลผลแถวไหนไปแล้ว เช่น เก็บเลข Order ID ล่าสุดที่ประมวลผลแล้วไว้ในไฟล์ config เล็ก ๆ
   แล้ว filter DataTable เอาเฉพาะแถวที่ Order ID มากกว่าเลขนั้น

สรุปคือ workflow ของคุณจากสกรีนช็อตทำถูกทิศทางแล้วเกือบทั้งหมด (Write Range / Send Email / Message Box)
แค่ตัดส่วน "Chrome Select" + "Extract Table Data" ออก แล้วเริ่มจาก **"Read Range" อ่านไฟล์ `orders.xlsx`
โดยตรง** แทนก็จะเสถียรและเร็วขึ้นมาก

ตัวอย่างไฟล์ Excel ที่มีข้อมูลตัวอย่าง (หน้าตาแบบเดียวกับที่ Django จะสร้างให้จริง พร้อมหัวตารางพื้นเหลือง)
แนบมาให้แล้วในชื่อ `ตัวอย่างไฟล์_orders.xlsx`

## หมายเหตุด้านความปลอดภัย/การใช้งานจริง (Production)

- `DEBUG = True` และ `SECRET_KEY` ในไฟล์นี้เหมาะกับการพัฒนา/ทดสอบเท่านั้น
- สำหรับใช้งานจริง ควร:
  - ตั้ง `DEBUG = False` และเก็บ `SECRET_KEY` ไว้ใน environment variable
  - กำหนด `ALLOWED_HOSTS` ให้ตรงกับโดเมนจริง
  - เปลี่ยนฐานข้อมูลจาก SQLite เป็น PostgreSQL/MySQL หากมีผู้ใช้งานพร้อมกันจำนวนมาก
  - พิจารณาใช้ shared network drive หรือ cloud storage (เช่น OneDrive/SharePoint ที่ UiPath เข้าถึงได้)
    แทนไฟล์ในเครื่องเดียว หากรัน Django และ UiPath Robot คนละเครื่องกัน
