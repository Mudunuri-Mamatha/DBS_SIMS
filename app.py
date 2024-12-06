from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = "1aae12d981e28a8dc451e0ce37204376a6f86524b2a390f5"
db = SQLAlchemy(app)

# Define database models
class Product(db.Model):
    __tablename__ = 'Product'
    Product_ID = db.Column(db.Integer, primary_key=True)
    Product_Name = db.Column(db.String(100), nullable=False)
    Product_list_price = db.Column(db.Float, nullable=False)
    Profit = db.Column(db.Float, nullable=False)
    Product_description = db.Column(db.String(200))
    Category_ID = db.Column(db.Integer, db.ForeignKey('Category.Category_ID'), nullable=False)
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)

class Customer(db.Model):
    __tablename__ = 'Customer'
    Cust_ID = db.Column(db.Integer, primary_key=True)
    CustName = db.Column(db.String(100), nullable=False)
    Cust_Phone = db.Column(db.String(15), nullable=False)
    Cust_addr = db.Column(db.String(200), nullable=False)
    Cust_email = db.Column(db.String(100), nullable=False)
    Cust_credit_limit = db.Column(db.Float, nullable=False)

class Category(db.Model):
    __tablename__ = 'Category'
    Category_ID = db.Column(db.Integer, primary_key=True)
    Category_Name = db.Column(db.String(100), nullable=False)

class Supplier(db.Model):
    __tablename__ = 'Supplier'
    Supplier_ID = db.Column(db.Integer, primary_key=True)
    Supplier_name = db.Column(db.String(100), nullable=False)
    Supplier_contact = db.Column(db.String(100), nullable=False)
    Supplier_rating = db.Column(db.Float, nullable=False)

class Warehouse(db.Model):
    __tablename__ = 'Warehouse'
    Warehouse_ID = db.Column(db.Integer, primary_key=True)
    Warehouse_Name = db.Column(db.String(100), nullable=False)
    Warehouse_Addr = db.Column(db.String(200), nullable=False)

class Employee(db.Model):
    __tablename__ = 'Employee'
    Emp_ID = db.Column(db.Integer, primary_key=True)
    Emp_Name = db.Column(db.String(100), nullable=False)
    Emp_Email = db.Column(db.String(100), nullable=False)
    Emp_Phone = db.Column(db.String(15), nullable=False)
    Emp_hiredate = db.Column(db.Date, nullable=False)
    Emp_job_title = db.Column(db.String(100), nullable=False)
    Warehouse_ID = db.Column(db.Integer, db.ForeignKey('Warehouse.Warehouse_ID'), nullable=False)
    
class Order(db.Model):
    __tablename__ = 'Order1'
    OrderID = db.Column(db.Integer, primary_key=True)
    Order_Date = db.Column(db.Date, nullable=False)
    OrderStatus = db.Column(db.String(50), nullable=False)
    Total_amount = db.Column(db.Float, nullable=False)
    Total_item_qty = db.Column(db.Integer, nullable=False)
    Cust_ID = db.Column(db.Integer, db.ForeignKey('Customer.Cust_ID'), nullable=False)
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('Supplier.Supplier_ID'), nullable=False)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
     # Relationships
    customer = db.relationship('Customer', backref='orders', lazy=True)
    supplier = db.relationship('Supplier', backref='orders', lazy=True)
    product = db.relationship('Product', backref='orders', lazy=True)

class Role(db.Model):
    __tablename__ = 'Role'
    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(50), unique=True, nullable=False)

    # One-to-many relationship with User
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
    __tablename__ = 'User'
    User_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Role_ID = db.Column(db.Integer, db.ForeignKey('Role.Role_ID'), nullable=False)


class SalesHistory(db.Model):
    __tablename__ = 'sales_history'
    Sale_ID = db.Column(db.Integer, primary_key=True)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)
    Sale_Date = db.Column(db.Date, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)


class InventoryTransaction(db.Model):
    __tablename__ = 'InventoryTransaction'
    Transaction_ID = db.Column(db.Integer, primary_key=True)
    Transaction_Type = db.Column(db.String(50), nullable=False)  # 'Addition' or 'Removal'
    Quantity = db.Column(db.Integer, nullable=False)
    Transaction_Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID'), nullable=False)

    product = db.relationship('Product', backref='transactions', lazy=True)



# --- Routes ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    return render_template("index.html")

