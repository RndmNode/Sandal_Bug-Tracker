from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def home():
    return render_template('login.html')

def run():
    app.run(debug=True)

if __name__ == "__main__":
    run()