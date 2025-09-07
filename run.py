#run.py
import os
from flask import render_template

from backend import create_app   # <- use backend instead of app

app = create_app()  # Flask app instance

@app.route("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

# @app.route("/")
# def home():
#     return render_template("index.html")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000)), 
        debug=True
    )
