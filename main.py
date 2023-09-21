from flask import Flask, render_template
import database_connection as db

app = Flask(__name__)

# DataBase Connection
connection = db.create_db_connection()


@app.route("/")
def hello_world():
    return  render_template('home.html')

@app.route("/create-link", methods=['POST'])
def create_link():
    return 'Creating Link :)'

@app.route("/<link>")
def display_link(link):
    res = db.get_original_from_shortened(connection, link)

    return  render_template('url.html', original_url=res, shortened_url=link)


if __name__ == '__main__':
    app.run(debug=True)