-- Create Customer table
USE mydatabase;

-- Create Admin table
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

-- Create Category table
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

-- Create ProductCategory table
CREATE TABLE IF NOT EXISTS ProductCategory (
    category_id INT,
    product_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Create CartProduct table
CREATE TABLE IF NOT EXISTS Cart (
    customer_id INT,
    product_id INT,
	price DECIMAL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Create a function to calculate the total amount in the cart for a specific customer
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


-- Create a trigger to check if the product is in the customer's cart before deletion
DELIMITER //

CREATE TRIGGER before_delete_product_from_cart
BEFORE DELETE ON Cart
FOR EACH ROW
BEGIN
    DECLARE product_count INT;

    -- Check if the product is in the customer's cart
    SELECT COUNT(*)
    INTO product_count
    FROM Cart
    WHERE customer_id = OLD.customer_id AND product_id = OLD.product_id;

    -- If the product is not in the cart, prevent deletion
    IF product_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete product. Product is not in the customer''s cart.';
    END IF;
END //

DELIMITER ;











-- Create Order table
-- Note: "Order" is a reserved keyword, consider using a different name for the table
-- CREATE TABLE IF NOT EXISTS Orders (
--     order_id INT PRIMARY KEY,
--     customer_id INT,
--     order_date DATE NOT NULL,
--     order_time TIME NOT NULL,
--     total_amt DECIMAL(10,2),
--     FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
-- );

-- Create Payment table
-- CREATE TABLE IF NOT EXISTS Payment (
--     payment_id INT PRIMARY KEY,
--     order_id INT,
--     customer_id INT, -- Assuming this is the foreign key for the customer
--     FOREIGN KEY (order_id) REFERENCES Orders(order_id)
-- );
-- Create Manage table
-- CREATE TABLE IF NOT EXISTS Manage (
--     admin_id INT,
--     product_id INT,
--     category_id INT,
--     FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
--     FOREIGN KEY (product_id) REFERENCES Product(product_id),
--     FOREIGN KEY (category_id) REFERENCES Category(category_id)
-- );
