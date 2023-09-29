from io import BytesIO, StringIO
from flask import Flask, render_template, jsonify, send_file, request
from utils.DatabaseController import DatabaseController
from utils.qr_code_generation import generate_qr_code
from time import time

# Flask Init
app = Flask(__name__)
# DataBase Controller
dc = DatabaseController()

@app.route("/")
def hello_world():
    return  render_template('home.html')

@app.route("/<link>")
def redirect(link):
    try:
        res = dc.get_original_from_shortened(link)
        return  render_template('url.html', original_url=res.get('original_url'))
    except:
        return  render_template('404.html'), 404

@app.route("/create-link", methods=['POST'])
def create_link():  
    try:
        data = request.get_json()
        url = data.get('url')
        res = dc.shorten_url(url)
        
        # Get root URL
        server_url = request.url_root
        res["shortened"] = f"{server_url}/display/{res['shortened']}"

        return jsonify(res), 200
    
    except ValueError as e:
        return jsonify({"message": "Invalid URL", "error": str(e)}), 400
    
    except Exception as e:
        print(e)
        return jsonify({"message": "error creating link", "error": str(e)}), 500
    
@app.route("/display/<code>")
def display_link(code):
    # Check if link is in database
    try:
        res = dc.get_original_from_shortened(code)
        print(res)

        original_url = res.get('original_url')
        shortened_url = res.get('shortened_url')

        full_shortened_url = request.url_root + shortened_url
        print(full_shortened_url)
        image_data = generate_qr_code(full_shortened_url)

        return render_template('display_link.html', original_url=original_url, shortened_url=full_shortened_url, image_data=image_data), 200
 
    except Exception as e:
        print(e)
        return render_template('404.html'), 404
    
@app.route('/get_qrimg')
def get_qrimg():
    img_buf = BytesIO()
    start = time()
    img = generate_qr_code(url='www.python.org')
    end = time()
    print(f"{(end - start) * 1000}ms")
    img.save(img_buf)
    img_buf.seek(0)
    return send_file(img_buf, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)