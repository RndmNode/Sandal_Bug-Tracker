from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Flask & Docker! welcome to Sandal, the bug tracker</h1>"

def run():
    app.run(debug=True)

if __name__ == "__main__":
    run()