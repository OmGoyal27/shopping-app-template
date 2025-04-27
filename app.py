import os
import json
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
    return send_from_directory("static", filename)      # Just get some basic files, like the favicon

@app.route("/product/<product_name>")
def product(product_name):
    product_path = os.path.join(PRODUCTS_DIR, product_name)
    details_path = os.path.join(product_path, "details.json")  # Get the details of the product
    if os.path.exists(details_path):  # Only if it exists
        with open(details_path) as f:
            product_details = json.load(f)
        # Mark product as unavailable if stock is 0
        product_details["unavailable"] = product_details.get("stock", 0) == 0
        return render_template("product.html", product=product_details)  # Serve it.
    else:
        abort(404)

@app.route("/Products/<product_name>/assets/<path:filename>")
def product_assets(product_name, filename):
    product_assets_path = os.path.join(PRODUCTS_DIR, product_name, "assets")
    return send_from_directory(product_assets_path, filename)                   # Gets the photos and other assets.

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()       # Get the search query
    matched_products = []

    for product_folder in os.listdir(PRODUCTS_DIR):
        product_path = os.path.join(PRODUCTS_DIR, product_folder, "details.json")
        if os.path.exists(product_path):
            with open(product_path, "r") as file:
                product_details = json.load(file)
                if query in product_details["name"].lower() or query in product_details["description"].lower():         # If the searched query is either in the product name itself, or the description
                    matched_products.append(product_details)

    # Render the index.html template with search results
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
            return redirect(url_for("product", product_name=product_name))  # Redirect back to product page

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

@app.route("/buy", methods=["POST", "GET"])
def buy():
    if request.method == "GET":
        return redirect(url_for("cart"))

    cart = session.get("cart", {})
    detailed_cart = []

    for product_name, quantity in cart.items():
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

    # Pass the detailed cart as a query parameter to the checkout page
    return render_template("checkout.html", cart=detailed_cart)

@app.route("/checkout")
def checkout():
    # Only render the checkout page if cart data is passed
    cart = request.args.get("cart", None)
    if not cart:
        return redirect(url_for("index"))
    return render_template("checkout.html", cart=json.loads(cart))

@app.route("/confirm_purchase", methods=["POST"])
def confirm_purchase():
    cart = session.get("cart", {})
    for product_name, quantity in cart.items():
        product_path = os.path.join(PRODUCTS_DIR, product_name, "details.json")
        if os.path.exists(product_path):
            with open(product_path, "r") as file:
                product_details = json.load(file)
            # Update stock
            product_details["stock"] = max(0, product_details.get("stock", 0) - quantity)
            with open(product_path, "w") as file:
                json.dump(product_details, file, indent=4)
    # Clear the cart after purchase
    session["cart"] = {}
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)