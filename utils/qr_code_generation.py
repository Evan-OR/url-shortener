import base64
from io import BytesIO
import qrcode

def generate_encoded_qr(url:str):    
    """
    Generate and encode a QR code image for a given URL.

    Args:
        url (str): The URL for which a QR code should be generated.

    Returns:
        str: The base64-encoded representation of the QR code image in PNG format.

    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2, 
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_buf = BytesIO()
    img = qr.make_image(fill_color="#535353", back_color="white") 
    img.save(img_buf, format="PNG")

    encoded_image = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return encoded_image