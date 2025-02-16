from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Remove or comment out the following lines - they are not needed for Netlify deployment
# if __name__ == "__main__":
#     app.run(debug=True)  # Don't run the Flask server directly on Netlify