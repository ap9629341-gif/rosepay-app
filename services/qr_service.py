"""
QR code service - generate QR codes for payments.
"""
import qrcode
import io
import base64
from typing import Optional


def generate_qr_code(data: str) -> str:
    """
    Generate QR code as base64 string.
    
    WHAT IT DOES:
    1. Creates QR code from data
    2. Converts to base64 image
    3. Returns image string that can be displayed
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def generate_payment_qr(link_id: str, base_url: str = "http://127.0.0.1:8000") -> str:
    """
    Generate QR code for payment link.
    
    The QR code contains the payment link URL.
    """
    payment_url = f"{base_url}/api/v1/payments/link/{link_id}"
    return generate_qr_code(payment_url)


def generate_wallet_qr(wallet_id: int, base_url: str = "http://127.0.0.1:8000") -> str:
    """
    Generate QR code for wallet (for receiving money).
    """
    wallet_url = f"{base_url}/api/v1/wallets/{wallet_id}/receive"
    return generate_qr_code(wallet_url)
