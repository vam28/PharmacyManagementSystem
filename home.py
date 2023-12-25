import streamlit as st

def display_all_products(db, cursor):
    st.header("All Products")
    # Perform a join operation to get product details with category information
    cursor.execute("SELECT Product.product_id, Product.name AS product_name, Product.price, "
                   "Category.name AS category_name "
                   "FROM Product "
                   "INNER JOIN Category ON Product.category_id = Category.category_id;")

    products = cursor.fetchall()

    # Display products vertically
    for product in products:
        product_id, product_name, price, category_name = product
        st.write(f"ID: {product_id}")
        st.write(f"Name: {product_name}")
        st.write(f"Price: {price}")
        st.write(f"Category: {category_name}")
        st.markdown("---")  # Add a horizontal line between products for better visibility

def add_to_cart(db, cursor, product_name):
    try:
        # Get the product details
        cursor.execute("SELECT product_id, price FROM Product WHERE name = %s", (product_name,))
        product_details = cursor.fetchone()

        if product_details:
            product_id, price = product_details
            # Insert the selected product into the Cart table
            cursor.execute("INSERT INTO Cart (customer_id, product_id, price) VALUES (%s, %s, %s)",
                           (st.session_state.customer_id, product_id, price))
            db.commit()
            st.success(f"{product_name} added to the cart successfully!")
        else:
            st.error("Invalid product selection.")

    except Exception as e:
        st.error(f"Error occurred: {e}")

def calculate_cart_total_for_customer(db, cursor, customer_id):
    try:
        # Call the SQL function to calculate the total amount
        cursor.execute("SELECT CalculateCartTotalForCustomer(%s)", (customer_id,))
        total_amount = cursor.fetchone()[0]

        return total_amount

    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

def delete_from_cart(db, cursor, product_name):
    try:
        # Get the product ID from the Product table
        cursor.execute("SELECT product_id FROM Product WHERE name = %s", (product_name,))
        product_id_result = cursor.fetchone()

        if product_id_result:
            product_id = product_id_result[0]

            # Check if the product is in the customer's cart before deletion
            cursor.execute("SELECT COUNT(*) FROM Cart WHERE customer_id = %s AND product_id = %s",
                           (st.session_state.customer_id, product_id))
            product_count = cursor.fetchone()[0]

            if product_count > 0:
                # Delete the selected product from the Cart table
                cursor.execute("DELETE FROM Cart WHERE customer_id = %s AND product_id = %s",
                               (st.session_state.customer_id, product_id))
                db.commit()
                st.success(f"{product_name} removed from the cart successfully!")
            else:
                st.error("Cannot delete product. Product is not in the customer's cart.")
        else:
            st.error("Invalid product selection.")

    except Exception as e:
        st.error(f"Error occurred: {e}")
   
