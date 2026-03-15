from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return {"status": "Puente Cosmico 2027-2079 Activo", "security": "B6-Verified"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
