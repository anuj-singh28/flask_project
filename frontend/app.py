from flask import Flask, render_template, request
import requests

BACKEND_URL = 'http://127.0.0.1:9000'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    try:

        form_data = dict(request.form)

        response = requests.post(BACKEND_URL+ '/submit', json=form_data)

        data = response.json()
        if data.get("success"):
            return 'Data submitted successfully!'

        else:
            return render_template("index.html", error=data.get("message"))

    except requests.exceptions.ConnectionError:
        return render_template("index.html", error="Backend server is not reachable")

    except Exception:
        return render_template("index.html", error="Something went wrong")


if __name__ == '__main__':
    app.run( port=8000, debug=True)


