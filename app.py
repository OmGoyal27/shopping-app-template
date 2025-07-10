import os
import json
import base64
import binascii
from flask import Flask, render_template, send_from_directory, abort, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management
PRODUCTS_DIR = "Products"

@app.route("/")
def index():
    products = []
    for product_dir in os.listdir(PRODUCTS_DIR):
        product_path = os.path.join(PRODUCTS_DIR, product_dir)
        if os.path.isdir(product_path):         # If the path is a directory
            details_path = os.path.join(product_path, "details.json")   # Get the details.json file
            if os.path.exists(details_path):                            # Only if it exists
                with open(details_path) as f:
                    product_details = json.load(f)
                    product_details["link"] = f"/product/{product_dir}"     # Make the link, the name of the directory
                    products.append(product_details)
    return render_template("index.html", products=products)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/product/<product_name>")
def product(product_name):
    product_path = os.path.join(PRODUCTS_DIR, product_name)
    details_path = os.path.join(product_path, "details.json")
    if os.path.exists(details_path):  # Only if it exists
        with open(details_path) as f:
            product_details = json.load(f)
        # Mark product as unavailable if stock is 0
        product_details["unavailable"] = product_details.get("stock", 0) == 0
        return render_template("product.html", product=product_details)
    else:
        abort(404)

@app.route("/Products/<product_name>/assets/<path:filename>")
def product_assets(product_name, filename):
    product_assets_path = os.path.join(PRODUCTS_DIR, product_name, "assets")
    return send_from_directory(product_assets_path, filename)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()       # Get the search query
    matched_products = []

    for product_folder in os.listdir(PRODUCTS_DIR):
        product_path = os.path.join(PRODUCTS_DIR, product_folder, "details.json")
        if os.path.exists(product_path):
            with open(product_path, "r") as file:
                product_details = json.load(file)
                if query in product_details["name"].lower() or query in product_details["description"].lower():
                    matched_products.append(product_details)

    return render_template("index.html", query=query, products=matched_products, search=True)

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    detailed_cart = {}

    for product_name, quantity in cart.items():
        product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")
        if os.path.exists(product_path):
            with open(product_path, "r") as file:
                product_details = json.load(file)
                detailed_cart[product_name] = {
                    "quantity": quantity,
                    "stock": product_details.get("stock", 0),
                    "images": product_details.get("images", []),
                    "description": product_details.get("description", ""),
                }

    return render_template("cart.html", cart=detailed_cart)

@app.route("/add_to_cart/<product_name>", methods=["POST"])
def add_to_cart(product_name):
    cart = session.get("cart", {})
    quantity = int(request.form.get("quantity", 1))
    product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")

    if os.path.exists(product_path):
        with open(product_path, "r") as file:
            product_details = json.load(file)
        available_stock = product_details.get("stock", 0)

        # Prevent adding more items than available in stock
        if product_name in cart:
            new_quantity = cart[product_name] + quantity
        else:
            new_quantity = quantity

        if new_quantity > available_stock:
            return redirect(url_for("product", product_name=product_name))

        cart[product_name] = new_quantity
        session["cart"] = cart

    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<product_name>", methods=["POST"])
def remove_from_cart(product_name):
    cart = session.get("cart", {})
    if product_name in cart:
        del cart[product_name]
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/update_cart/<product_name>", methods=["POST"])
def update_cart(product_name):
    cart = session.get("cart", {})
    quantity = int(request.form.get("quantity", 1))
    if quantity > 0:
        cart[product_name] = quantity  # Update the quantity directly
    else:
        cart.pop(product_name, None)  # Remove the product if quantity is 0
    session["cart"] = cart
    return redirect(url_for("cart"))

def get_detailed_cart(product_name: str, quantity: int, detailed_cart: list = None):
    if not detailed_cart:
        detailed_cart = []

    product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")
    if os.path.exists(product_path):
        with open(product_path, "r") as file:
            product_details = json.load(file)
            detailed_cart.append({
                "name": product_name,
                "quantity": quantity,
                "price": product_details.get("price", 0),
                "total_cost": quantity * product_details.get("price", 0)
            })

    return detailed_cart

