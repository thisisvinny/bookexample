from flask import Flask
from bookapp import app
import os

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=int(os.environ.get("PORT", 5000)))