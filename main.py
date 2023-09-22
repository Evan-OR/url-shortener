from flask import Flask, render_template, jsonify, request
from database_connection import create_db_connection, shorten_url, get_original_from_shortened

app = Flask(__name__)

# DataBase Connection
connection = create_db_connection()


@app.route("/")
def hello_world():
    return  render_template('home.html')

@app.route("/<link>")
def display_link(link):
    res = get_original_from_shortened(connection, link)

    return  render_template('url.html', original_url=res)

@app.route("/create-link", methods=['POST'])
def create_link():  

    data = request.get_json()
    url = data.get('url')

    try:
        res = shorten_url(connection, url)
        return jsonify(res), 200
    
    except ValueError as e:
        return jsonify({"message": "Invalid URL", "error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"message": "error creating link", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)