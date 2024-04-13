from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/log_in')
def log_in():
    return render_template('log_in.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('online_store.db')
        cursor = conn.cursor()

        # Вставляем данные пользователя в таблицу
        cursor.execute('INSERT INTO users (username, password, cart) VALUES (?, ?, ?)', (username, password, ''))

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
        return 'Пользователь успешно зарегистрирован!'
    else:
        return 'Метод не поддерживается!'


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/product1')
def product1():
    return render_template('product1.html')


@app.route('/product2')
def product2():
    return render_template('product2.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
