import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'shop.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------------------
# Modeles
# ---------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    stock = db.Column(db.Integer, default=10)


# ---------------------------
# Donnees de demonstration
# ---------------------------
def seed_data():
    if Product.query.count() == 0:
        demo_products = [
            Product(name="Casque Audio Sans Fil", description="Confort et son immersif pour toute la journee.",
                     price=59.99, image="headphones.jpg", stock=15),
            Product(name="Montre Connectee", description="Suivi d'activite, notifications et autonomie longue duree.",
                     price=89.90, image="watch.jpg", stock=8),
            Product(name="Sac a Dos Urbain", description="Compartiment laptop, resistant a l'eau, design minimaliste.",
                     price=39.50, image="backpack.jpg", stock=20),
            Product(name="Clavier Mecanique", description="Switches tactiles, retroeclairage RGB, pour gamers et devs.",
                     price=74.00, image="keyboard.jpg", stock=12),
            Product(name="Enceinte Bluetooth", description="Son puissant, portable, resistante aux projections.",
                     price=45.00, image="speaker.jpg", stock=18),
            Product(name="Lampe de Bureau LED", description="Luminosite reglable, port USB integre, design epure.",
                     price=25.99, image="lamp.jpg", stock=25),
        ]
        db.session.add_all(demo_products)
        db.session.commit()


# ---------------------------
# Aides pour le panier (en session)
# ---------------------------
def get_cart():
    return session.setdefault('cart', {})  # {product_id_str: quantity}


# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session.modified = True
    flash(f"« {product.name} » a ete ajoute au panier.", "success")
    return redirect(request.referrer or url_for('index'))


@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    cart = get_cart()
    items = []
    total = 0.0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)


@app.route('/checkout', methods=['POST'])
def checkout():
    session['cart'] = {}
    flash("Merci pour votre commande ! (demo - aucun paiement reel)", "success")
    return redirect(url_for('index'))


@app.route('/healthz')
def healthz():
    """Endpoint de health check, utile pour Kubernetes (liveness/readiness)."""
    return {"status": "ok"}, 200


with app.app_context():
    db.create_all()
    seed_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
