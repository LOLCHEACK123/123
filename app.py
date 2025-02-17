from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'Sungat123'

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

products = {
    "Телефоны": [
        {"name": "iPhone 15 Pro", "price": 999, "image": "iphone15pro.jpg"},
        {"name": "Samsung Galaxy S23", "price": 899, "image": "samsung-galaxy-s23.jpg"},
        {"name": "Google Pixel 7", "price": 799, "image": "google-pixel-7.jpg"}
    ],
    "Ноутбуки": [
        {"name": "MacBook Air M2", "price": 1199, "image": "macbook-air-m2.jpg"},
        {"name": "Asus ROG Zephyrus", "price": 1499, "image": "asus-rog-zephyrus.jpg"},
        {"name": "Dell XPS 15", "price": 1299, "image": "dell-xps-15.jpg"}
    ],
    "Телевизоры": [
        {"name": "LG OLED C2", "price": 1299, "image": "lg-oled-c2.jpg"},
        {"name": "Samsung QLED Q80", "price": 1099, "image": "samsung-qled-q80.jpg"},
        {"name": "Sony Bravia XR", "price": 1399, "image": "sony-bravia-xr.jpg"}
    ],
    "PlayStation": [
        {"name": "PlayStation 5", "price": 499, "image": "playstation-5.jpg"},
        {"name": "PlayStation 4 Pro", "price": 399, "image": "playstation-4-pro.jpg"},
        {"name": "PlayStation VR2", "price": 549, "image": "playstation-vr2.jpg"}
    ]
}

# Хранилище пользователей (в реальном проекте – база данных)
users = {}


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Ошибка входа. Проверьте логин и пароль!"
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Пользователь уже существует!"
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = []

    if request.method == 'POST':
        item = request.form.get('item')
        session['cart'].append(item)

    return render_template('cart.html', cart=session['cart'])


@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))

    cart_items = session.get('cart', [])
    if not cart_items:
        return "Ваша корзина пуста!"

    total_price = sum(
        [next((p['price'] for category in products.values() for p in category if p['name'] == item), 0) for item in
         cart_items])

    message = f"Пользователь {session['username']} оформил заказ:\n" + "\n".join(
        cart_items) + f"\nОбщая сумма: ${total_price}"
    send_telegram_message(message)

    session['cart'] = []
    return render_template('checkout.html')


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)


if __name__ == '__main__':
    app.run(debug=True)
