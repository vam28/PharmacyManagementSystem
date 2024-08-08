<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Platform README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #333;
        }
        pre {
            background: #f4f4f4;
            border: 1px solid #ddd;
            padding: 10px;
            overflow: auto;
        }
        code {
            font-family: monospace;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .code-block {
            background-color: #f9f9f9;
            border: 1px solid #e1e1e1;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>E-Commerce Platform</h1>
        <p>This is a simple e-commerce platform built using Streamlit and MySQL. It allows users to add, view, and delete products, and manage a shopping cart. The platform includes functionalities for administrators to manage products and categories, and for customers to view and add products to their cart.</p>

        <h2>Features</h2>
        <ul>
            <li><strong>Admin Interface:</strong></li>
            <ul>
                <li>Add new products and categories.</li>
                <li>View all products with their categories.</li>
                <li>Delete products.</li>
            </ul>
            <li><strong>Customer Interface:</strong></li>
            <ul>
                <li>View all available products.</li>
                <li>Add products to the cart.</li>
                <li>View cart total.</li>
                <li>Delete products from the cart.</li>
            </ul>
        </ul>

        <h2>Prerequisites</h2>
        <ul>
            <li>Python 3.6 or higher</li>
            <li>MySQL Server</li>
        </ul>

        <h2>Installation</h2>
        <ol>
            <li>Clone the repository:
                <div class="code-block">
                    <pre><code>git clone https://github.com/your-username/e-commerce-platform.git
cd e-commerce-platform</code></pre>
                </div>
            </li>
            <li>Install the required Python packages:
                <div class="code-block">
                    <pre><code>pip install -r requirements.txt</code></pre>
                </div>
            </li>
            <li>Set up the MySQL database:
                <div class="code-block">
                    <pre><code>CREATE DATABASE mydatabase;
USE mydatabase;

CREATE TABLE IF NOT EXISTS Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

CREATE TABLE IF NOT EXISTS Cart (
    customer_id INT,
    product_id INT,
    price DECIMAL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

DELIMITER //
CREATE FUNCTION CalculateCartTotalForCustomer(customer_id_param INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_amount DECIMAL(10, 2);

    SELECT SUM(price) INTO total_amount
    FROM Cart
    WHERE customer_id = customer_id_param;

    RETURN COALESCE(total_amount, 0);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER before_delete_product_from_cart
BEFORE DELETE ON Cart
FOR EACH ROW
BEGIN
    DECLARE product_count INT;

    SELECT COUNT(*)
    INTO product_count
    FROM Cart
    WHERE customer_id = OLD.customer_id AND product_id = OLD.product_id;

    IF product_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete product. Product is not in the customer''s cart.';
    END IF;
END //
DELIMITER ;</code></pre>
                </div>
            </li>
        </ol>

        <h2>Usage</h2>
        <ol>
            <li>Run the Streamlit app:
                <div class="code-block">
                    <pre><code>streamlit run main.py</code></pre>
                </div>
            </li>
            <li>Navigate to the local server (usually <code>http://localhost:8501</code>) in your web browser.</li>
            <li>Use the interface to add, view, and delete products, and manage the shopping cart.</li>
        </ol>

        <h2>Project Structure</h2>
        <ul>
            <li><code>main.py</code>: The main Streamlit application file.</li>
            <li><code>product_operations.py</code>: Contains functions for product management.</li>
            <li><code>requirements.txt</code>: Lists the required Python packages.</li>
        </ul>

        <h2>Contributing</h2>
        <p>Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.</p>

        <h2>License</h2>
        <p>This project is licensed under the MIT License.</p>
    </div>
</body>
</html>
