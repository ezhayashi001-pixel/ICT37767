from pathlib import Path
import re


def is_receipt_image(path: str) -> bool:
    """Check whether an uploaded image likely is a payment receipt.

    Uses pytesseract OCR if available, otherwise falls back to filename/size heuristics.
    """
    p = Path(path)
    if not p.exists():
        return False

    keywords = [
        "สลิป", "ใบเสร็จ", "PromptPay", "Prompt Pay", "ttb", "ธนาคาร", "ยอด",
        "จำนวน", "รายการ", "Receipt", "Slip", "Bank",
    ]

    try:
        import pytesseract
        from PIL import Image

        try:
            text = pytesseract.image_to_string(Image.open(path), lang='tha+eng')
        except Exception:
            text = pytesseract.image_to_string(Image.open(path))

        if not text:
            return False

        text_lower = text.lower()
        for k in keywords:
            if k.lower() in text_lower:
                return True

        if re.search(r"\d{5,}", text):
            return True

        return False
    except Exception:
        name = p.name.lower()
        for k in keywords:
            if k.lower() in name:
                return True
        try:
            if p.stat().st_size < 5_000:
                return False
        except Exception:
            pass
        return True
