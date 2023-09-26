import qrcode

def generate_qr_code(url):
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create a PIL image from the QR code data
    img = qr.make_image(fill_color="black", back_color="white")

    return img