from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import os
import base64
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_img = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)

            # Encode the image for display
            qr_code_img = base64.b64encode(buffer.getvalue()).decode()
            # Save image temporarily for download
            buffer.seek(0)
            with open("qrcode.png", "wb") as f:
                f.write(buffer.getvalue())
    return render_template('index.html', qr_code=qr_code_img)


@app.route('/download')
def download():
    # Serve the QR Code file for download
    return send_file(
        'qrcode.png',
        mimetype='image/png',
        as_attachment=True,
        download_name='qrcode.png'
    )


if __name__ == '__main__':
    # Ensure old QR codes are deleted on restart
    if os.path.exists("qrcode.png"):
        os.remove("qrcode.png")
    app.run(debug=True)
