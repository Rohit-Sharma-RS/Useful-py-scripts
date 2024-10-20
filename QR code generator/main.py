import qrcode
from PIL import Image

qrcode_error_correction = input("What error correction level you want to use\n1. Low\n2. Medium\n3. Quartile\n4. High\ndefault = 2 or Medium\n")
qrcode_border = input("Enter the border size of QR code\ndefault = 6\n")
qrcode_version = input("Enter the version of QR code\n(1 to 40 higher version->larger qr)\ndefault = 2\n")

if qrcode_error_correction == '1':
    qrcode_error_correction = qrcode.constants.ERROR_CORRECT_L
elif qrcode_error_correction == '3':
    qrcode_error_correction = qrcode.constants.ERROR_CORRECT_Q
elif qrcode_error_correction == '4':
    qrcode_error_correction = qrcode.constants.ERROR_CORRECT_H
else:
    qrcode_error_correction = qrcode.constants.ERROR_CORRECT_M

if qrcode_version == '' or int(qrcode_version) < 1 or int(qrcode_version) > 40:
    qrcode_version = 2

if qrcode_border == '' or int(qrcode_border) < 0:
    qrcode_border = 6

qr = qrcode.QRCode(
    version=int(qrcode_version),
    error_correction=qrcode_error_correction,
    box_size=10,
    border=int(qrcode_border),
)

choice = input("Enter the data you want to store in QR code\nYour choices are \n1. Text or URL\n2. vCard info\n3. info with logo\n4. WiFi network info\n5. UPI id\n6. UPI id with amount\n")
if choice == '1':
    data = input("Enter the text or URL you want to store in QR code: ")
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QRcode.png")
    print("QR code generated successfully")
    
elif choice == '2':
    name = input("Enter the name: ")
    phone = input("Enter the phone number: ")
    email = input("Enter the email: ")
    qr.add_data(f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QRcode.png")
    print("QR code generated successfully")

elif choice == '3':
    data = input("Enter the text or URL you want to store in QR code: ")
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    logo = Image.open("logo.png")
    img.paste(logo, (50, 50))
    img.save("QRcode.png")
    print("QR code generated successfully")

elif choice == '4':
    ssid = input("Enter the SSID: ")
    password = input("Enter the password: ")
    qr.add_data(f"WIFI:S:{ssid};T:WPA;P:{password};;")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QRcode.png")
    print("QR code generated successfully")