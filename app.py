import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Set webpage title
st.set_page_config(page_title="IGCEP Data Portal", layout="wide")

# 1. Initialize session state to keep track of login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 2. IF NOT LOGGED IN: Show the Login Screen
if not st.session_state["logged_in"]:
    st.title("🔒 Secure Data Portal Login")
    st.write("This database is restricted. Please enter the access password.")
    
    # Create the password input box (hides characters as you type)
    user_password = st.text_input("Enter Access Password:", type="password")
    login_button = st.button("Access Database")
    
    # CHANGE THIS to whatever password you want to give your classmates!
    CORRECT_PASSWORD = "Zahid56"
    
    if login_button:
        if user_password == CORRECT_PASSWORD:
            st.session_state["logged_in"] = True
            st.rerun() # Refresh the page to show the database
        else:
            st.error("❌ Incorrect password! Access Denied.")

# 3. IF LOGGED IN: Show the actual Search Engine
else:
    # Add a logout button in the sidebar
    if st.sidebar.button("Log Out 🔒"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("⚡ Power Generation Database Search Portal")
    st.write("Welcome! Search the data instantly below.")

    # Connect to your existing MySQL database
    engine = create_engine("mysql+pymysql://root:Zahid56@localhost:3306/power_db")

    # Create a search bar input box on the webpage
    search_query = st.text_input("🔍 Search by Plant Name, Fuel Type, or Zone:", "")

    # Pull data safely using parameters (SQL injection protection)
    if search_query:
        query = """
        SELECT * FROM data_generator 
        WHERE plant_name LIKE :search 
           OR fuel LIKE :search 
           OR zone LIKE :search
        """
        safe_search = f"%{search_query}%"
        df = pd.read_sql(text(query), con=engine, params={"search": safe_search})
        
        if not df.empty:
            st.success(f"Found {len(df)} matching records!")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No matching records found. Try searching something else!")
    else:
        df = pd.read_sql(text("SELECT * FROM data_generator"), con=engine)
        st.dataframe(df, use_container_width=True)