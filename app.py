from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    return render_template("analyze.html")


@app.route("/create-resume")
def create_resume():
    return render_template("create_resume.html")


if __name__ == "__main__":
    app.run(debug=True)