# Smart Inventory Management System (SIMS)

## Overview
The Smart Inventory Management System (SIMS) is a web-based application designed to simplify and optimize inventory management. It provides businesses with essential tools to manage inventory, suppliers, orders, warehouses, employees, and customers efficiently. The system is equipped with role-based dashboards tailored for specific users, enabling seamless operations across various functional areas.

With features like real-time low stock alerts, advanced analytics, profitability analysis, and revenue trends, SIMS serves as a comprehensive solution for managing inventory in a dynamic environment.

---

## Key Components

### Role-Based Dashboards
- **Admin Dashboard**: Provides comprehensive access to manage all entities and view analytics.
- **Supplier Dashboard**: Focuses on supplier-specific data and order tracking.
- **Warehouse Dashboard**: Includes inventory transactions and low stock alerts.
- **Finance Dashboard**: Highlights revenue reports, profitability analysis, and high-value orders.
- **Sales Dashboard**: Displays top-selling products, sales trends, and pending orders.

### Core Functionalities
- CRUD operations for Products, Categories, Customers, Employees, Orders, Suppliers, and Warehouses.
- Real-time low stock alerts and inventory transactions.
- Advanced analytics like sales trends, profitability analysis, and revenue reports.

### Authentication and Authorization
- Secure registration and login with role-based access control to ensure tailored experiences for each user role.

### Analytics and Insights
- Top-selling products, orders by status, high-value orders, and revenue trends.
- Search functionalities for customers and orders, with comprehensive result pages.

### Database Integration
- Well-designed database in BCNF or 3NF, accommodating relational dependencies and constraints efficiently.

### User-Friendly Interface
- Responsive frontend built with HTML and CSS, providing a seamless user experience.

---

## Functionality Details

### Basic Functions
#### CRUD Operations for Core Entities
1. **Products**: Add, view, update, and delete products with attributes such as name, price, cost, profit, and description.
2. **Categories**: Manage categories for product classification (e.g., electronics, groceries).
3. **Customers**: Maintain customer records, including name, contact, address, and credit limit.
4. **Employees**: Manage employee information such as role, hire date, and warehouse assignment.
5. **Orders**: CRUD for orders to handle customer purchases, supplier orders, and associated product quantities.
6. **Suppliers**: Manage supplier information such as contact details, ratings, and performance metrics.
7. **Warehouses**: Track warehouse locations, addresses, and associated employees.

---

### Advanced Functions
1. **Dashboards**:
   - Tailored dashboards for Admin, Supplier, Warehouse, Finance, and Sales roles.
   - Built with Flask routes and dynamic templates.
   - Responsive design using Bootstrap.

2. **Add Inventory Transactions**:
   - Record additions and removals of inventory with transaction type and quantities.

3. **High-Value Orders**:
   - Identify orders exceeding a specific monetary threshold.

4. **Low Stock Alerts**:
   - Notify users when product quantities fall below predefined thresholds.

5. **Profitability Analysis**:
   - Calculate total profit for each product or category.
   - Visualized using Chart.js for bar and pie charts.

6. **Revenue by Month**:
   - Monthly revenue reports for sales and orders.

7. **Sales Trends**:
   - Analyze trends based on customer purchases and total sales.

8. **Search Functionalities**:
   - Search customers by name, ID, or contact details.
   - Retrieve order details based on filters like order ID, status, or customer.

9. **Top Products and Sales**:
   - Identify top-selling products and highest revenue-generating sales records.

10. **Logout**:
   - Secure session termination for users.

---

## Project Setup

### Steps to Run the Project
1. **Navigate to the project folder**  
   Open the terminal and navigate to the root directory of the project:
   ```bash
   cd <project-folder>

2. **Create a virtual environment**  
   Run the following command to create a virtual environment for the project:
   ```bash
   python -m venv venv

3. **Activate the virtual environment**  
   On Windows, run:  
   ```bash
   venv\Scripts\activate

On Mac/Linux, run:
```bash
source venv/bin/activate

4. **Install the required dependencies**  
   Run the following command to install all the dependencies listed in the `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt

5. **Set up the database**  
   Ensure that the MySQL server is running.  
   Connect to MySQL Workbench or your preferred MySQL client and execute the following steps:  
   1. Create the database using the provided schema.  
   2. Verify the database structure matches the schema requirements.

6. **Run the application**  
   Use the following command to start the application:  
   ```bash
   python app.py


7. **Access the application**  
   Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).


