from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

INVENTORY_FILE = "inventory.csv"

def load_inventory():
    try:
        with open(INVENTORY_FILE, newline='', mode='r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def save_inventory(data):
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_product():
    inventory = load_inventory()
    product_id = request.form['product_id']
    if any(item['Product ID'] == product_id for item in inventory):
        return "Error: Product ID already exists.", 400
    new_product = {
        "Product ID": product_id,
        "Product Name": request.form['product_name'],
        "Category": request.form['category'],
        "Price": request.form['price'],
        "Stock": request.form['stock'],
        "Total Sales": "0"
    }
    inventory.append(new_product)
    save_inventory(inventory)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
