import os
import json
from flask import Flask, render_template, send_from_directory, abort, request
from icecream import ic

app = Flask(__name__)
PRODUCTS_DIR = "Products"

@app.route("/")
def index():
    products = []
    for product_dir in os.listdir(PRODUCTS_DIR):
        product_path = os.path.join(PRODUCTS_DIR, product_dir)
        if os.path.isdir(product_path):
            details_path = os.path.join(product_path, "details.json")
            if os.path.exists(details_path):
                with open(details_path) as f:
                    product_details = json.load(f)
                    product_details["link"] = f"/product/{product_dir}"
                    products.append(product_details)
    return render_template("index.html", products=products)

@app.route("/product/<product_name>")
def product(product_name):
    product_path = os.path.join(PRODUCTS_DIR, product_name)
    details_path = os.path.join(product_path, "details.json")
    if os.path.exists(details_path):
        with open(details_path) as f:
            product_details = json.load(f)
        return render_template("product.html", product=product_details)
    else:
        abort(404)

@app.route("/Products/<product_name>/assets/<path:filename>")
def product_assets(product_name, filename):
    product_assets_path = os.path.join(PRODUCTS_DIR, product_name, "assets")
    return send_from_directory(product_assets_path, filename)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    matched_products = []

    for product_folder in os.listdir(PRODUCTS_DIR):
        product_path = os.path.join(PRODUCTS_DIR, product_folder, "details.json")
        if os.path.exists(product_path):
            with open(product_path, "r") as file:
                product_details = json.load(file)
                if query in product_details["name"].lower() or query in product_details["description"].lower():
                    matched_products.append(product_details)

    # Render the index.html template with search results
    return render_template("index.html", query=query, products=matched_products, search=True)

if __name__ == "__main__":
    app.run(debug=True)