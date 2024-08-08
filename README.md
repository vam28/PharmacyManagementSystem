# E-Commerce Platform

This is a simple e-commerce platform built using Streamlit and MySQL. It allows users to add, view, and delete products, and manage a shopping cart. The platform includes functionalities for administrators to manage products and categories, and for customers to view and add products to their cart.

For a full description of the module, visit the [project page](https://github.com/your-username/e-commerce-platform).

Submit bug reports and feature suggestions, or track changes in the [issue queue](https://github.com/your-username/e-commerce-platform/issues).

## Table of contents

- Requirements
- Installation
- Usage
- Project Structure
- Contributing
- License

## Requirements

This project requires the following:

- Python 3.6 or higher
- MySQL Server

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/e-commerce-platform.git
    cd e-commerce-platform
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up the MySQL database:

    ```sql
    CREATE DATABASE mydatabase;
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
    DELIMITER ;
    ```

## Usage

1. Run the Streamlit app:

    ```sh
    streamlit run main.py
    ```

2. Navigate to the local server (usually `http://localhost:8501`) in your web browser.
3. Use the interface to add, view, and delete products, and manage the shopping cart.

## Project Structure

- `main.py`: The main Streamlit application file.
- `product_operations.py`: Contains functions for product management.
- `requirements.txt`: Lists the required Python packages.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
