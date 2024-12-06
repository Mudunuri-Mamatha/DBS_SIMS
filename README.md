
Smart Inventory Management System (SIMS)
Overview
The Smart Inventory Management System (SIMS) is a web-based application designed to simplify and optimize inventory management. It provides businesses with essential tools to manage inventory, suppliers, orders, warehouses, employees, and customers efficiently. The system is equipped with role-based dashboards tailored for specific users, enabling seamless operations across various functional areas.
With features like real-time low stock alerts, advanced analytics, profitability analysis, and revenue trends, SIMS serves as a comprehensive solution for managing inventory in a dynamic environment.

Key components
The key components of SIMS are:
Role-Based Dashboards:
Admin Dashboard: Provides comprehensive access to manage all entities and view analytics.
Supplier Dashboard: Focuses on supplier-specific data and order tracking.
Warehouse Dashboard: Includes inventory transactions and low stock alerts.
Finance Dashboard: Highlights revenue reports, profitability analysis, and high-value orders.
Sales Dashboard: Displays top-selling products, sales trends, and pending orders.
Core Functionalities:
CRUD operations for Products, Categories, Customers, Employees, Orders, Suppliers, and Warehouses.
Real-time low stock alerts and inventory transactions.
Advanced analytics like sales trends, profitability analysis, and revenue reports.
Authentication and Authorization:
Secure registration and login with role-based access control to ensure tailored experiences for each user role.
Analytics and Insights:
Top-selling products, orders by status, high-value orders, and revenue trends.
Search functionalities for customers and orders, with comprehensive result pages.
Database Integration:
Well-designed database in BCNF or 3NF, accommodating relational dependencies and constraints efficiently.
User-Friendly Interface:
Responsive frontend built with HTML and CSS, providing a seamless user experience.

Functionality Details
The Smart Inventory Management System (SIMS) provides both basic and advanced functionalities to streamline inventory operations and meet diverse business needs. Each function is meticulously implemented to ensure efficiency, user-friendliness, and data accuracy.
Basic Functions
CRUD Operations for Core Entities
Products:
Add, view, update, and delete products with attributes such as name, price, cost, profit, and description.
Implementation:
SQL INSERT, SELECT, UPDATE, and DELETE queries in Flask routes.
Frontend forms for product details with validation.
Category:
Manage categories for product classification (e.g., electronics, groceries).
Customer:
Maintain customer records including name, contact, address, and credit limit.
Employee:
Manage employee information such as role, hire date, and warehouse assignment.
Order:
CRUD for orders to handle customer purchases, supplier orders, and associated product quantities.
Supplier:
Manage supplier information such as contact details, ratings, and performance metrics.
Warehouse:
Track warehouse locations, addresses, and associated employees.
Advanced Functions
Dashboards


Admin Dashboard:
Comprehensive control over all entities.
Access to advanced reports, user management, and system settings.
Supplier Dashboard:
Manage supplier details and view order details.
Warehouse Dashboard:
Handle warehouse data, predictive reordering, and low stock alerts.
Finance Dashboard:
View profitability analysis, revenue by month, and high-value orders.
Sales Dashboard:
Analyze sales trends, pending orders, top-selling products, and total sales.
Implementation:
Dashboards built with Flask routes and dynamic templates.
Responsive design using Bootstrap for seamless navigation.
Add Inventory Transaction


Record additions and removals of inventory with transaction type and quantities.
Implementation:
Dropdowns for product selection and transaction type.
SQL queries to update the inventory transaction table.
High-Value Orders


Identify orders exceeding a specific monetary threshold.
Implementation:
SQL queries to filter orders based on Total_Amount.
Results displayed on a dynamically generated report.
Low Stock Alerts


Notify users when product quantities fall below predefined thresholds.
Implementation:
SQL queries to identify products with stock below the threshold.
Alerts displayed on dashboards.
Order Details


Display detailed order information, including customer, product, and status.
Implementation:
Join queries to fetch related order details.
Dynamic tables for presentation.
Orders by Status


Categorize and display orders based on their status (e.g., Pending, Shipped, Delivered).
Implementation:
SQL filtering by the OrderStatus field.
AJAX for filtering without reloading.
Pending Orders


Display orders awaiting processing or shipment.
Implementation:
SQL queries to filter orders with "Pending" status.
Update status directly from the interface.
Profitability Analysis


Calculate total profit for each product or category.
Implementation:
SQL aggregation (SUM) on the profit of sold items.
Visualization using Chart.js for bar and pie charts.
Registration and Login


User registration with role assignment.
Secure login with password hashing and session management.
Implementation:
Passwords hashed with bcrypt.
Role-based access control using session variables.
Role-Based Authentication


Restrict access to specific functionalities based on user roles (e.g., Admin, Finance).
Implementation:
Middleware checks in Flask routes for role validation.
Revenue by Month


Monthly revenue reports for sales and orders.
Implementation:
SQL queries to calculate monthly revenue.
Bar charts using Chart.js for visualization.
Sales Trends


Analyze trends based on customer purchases and total sales.
Implementation:
SQL queries grouped by customer and time.
Dynamic tables and charts for display.
Search Customers


Search for customers by name, ID, or contact details.
Implementation:
AJAX for real-time search.
SQL queries with LIKE operator for partial matches.
Search Orders


Retrieve order details based on filters like order ID, status, or customer.
Implementation:
SQL joins to fetch comprehensive details.
Results displayed dynamically.
Top Products


Identify top-selling products based on sales volume.
Implementation:
SQL aggregation and sorting to rank products.
Visualization using bar charts.
Top Sales


Highlight highest revenue-generating sales records.
Implementation:
SQL queries sorted by total revenue.
Data presented in dynamic tables.
Logout


Secure session termination for users.
Implementation:
Flask session.clear() method to remove session data.
Integration and Implementation
Each feature integrates seamlessly into the SIMS system using the Flask backend for business logic and MySQL for data storage.
The user interface employs Bootstrap for responsiveness and AJAX for dynamic interactions.
Features are modular, ensuring scalability for future enhancements.
This combination of basic and advanced functionalities provides a comprehensive inventory management solution tailored to diverse business needs.

Project Setup
Steps to Run the Project
1.Navigate to the project folder: Open the terminal and navigate to the root directory of the project.


2. Create a virtual environment:
 python -m venv venv
3. Activate the virtual environment:
On Windows:
 venv\Scripts\activate
On Mac/Linux:
 source venv/bin/activate

4. Install the required dependencies:

 pip install -r requirements.txt

5. Set up the database:
Ensure that MySQL server is running.
Connect to the MySQL Workbench and create the database using the provided schema.
6. Run the application:

 python app.py

7. Access the application: Open your browser and navigate to http://127.0.0.1:5000/.



Implementation Details
Backend
Framework: Python Flask
Database: MySQL, integrated using Flask-MySQLdb
Business Logic: Core operations like CRUD, analytics, and role-based access are implemented in Flask routes.
Security: Password hashing with bcrypt and session-based authentication for role-specific access control.
Frontend
Languages: HTML, CSS
Frameworks and Libraries: Bootstrap for responsiveness, Chart.js for data visualization, and AJAX for dynamic UI updates.
Templates: Dynamic pages built with Flask's Jinja2 templating engine.

