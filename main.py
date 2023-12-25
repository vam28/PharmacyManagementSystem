# main.py
import streamlit as st
import mysql.connector
from manage_stock import *
from home import *

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8088",
    database="sepro"
)
cursor = db.cursor()

# Function to check if admin is logged in
def is_admin_logged_in():
    return st.session_state.is_admin_logged_in if 'is_admin_logged_in' in st.session_state else False

# Function to check if customer is logged in
def is_customer_logged_in():
    return st.session_state.is_customer_logged_in if 'is_customer_logged_in' in st.session_state else False

# Function to handle user registration
def register():
    st.header("User Registration")
    user_type = st.radio("Select user type:", ["Customer", "Admin"])
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Register"):
        if user_type == "Customer":
            cursor.execute("INSERT INTO Customer (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        elif user_type == "Admin":
            cursor.execute("INSERT INTO Admin (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        
        db.commit()
        st.success("Registration successful!")

# Function to handle user login
def login():
    st.header("User Login")
    user_type = st.radio("Select user type:", ["Customer", "Admin"])
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        if user_type == "Customer":
            cursor.execute("SELECT customer_id FROM Customer WHERE email = %s AND password = %s", (email, password))
            customer_id = cursor.fetchone()
            if customer_id:
                st.session_state.is_customer_logged_in = True  # Set customer login status in session state
                st.session_state.customer_id = customer_id[0]  # Save customer ID in session state
                st.success("Login successful!")
                st.write(f"Customer ID: {customer_id[0]}")  # Display customer ID on the screen
            else:
                st.error("Invalid email or password")
        elif user_type == "Admin":
            cursor.execute("SELECT admin_id FROM Admin WHERE email = %s AND password = %s", (email, password))
            admin_id = cursor.fetchone()
            if admin_id:
                st.session_state.is_admin_logged_in = True  # Set admin login status in session state
                st.success("Admin login successful!")
            else:
                st.error("Invalid email or password")

def main():
    page = st.sidebar.radio("Select a page:", ["Registration", "Login", "Home", "Manage Stock"])

    # Define variables for login
    email = ""
    password = ""

    if page == "Registration":
        register()

    elif page == "Login":
        login()

        if is_admin_logged_in():
            st.warning("Only admins can view this page. Please select 'Admin Stock Page' from the sidebar.")

        elif is_customer_logged_in():
            # No need to call get_customer_id since the customer_id is saved in session state
            st.success("Redirecting to Home...")

    elif page == "Home":
        # Check if the customer is logged in before showing the "Home" page
        if not is_customer_logged_in():
            st.warning("Please log in as a customer to access the 'Home' page.")

        else:
            # Customer ID is already saved in session state in the login function
            customer_id = st.session_state.customer_id
            st.success("Welcome to the Home page!")

            # Display all products
            display_all_products(db, cursor)

            # Section to add products to the cart
            st.header("Add Products to Cart")
            product_name_to_add = st.text_input("Enter product name to add to the cart:")
            if st.button("Add Product to Cart"):
                add_to_cart(db, cursor , product_name_to_add)

            # Section to show total amount in the cart on the frontend
            st.header("Cart Summary")
            total_amount = calculate_cart_total_for_customer(db, cursor, customer_id)

            if total_amount is not None:
                st.success(f"Total amount in the cart: Rs.{total_amount}")
            else:
                st.warning("Unable to retrieve total amount.")

            # Section to delete products from the cart
            st.header("Delete Products from Cart")
            product_name_to_delete = st.text_input("Enter product name to delete from the cart:")
            if st.button("Delete Product from Cart"):
                delete_from_cart(db, cursor , product_name_to_delete)

    elif page == "Manage Stock":
        # Check if admin is logged in before showing the stock page
        if is_admin_logged_in():
            add_product(db, cursor)
            view_product(db, cursor)
            delete_product(db, cursor)

        else:
            st.warning("Only admins can view this page. Please log in as an admin.")

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()



