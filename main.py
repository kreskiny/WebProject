from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/log_in')
def log_in():
    return render_template('log_in.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/product')
def product():
    return render_template('product.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
