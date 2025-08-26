# backend/wsgi.py
from backend.app import create_app  # <-- import from backend.app

app = create_app()

if __name__ == "__main__":
    app.run()
