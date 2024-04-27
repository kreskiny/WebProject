import sqlite3

from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/online_store.db")
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('log_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('log_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.context_processor
def inject_user():
    return dict(current_user=current_user)


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        return render_template('cart.html')
    else:
        return render_template('cart_false.html')


@app.route('/product1')
def product1():
    return render_template('product1.html')


@app.route('/product2')
def product2():
    return render_template('product2.html')

@app.route('/product3')
def product3():
    return render_template('product3.html')

@app.route('/product4')
def product4():
    return render_template('product4.html')

@app.route('/product5')
def product5():
    return render_template('product5.html')

@app.route('/product6')
def product6():
    return render_template('product6.html')

@app.route('/product7')
def product7():
    return render_template('product7.html')

@app.route('/product8')
def product8():
    return render_template('product8.html')


@app.route('/personal')
def personal():
    if current_user.is_authenticated:
        return render_template('personal.html')
    else:
        return render_template('personal_false.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit_data():
    return render_template('edit_data.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    name = request.form["name_ed"]
    surname = request.form["surname_ed"]
    dob = request.form["dob_ed"]
    phone = request.form["phone_ed"]
    adress = request.form["adress_ed"]
    email = current_user.email
    if not (name and surname and dob and phone and adress):
        return 'Пожалуйста заполните все поля.'


    try:
        sqlite_connection = sqlite3.connect('db/online_store.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """UPDATE users SET name = ?, surname = ?, date_of_birth = ?, phone_number = ?, adress = ? WHERE email = ?"""
        data = (name, surname, dob, phone, adress, email)
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()

        print(name, surname, email, dob, phone, adress)
        return 'Данные успешно сохранены'
    except Exception as e:
        return 'Ошибка в сохранении данных: ' + str(e)


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    if request.method == 'GET':
        return render_template('pay.html')
    elif request.method == 'POST':
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['address'])
        print(request.form['phone'])
        print(request.form['quantity'])
        return "Заявка оформлена, скоро с вами свяжется оператор"



if __name__ == '__main__':
    main()