@app.route("/buy", methods=["POST", "GET"])
def buy():
    if request.method == "GET":
        return redirect(url_for("cart"))

    cart = session.get("cart", {})
    detailed_cart = []

    for product_name, quantity in cart.items():
        detailed_cart = get_detailed_cart(product_name, quantity, detailed_cart)

    # Encode cart data as base64 to avoid HTML escaping issues
    cart_json = json.dumps(detailed_cart)
    cart_b64 = base64.b64encode(cart_json.encode('utf-8')).decode('utf-8')
    return render_template("checkout.html", cart=detailed_cart, cart_data=cart_b64)

@app.route("/buy_now", methods=["GET", "POST"])
def buy_now():
    if request.method == "GET":
        return redirect(url_for("cart"))
    
    data = request.form
    product_name = data.get("product_name")
    quantity = int(data.get("quantity", 1))

    detailed_cart = get_detailed_cart(product_name, quantity)

    # Encode cart data as base64 to avoid HTML escaping issues
    cart_json = json.dumps(detailed_cart)
    cart_b64 = base64.b64encode(cart_json.encode('utf-8')).decode('utf-8')
    return render_template("checkout.html", cart=detailed_cart, cart_data=cart_b64)


@app.route("/checkout")
def checkout():
    # Redirect to cart if accessed directly
    return redirect(url_for("cart"))

@app.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():
    # Add your purchase confirmation logic here
    # This place is where you would handle the purchase confirmation
    # If payment is successful, update stock and clear cart
    # If payment fails, you might want to redirect back to the cart or show an error message
    cart_data = request.form.get("cart")
    print(f"Raw cart data received: {repr(cart_data)}")  # Use repr to see exact string
    
    if cart_data:
        # This is from checkout page (buy_now or buy), cart is base64 encoded
        try:
            # Decode from base64 first
            cart_json = base64.b64decode(cart_data).decode('utf-8')
            print(f"Decoded JSON: {cart_json}")
            cart_list = json.loads(cart_json)
            print(f"Successfully parsed cart: {cart_list}")
            # Process cart from checkout (list format)
            for item in cart_list:
                product_name = item.get("name")
                quantity = item.get("quantity", 0)
                
                if product_name and quantity > 0:
                    product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")
                    if os.path.exists(product_path):
                        try:
                            with open(product_path, "r") as file:
                                product_details = json.load(file)
                            
                            # Check stock availability
                            available_stock = product_details.get("stock", 0)
                            if quantity > available_stock:
                                print(f"Insufficient stock for {product_name}. Requested: {quantity}, Available: {available_stock}")
                                continue
                            
                            # Update stock
                            product_details["stock"] = max(0, available_stock - quantity)
                            with open(product_path, "w") as file:
                                json.dump(product_details, file, indent=4)
                                
                            print(f"Purchased {quantity} of {product_name}. Remaining stock: {product_details['stock']}")
                        except (json.JSONDecodeError, IOError) as e:
                            print(f"Error processing purchase for {product_name}: {e}")
        except (json.JSONDecodeError, binascii.Error) as e:
            print(f"Error parsing cart data: {e}")
            return redirect(url_for("cart"))
    else:
        # This is from regular cart, use session cart
        cart = session.get("cart", {})
        if not cart:
            return redirect(url_for("cart"))
        
        # Process session cart (dictionary format)
        for product_name, quantity in cart.items():
            product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")
            if os.path.exists(product_path):
                try:
                    with open(product_path, "r") as file:
                        product_details = json.load(file)
                    
                    # Check stock availability
                    available_stock = product_details.get("stock", 0)
                    if quantity > available_stock:
                        print(f"Insufficient stock for {product_name}. Requested: {quantity}, Available: {available_stock}")
                        continue
                    
                    # Update stock
                    product_details["stock"] = max(0, available_stock - quantity)
                    with open(product_path, "w") as file:
                        json.dump(product_details, file, indent=4)
                        
                    print(f"Purchased {quantity} of {product_name}. Remaining stock: {product_details['stock']}")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error processing purchase for {product_name}: {e}")
        
        # Clear the session cart after purchase
        session["cart"] = {}
    
    return redirect(url_for("thank_you"))

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    app.run(debug=True)