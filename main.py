import os
from flask import Flask, render_template, jsonify, redirect, request
from utils.DatabaseController import DatabaseController
from utils.qr_code_generation import generate_encoded_qr
from utils.utils import get_base_url

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
    except Exception as e:
        return  render_template('404.html'), 404

@app.route("/create-link", methods=['POST'])
def create_link():  
    try:
        data = request.get_json()
        url = data.get('url')
        res = dc.shorten_url(url)
        
        # Get root URL
        server_url = get_base_url(request)
        res["shortened"] = f"{server_url}display/{res.get('shortened')}"
        return jsonify(res), 200
    
    except ValueError as e:
        return jsonify({"message": "Invalid URL", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message": "error creating link", "error": str(e)}), 500
    
@app.route("/display/<code>")
def display_link(code):
    try:
        res = dc.get_original_from_shortened(code)

        original_url = res.get('original_url')
        shortened_url = res.get('shortened_url')

        full_shortened_url = get_base_url(request) + shortened_url

        encoded_image = generate_encoded_qr(original_url)

        return render_template('display_link.html', original_url=original_url, shortened_url=full_shortened_url, encoded_image=encoded_image), 200
 
    except Exception as e:
        return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    env_type = os.getenv('ENV_TYPE', os.environ.get('ENV_TYPE'))

    if env_type == "DEBUG":
        app.run(debug=True)    
    else:
        app.run(debug=False)
