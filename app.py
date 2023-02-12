from flask import Flask,render_template

from getToken2 import startApi
from getToken2 import getValue

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('website.html')

@app.route("/api")
def api():
    return str(getValue(client_config))
    pass
    
if __name__ == "__main__":
    client_config = startApi()
    app.run(debug=True)