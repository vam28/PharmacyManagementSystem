   # product_operations.py
import streamlit as st
import mysql.connector

def add_product(db, cursor):
    st.header("Add Product")
    product_name = st.text_input("Enter product name:")
    price = st.number_input("Enter product price:")
    category_name = st.text_input("Enter product category:")
    
    if st.button("Add Product"):
        try:
            # Check if the category exists
            cursor.execute("SELECT * FROM Category WHERE name = %s", (category_name,))
            category = cursor.fetchone()

            if not category:
                # If the category does not exist, create it
                cursor.execute("INSERT INTO Category (name) VALUES (%s)", (category_name,))
                db.commit()
                st.success("Category added successfully!")

            # Get the category_id
            cursor.execute("SELECT category_id FROM Category WHERE name = %s", (category_name,))
            category_id = cursor.fetchone()[0]

            # Check if the product already exists in the category
            cursor.execute("SELECT * FROM Product WHERE name = %s AND category_id = %s", (product_name, category_id))
            existing_product = cursor.fetchone()

            if existing_product:
                st.error("Product with the same name already exists in this category. Choose a different name.")
            else:
                # Add the product
                cursor.execute("INSERT INTO Product (name, price, category_id) VALUES (%s, %s, %s)",
                               (product_name, price, category_id))
                db.commit()
                st.success("Product added successfully!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def view_product(db, cursor):
    st.header("View Product")
    
    # Perform a join operation to get product details with category information
    cursor.execute("SELECT Product.product_id, Product.name AS product_name, Product.price, "
                   "Category.category_id, Category.name AS category_name "
                   "FROM Product "
                   "INNER JOIN Category ON Product.category_id = Category.category_id;")
    
    products = cursor.fetchall()

    # Display products in a table
    st.subheader("Product Information:")
    st.table(products)

def delete_product(db, cursor):
    st.header("Delete Product")
    product_id = st.number_input("Enter product ID to delete:", step=1, value=1)
    
    if st.button("Delete Product"):
        # Check if the product_id exists
        cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
        existing_product = cursor.fetchone()

        if existing_product:
            # Get the category_id of the product
            category_id = existing_product[3]  # Assuming the category_id is at index 3, adjust if needed

            # Delete the product from the Product table
            cursor.execute("DELETE FROM Product WHERE product_id = %s", (product_id,))
            db.commit()
            st.success("Product deleted successfully!")

            # Check if the category is unique (not associated with any other product)
            cursor.execute("SELECT COUNT(*) FROM Product WHERE category_id = %s", (category_id,))
            product_count = cursor.fetchone()[0]

            if product_count == 0:
                # If the category is unique, delete it from the Category table
                cursor.execute("DELETE FROM Category WHERE category_id = %s", (category_id,))
                db.commit()
                st.success("Category deleted successfully!")
        else:
            st.error("Product not found.")



# def calculate_cart_total_for_customer(db, cursor, customer_id):
#     try:
#         # Call the SQL function to calculate the total amount
#         cursor.execute("SELECT CalculateCartTotalForCustomer(%s)", (customer_id,))
#         total_amount = cursor.fetchone()[0]

#         return total_amount

#     except Exception as e:
#         st.error(f"Error occurred: {e}")
#         return None
    


    