'''
@app.route('/')
def index():
    return render_template("index.html")
'''

@app.route('/success')
def success():
    return render_template("success.html")

# --- Product CRUD Operations ---
@app.route('/products', methods=["GET", "POST"])
def products():
    if request.method == "POST":
        try:
            name = request.form['product_name']
            price = float(request.form['product_list_price'])
            profit = float(request.form['profit'])
            description = request.form['product_description']
            category_id = int(request.form['category_id'])
            supplier_id = int(request.form['supplier_id'])

            if not Category.query.get(category_id):
                flash("Error: The specified Category_ID does not exist.")
                return redirect(url_for('products'))
            if not Supplier.query.get(supplier_id):
                flash("Error: The specified Supplier_ID does not exist.")
                return redirect(url_for('products'))

            new_product = Product(
                Product_Name=name,
                Product_list_price=price,
                Profit=profit,
                Product_description=description,
                Category_ID=category_id,
                Supplier_ID=supplier_id
            )
            db.session.add(new_product)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'products' route:", e)
            return f"An error occurred: {e}", 500

    try:
        products = Product.query.all()
        return render_template("products.html", products=products)
    except Exception as e:
        print("Error occurred while rendering 'products.html':", e)
        return f"An error occurred: {e}", 500

@app.route('/edit_product/<int:id>', methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.Product_Name = request.form['product_name']
        product.Product_list_price = float(request.form['product_list_price'])
        product.Profit = float(request.form['profit'])
        product.Product_description = request.form['product_description']
        product.Category_ID = int(request.form['category_id'])
        product.Supplier_ID = int(request.form['supplier_id'])

        # Validate foreign key relationships
        if not Category.query.get(product.Category_ID):
            flash("Error: Invalid Category_ID.")
            return redirect(url_for('edit_product', id=id))
        if not Supplier.query.get(product.Supplier_ID):
            flash("Error: Invalid Supplier_ID.")
            return redirect(url_for('edit_product', id=id))

        db.session.commit()
        flash("Product updated successfully!")
        return redirect(url_for('products'))
    return render_template("edit_product.html", product=product)


@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted!")
    return redirect(url_for('products'))

# --- Customer CRUD Operations ---
@app.route('/customers', methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        try:
            name = request.form['cust_name']
            phone = request.form['cust_phone']
            address = request.form['cust_addr']
            email = request.form['cust_email']
            credit_limit = float(request.form['cust_credit_limit'])

            new_customer = Customer(
                CustName=name,
                Cust_Phone=phone,
                Cust_addr=address,
                Cust_email=email,
                Cust_credit_limit=credit_limit
            )
            db.session.add(new_customer)
            db.session.commit()
            flash("Customer added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'customers' route:", e)
            return f"An error occurred: {e}", 500

    try:
        customers = Customer.query.all()
        return render_template("customers.html", customers=customers)
    except Exception as e:
        print("Error occurred while rendering 'customers.html':", e)
        return f"An error occurred: {e}", 500
    
@app.route('/edit_customer/<int:id>', methods=["GET", "POST"])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == "POST":
        try:
            customer.CustName = request.form['cust_name']
            customer.Cust_Phone = request.form['cust_phone']
            customer.Cust_addr = request.form['cust_addr']
            customer.Cust_email = request.form['cust_email']
            customer.Cust_credit_limit = float(request.form['cust_credit_limit'])

            db.session.commit()
            flash("Customer updated successfully!")
            return redirect(url_for('customers'))
        except Exception as e:
            flash(f"An error occurred while updating the customer: {e}")
            return redirect(url_for('edit_customer', id=id))

    return render_template("edit_customer.html", customer=customer)


@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted!")
    return redirect(url_for('customers'))

# --- Category CRUD Operations ---
@app.route('/categories', methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        try:
            name = request.form['category_name']
            new_category = Category(Category_Name=name)
            db.session.add(new_category)
            db.session.commit()
            flash("Category added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'categories' route:", e)
            return f"An error occurred: {e}", 500

    try:
        categories = Category.query.all()
        return render_template("categories.html", categories=categories)
    except Exception as e:
        print("Error occurred while rendering 'categories.html':", e)
        return f"An error occurred: {e}", 500
    
@app.route('/edit_category/<int:id>', methods=["GET", "POST"])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        try:
            category.Category_Name = request.form['category_name']
            db.session.commit()
            flash("Category updated successfully!")
            return redirect(url_for('categories'))
        except Exception as e:
            flash(f"An error occurred while updating the category: {e}")
            return redirect(url_for('edit_category', id=id))

    return render_template("edit_category.html", category=category)


@app.route('/delete_category/<int:id>')
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted!")
    return redirect(url_for('categories'))

# --- Supplier CRUD Operations ---
@app.route('/suppliers', methods=["GET", "POST"])
def suppliers():
    if request.method == "POST":
        try:
            name = request.form['supplier_name']
            contact = request.form['supplier_contact']
            rating = float(request.form['supplier_rating'])

            new_supplier = Supplier(
                Supplier_name=name,
                Supplier_contact=contact,
                Supplier_rating=rating
            )
            db.session.add(new_supplier)
            db.session.commit()
            flash("Supplier added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'suppliers' route:", e)
            return f"An error occurred: {e}", 500

    try:
        suppliers = Supplier.query.all()
        return render_template("suppliers.html", suppliers=suppliers)
    except Exception as e:
        print("Error occurred while rendering 'suppliers.html':", e)
        return f"An error occurred: {e}", 500
    
@app.route('/edit_supplier/<int:id>', methods=["GET", "POST"])
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == "POST":
        try:
            supplier.Supplier_name = request.form['supplier_name']
            supplier.Supplier_contact = request.form['supplier_contact']
            supplier.Supplier_rating = float(request.form['supplier_rating'])

            db.session.commit()
            flash("Supplier updated successfully!")
            return redirect(url_for('suppliers'))
        except Exception as e:
            flash(f"An error occurred while updating the supplier: {e}")
            return redirect(url_for('edit_supplier', id=id))

    return render_template("edit_supplier.html", supplier=supplier)


@app.route('/delete_supplier/<int:id>')
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash("Supplier deleted!")
    return redirect(url_for('suppliers'))

# --- Warehouse CRUD Operations ---
@app.route('/warehouses', methods=["GET", "POST"])
def warehouses():
    if request.method == "POST":
        try:
            name = request.form['warehouse_name']
            address = request.form['warehouse_addr']

            new_warehouse = Warehouse(
                Warehouse_Name=name,
                Warehouse_Addr=address
            )
            db.session.add(new_warehouse)
            db.session.commit()
            flash("Warehouse added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'warehouses' route:", e)
            return f"An error occurred: {e}", 500

    try:
        warehouses = Warehouse.query.all()
        return render_template("warehouses.html", warehouses=warehouses)
    except Exception as e:
        print("Error occurred while rendering 'warehouses.html':", e)
        return f"An error occurred: {e}", 500
    
@app.route('/edit_warehouse/<int:id>', methods=["GET", "POST"])
def edit_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    if request.method == "POST":
        try:
            warehouse.Warehouse_Name = request.form['warehouse_name']
            warehouse.Warehouse_Addr = request.form['warehouse_addr']

            db.session.commit()
            flash("Warehouse updated successfully!")
            return redirect(url_for('warehouses'))
        except Exception as e:
            flash(f"An error occurred while updating the warehouse: {e}")
            return redirect(url_for('edit_warehouse', id=id))

    return render_template("edit_warehouse.html", warehouse=warehouse)


@app.route('/delete_warehouse/<int:id>')
def delete_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    db.session.delete(warehouse)
    db.session.commit()
    flash("Warehouse deleted!")
    return redirect(url_for('warehouses'))

# --- Employee CRUD Operations with Foreign Key Check ---
@app.route('/employees', methods=["GET", "POST"])
def employees():
    if request.method == "POST":
        try:
            name = request.form['emp_name']
            email = request.form['emp_email']
            phone = request.form['emp_phone']
            hiredate = datetime.strptime(request.form['emp_hiredate'], '%Y-%m-%d').date()
            job_title = request.form['emp_job_title']
            warehouse_id = int(request.form['warehouse_id'])

            if not Warehouse.query.get(warehouse_id):
                flash("Error: The specified Warehouse_ID does not exist.")
                return redirect(url_for('employees'))

            new_employee = Employee(
                Emp_Name=name,
                Emp_Email=email,
                Emp_Phone=phone,
                Emp_hiredate=hiredate,
                Emp_job_title=job_title,
                Warehouse_ID=warehouse_id
            )
            db.session.add(new_employee)
            db.session.commit()
            flash("Employee added successfully!")
            return redirect(url_for('success'))
        
        except Exception as e:
            print("Error occurred in 'employees' route:", e)
            return f"An error occurred: {e}", 500

    try:
        employees = Employee.query.all()
        return render_template("employees.html", employees=employees)
    except Exception as e:
        print("Error occurred while rendering 'employees.html':", e)
        return f"An error occurred: {e}", 500
    
@app.route('/edit_employee/<int:id>', methods=["GET", "POST"])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        try:
            employee.Emp_Name = request.form['emp_name']
            employee.Emp_Email = request.form['emp_email']
            employee.Emp_Phone = request.form['emp_phone']
            employee.Emp_hiredate = datetime.strptime(request.form['emp_hiredate'], '%Y-%m-%d').date()
            employee.Emp_job_title = request.form['emp_job_title']
            employee.Warehouse_ID = int(request.form['warehouse_id'])

            # Validate foreign key relationship
            if not Warehouse.query.get(employee.Warehouse_ID):
                flash("Error: The specified Warehouse_ID does not exist.")
                return redirect(url_for('edit_employee', id=id))

            db.session.commit()
            flash("Employee updated successfully!")
            return redirect(url_for('employees'))
        except Exception as e:
            flash(f"An error occurred while updating the employee: {e}")
            return redirect(url_for('edit_employee', id=id))

    return render_template("edit_employee.html", employee=employee)


@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted!")
    return redirect(url_for('employees'))
    

# --- Orders CRUD Operations ---
@app.route('/orders', methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        try:
            # Log form data for debugging
            print("Received form data:", request.form)

            # Get data from the form
            order_date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
            order_status = request.form['order_status']
            total_amount = float(request.form['total_amount'])
            total_item_qty = int(request.form['total_item_qty'])
            cust_id = int(request.form['cust_id'])
            supplier_id = int(request.form['supplier_id'])
            product_id = int(request.form['product_id'])

            # Check if Cust_ID, Supplier_ID, and Product_ID exist in their respective tables
            if not Customer.query.get(cust_id):
                flash("Error: The specified Customer ID does not exist.")
                return redirect(url_for('orders'))
            if not Supplier.query.get(supplier_id):
                flash("Error: The specified Supplier ID does not exist.")
                return redirect(url_for('orders'))
            if not Product.query.get(product_id):
                flash("Error: The specified Product ID does not exist.")
                return redirect(url_for('orders'))

            # Add the order if foreign keys are valid
            new_order = Order(
                Order_Date=order_date,
                OrderStatus=order_status,
                Total_amount=total_amount,
                Total_item_qty=total_item_qty,
                Cust_ID=cust_id,
                Supplier_ID=supplier_id,
                Product_ID=product_id
            )
            db.session.add(new_order)
            db.session.commit()
            flash("Order added successfully!")
            return redirect(url_for('orders'))

        except Exception as e:
            print("Error occurred in 'orders' route:", e)
            return f"An error occurred: {e}", 500

    try:
        orders = Order.query.all()
        return render_template("orders.html", orders=orders)
    except Exception as e:
        print("Error occurred while rendering 'orders.html':", e)
        return f"An error occurred: {e}", 500



@app.route('/edit_order/<int:id>', methods=["GET", "POST"])
def edit_order(id):
    order = Order.query.get_or_404(id)
    if request.method == "POST":
        try:
            order.Order_Date = datetime.strptime(request.form['order_date'], '%Y-%m-%d').date()
            order.OrderStatus = request.form['order_status']
            order.Total_amount = float(request.form['total_amount'])
            order.Total_item_qty = int(request.form['total_item_qty'])
            order.Cust_ID = int(request.form['cust_id'])
            order.Supplier_ID = int(request.form['supplier_id'])
            order.Product_ID = int(request.form['product_id'])

            # Validate foreign key relationships
            if not Customer.query.get(order.Cust_ID):
                flash("Error: The specified Customer_ID does not exist.")
                return redirect(url_for('edit_order', id=id))
            if not Supplier.query.get(order.Supplier_ID):
                flash("Error: The specified Supplier_ID does not exist.")
                return redirect(url_for('edit_order', id=id))
            if not Product.query.get(order.Product_ID):
                flash("Error: The specified Product_ID does not exist.")
                return redirect(url_for('edit_order', id=id))

            db.session.commit()
            flash("Order updated successfully!")
            return redirect(url_for('orders'))
        except Exception as e:
            flash(f"An error occurred while updating the order: {e}")
            return redirect(url_for('edit_order', id=id))

    return render_template("edit_order.html", order=order)


@app.route('/delete_order/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash("Order deleted!")
    return redirect(url_for('orders'))

@app.route('/search_customers', methods=["GET", "POST"])
def search_customers():
    if request.method == "POST":
        query = request.form['query']
        # Search for customers whose name or phone number matches the query
        results = Customer.query.filter(
            (Customer.CustName.ilike(f"%{query}%")) | 
            (Customer.Cust_Phone.ilike(f"%{query}%"))
        ).all()
        return render_template("search_customers_results.html", customers=results)
    return render_template("search_customers.html")

@app.route('/search_orders', methods=["GET", "POST"])
def search_orders():
    if request.method == "POST":
        query = request.form['query']
        # Search for orders by status or customer ID
        results = Order.query.filter(
            (Order.OrderStatus.ilike(f"%{query}%")) |
            (Order.Cust_ID == query)
        ).all()
        return render_template("search_orders_results.html", orders=results)
    return render_template("search_orders.html")

@app.route('/order_details', methods=["GET"])
def order_details():
    try:
        results = db.session.query(
            Order.OrderID,
            Order.Order_Date,
            Customer.CustName.label("Customer_Name"),
            Supplier.Supplier_name.label("Supplier_Name"),
            Product.Product_Name.label("Product_Name"),
            Order.OrderStatus.label("Status"),
            Order.Total_amount.label("Total_Amount"),
            Order.Total_item_qty.label("Total_Quantity")
        ).join(Customer, Order.Cust_ID == Customer.Cust_ID
        ).join(Supplier, Order.Supplier_ID == Supplier.Supplier_ID
        ).join(Product, Order.Product_ID == Product.Product_ID
        ).all()

        return render_template("order_details.html", orders=results)
    except Exception as e:
        print(f"Error in fetching order details: {e}")
        return f"An error occurred: {e}", 500



@app.route('/total_sales', methods=["GET"])
def total_sales():
    try:
        results = db.session.query(
            Product.Product_Name,
            db.func.sum(Order.Total_item_qty).label("Total_Quantity_Sold"),
            db.func.sum(Order.Total_amount).label("Total_Sales")
        ).join(Product, Order.Product_ID == Product.Product_ID
        ).group_by(Product.Product_Name).all()

        return render_template("total_sales.html", sales=results)
    except Exception as e:
        print(f"Error in fetching total sales data: {e}")
        return f"An error occurred: {e}", 500


@app.route('/top_products')
def top_products():
    # Query to calculate the top 5 products based on total quantity sold
    results = db.session.query(
        Product.Product_Name,
        db.func.sum(Order.Total_item_qty).label("TotalQuantity")
    ).join(Order, Order.Product_ID == Product.Product_ID) \
        .group_by(Product.Product_Name) \
        .order_by(db.desc("TotalQuantity")).limit(5).all()

    return render_template("top_products.html", products=results)

@app.route('/orders_by_status')
def orders_by_status():
    # Query to count the number of orders grouped by their status
    results = db.session.query(
        Order.OrderStatus,
        db.func.count(Order.OrderID).label("OrderCount")
    ).group_by(Order.OrderStatus).all()

    return render_template("orders_by_status.html", statuses=results)

@app.route('/high_value_orders')
def high_value_orders():
    # Query to fetch orders with a total amount greater than a certain threshold
    threshold = 500.0  # Define the threshold value
    results = db.session.query(
        Order.OrderID,
        Order.Order_Date,
        Order.Total_amount,
        Customer.CustName
    ).join(Customer, Order.Cust_ID == Customer.Cust_ID) \
        .filter(Order.Total_amount > threshold).all()

    return render_template("high_value_orders.html", orders=results)

@app.route('/revenue_by_month')
def revenue_by_month():
    # Query to calculate total revenue grouped by month
    results = db.session.query(
        db.func.date_format(Order.Order_Date, '%Y-%m').label("Month"),
        db.func.sum(Order.Total_amount).label("TotalRevenue")
    ).group_by("Month").all()

    return render_template("revenue_by_month.html", revenues=results)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        role_name = request.form['role']  # Role selected from the dropdown

        # Fetch Role_ID based on Role_Name
        role = Role.query.filter_by(Role_Name=role_name).first()
        if not role:
            flash("Invalid role selected!")
            return redirect(url_for('register'))

        # Hash the password (Optional, for security)
        hashed_password = password  # Use `bcrypt` or similar library to hash passwords

        # Create and save the user
        new_user = User(Username=username, Password=hashed_password, Role_ID=role.Role_ID)
        db.session.add(new_user)
        db.session.commit()

        flash("User registered successfully!")
        return redirect(url_for('login'))

    return render_template("register.html")

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != required_role:
                flash("You do not have permission to access this page.")
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Verify user credentials
        user = User.query.filter_by(Username=username, Password=password).first()
        if user:
            # Store user details and role in the session
            session['user_id'] = user.User_ID
            session['username'] = user.Username
            session['user_role'] = user.role.Role_Name  # Access Role_Name through the relationship

            flash("Logged in successfully!")
            return redirect(url_for('index'))

        flash("Invalid username or password!")
        return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/admin_dashboard')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/warehouse_dashboard')
@role_required('warehouse')
def warehouse_dashboard():
    return render_template('warehouse_dashboard.html')

@app.route('/sales_dashboard')
@role_required('sales')
def sales_dashboard():
    return render_template('sales_dashboard.html')

@app.route('/supplier_dashboard')
@role_required('supplier')
def supplier_dashboard():
    return render_template('supplier_dashboard.html')

@app.route('/finance_dashboard')
@role_required('finance')
def finance_dashboard():
    return render_template('finance_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/pending_orders', methods=['GET', 'POST'])
@role_required('sales')
def pending_orders():
    if request.method == 'POST':
        order_id = request.form['order_id']
        new_status = request.form['status']

        order = Order.query.get(order_id)
        if order:
            order.OrderStatus = new_status
            db.session.commit()
            flash('Order status updated successfully!')
        else:
            flash('Order not found.')

    pending_orders = Order.query.filter_by(OrderStatus='Pending').all()
    return render_template('pending_orders.html', orders=pending_orders)

@app.route('/sales_trends')
@role_required('sales')
def sales_trends():
    trends = db.session.query(
        Customer.Cust_ID,
        Customer.CustName,
        db.func.sum(Order.Total_item_qty).label('TotalItemsBought'),
        db.func.sum(Order.Total_amount).label('TotalSpent')
    ).join(Order, Customer.Cust_ID == Order.Cust_ID) \
        .group_by(Customer.Cust_ID, Customer.CustName) \
        .order_by(db.desc('TotalSpent')).all()
    return render_template('sales_trends.html', trends=trends)




'''
@app.route('/predictive_reorder', methods=["GET"])
def predictive_reorder():
    from datetime import timedelta, date

    # Query products
    products = db.session.query(Product.Product_ID, Product.Product_Name).all()
    reorder_list = []

    # Iterate over each product
    for product in products:
        # Query sales data for the product
        sales_data = db.session.query(
            SalesHistory.Sale_Date, db.func.sum(SalesHistory.Quantity).label("TotalQuantity")
        ).filter(SalesHistory.Product_ID == product.Product_ID).group_by(SalesHistory.Sale_Date).all()

        if len(sales_data) < 5:
            continue  # Skip products with insufficient data

        # Calculate daily sales averages (rolling weekly demand)
        sales_data.sort(key=lambda x: x[0])  # Ensure data is sorted by date
        total_days = (sales_data[-1][0] - sales_data[0][0]).days + 1
        daily_sales = [0] * total_days

        # Map daily sales
        start_date = sales_data[0][0]
        for sale in sales_data:
            index = (sale[0] - start_date).days
            daily_sales[index] = sale[1]

        # Calculate moving average (7-day window)
        window = 7
        moving_avg = [
            sum(daily_sales[i:i + window]) / window
            for i in range(len(daily_sales) - window + 1)
        ]
        predicted_demand = moving_avg[-1] if moving_avg else 0

        # Calculate current stock (cumulative sales)
        total_sold = sum(sale[1] for sale in sales_data)
        if total_sold < predicted_demand:
            reorder_list.append({
                "Product_Name": product.Product_Name,
                "Reorder_Quantity": int(predicted_demand - total_sold)
            })

    return render_template("predictive_reorder.html", reorder_list=reorder_list)
'''

@app.route('/predictive_reorder', methods=["GET"])
def predictive_reorder():
    from datetime import timedelta, date

    # Query products
    products = db.session.query(Product.Product_ID, Product.Product_Name).all()
    reorder_list = []

    # Simulated current stock for testing
    simulated_stock = {
        101: 15,  # Product A
        102: 10   # Product B
    }

    # Iterate over each product
    for product in products:
        # Query sales data for the product
        sales_data = db.session.query(
            SalesHistory.Sale_Date, db.func.sum(SalesHistory.Quantity).label("TotalQuantity")
        ).filter(SalesHistory.Product_ID == product.Product_ID).group_by(SalesHistory.Sale_Date).all()

        if len(sales_data) < 5:
            continue  # Skip products with insufficient data

        # Calculate daily sales averages (rolling weekly demand)
        sales_data.sort(key=lambda x: x[0])  # Ensure data is sorted by date
        total_days = (sales_data[-1][0] - sales_data[0][0]).days + 1
        daily_sales = [0] * total_days

        # Map daily sales
        start_date = sales_data[0][0]
        for sale in sales_data:
            index = (sale[0] - start_date).days
            daily_sales[index] = sale[1]

        # Calculate moving average (7-day window)
        window = 7
        moving_avg = [
            sum(daily_sales[i:i + window]) / window
            for i in range(len(daily_sales) - window + 1)
        ]
        predicted_demand = moving_avg[-1] if moving_avg else 0

        # Get current stock from simulated data
        current_stock = simulated_stock.get(product.Product_ID, 0)

        # Append to reorder list if stock is insufficient
        if current_stock < predicted_demand:
            reorder_list.append({
                "Product_Name": product.Product_Name,
                "Reorder_Quantity": int(predicted_demand - current_stock)
            })

    return render_template("predictive_reorder.html", reorder_list=reorder_list)


@app.route('/add_inventory_transaction', methods=["GET", "POST"])
@role_required('warehouse')
def add_inventory_transaction():
    if request.method == "POST":
        try:
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
            transaction_type = request.form['transaction_type']

            new_transaction = InventoryTransaction(
                Product_ID=product_id,
                Quantity=quantity,
                Transaction_Type=transaction_type
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash("Inventory transaction added successfully!")
            return redirect(url_for('warehouse_dashboard'))
        except Exception as e:
            flash(f"Error occurred: {e}")
            return redirect(url_for('add_inventory_transaction'))

    products = Product.query.all()
    return render_template('add_inventory_transaction.html', products=products)



@app.route('/low_stock_alerts')
@role_required('warehouse')
def low_stock_alerts():
    # Set a low stock threshold
    low_stock_threshold = 10

    # Query to calculate stock levels dynamically using inventory transactions
    stock_data = db.session.query(
        Product.Product_ID,
        Product.Product_Name,
        db.func.coalesce(
            db.func.sum(
                db.case(
                    (InventoryTransaction.Transaction_Type == 'Addition', InventoryTransaction.Quantity)
                )
            ), 0).label('Total_Added'),
        db.func.coalesce(
            db.func.sum(
                db.case(
                    (InventoryTransaction.Transaction_Type == 'Removal', InventoryTransaction.Quantity)
                )
            ), 0).label('Total_Removed')
    ).outerjoin(InventoryTransaction, InventoryTransaction.Product_ID == Product.Product_ID
    ).group_by(Product.Product_ID).all()

    # Identify products with low stock
    low_stock = [
        {
            "Product_ID": product.Product_ID,
            "Product_Name": product.Product_Name,
            "Current_Stock": product.Total_Added - product.Total_Removed
        }
        for product in stock_data if product.Total_Added - product.Total_Removed < low_stock_threshold
    ]

    return render_template('low_stock_alerts.html', products=low_stock)

@app.route('/profitability_analysis')
@role_required('finance')
def profitability_analysis():
    # Query to calculate total profit for each product
    profitability = db.session.query(
        Product.Product_Name,
        db.func.sum(Order.Total_item_qty * Product.Profit).label('Total_Profit')
    ).join(Order, Product.Product_ID == Order.Product_ID).group_by(Product.Product_Name).all()
    
    # Prepare data for the chart
    labels = [product.Product_Name for product in profitability]
    data = [product.Total_Profit for product in profitability]
    
    return render_template(
        'profitability_analysis.html', 
        labels=labels, 
        data=data
    )



if __name__ == "__main__":
    app.run(debug=True)
