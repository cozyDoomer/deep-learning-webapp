from flask import Flask, render_template
from image_classifier import image_classifier

app = Flask(__name__)

app.register_blueprint(image_classifier)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cv")
def cv():
    return render_template("cv.html")

if __name__ == "__main__":
    app.run(debug=True)