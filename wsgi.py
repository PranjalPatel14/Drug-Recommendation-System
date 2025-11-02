"""
WSGI entry point for production deployment
Use this file to run the app with Gunicorn or other WSGI servers
"""
from app import app

if __name__ == "__main__":
    app.run()

