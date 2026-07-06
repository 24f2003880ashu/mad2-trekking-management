from flask import Flask
from config import Config
from models import db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return "Welcome to Trekking Management Application"
with app.app_context():
    db.create_all()
    print("Database Created Successfully")
if __name__ == "__main__":
    app.run(debug=True)