import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import re

# UNCOMMENT FOR FINAL PUSH

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

import base64
def set_bg_hack(main_bg):
    main_bg_ext = "jpg"
        
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg_hack('backgrounds/pet_bg_alt.jpg')



def create_connection():
    conn = sqlite3.connect('user_credentials.db')
    return conn

def create_user(conn, first_name, last_name, email, username, password):
    password_hash = pbkdf2_sha256.hash(password)
    query = "INSERT INTO users (first_name, last_name, email, username, password) VALUES (?, ?, ?, ?, ?)"
    with conn:
        conn.execute(query, (first_name, last_name, email, username, password_hash))

def username_exists(conn, username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor = conn.execute(query, (username,))
    row = cursor.fetchone()
    return row is not None

def validate_email(email):
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False

def create_connection():
    conn = sqlite3.connect('user_credentials.db')
    return conn

def username_exists(conn, username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor = conn.execute(query, (username,))
    row = cursor.fetchone()
    return row is not None

def verify_password(saved_password, provided_password):
    return pbkdf2_sha256.verify(provided_password, saved_password)

def validate_username(username):
    pattern = r"^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def main():
    st.markdown(
        """
        <style>
        .centered {
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 10vh; 
            z-index: 1;
            margin-top: -10vh;
            margin-bottom:-10vh;
        }
        .subtext {
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 6vh;
            margin-top: -2vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='centered'><h1>Best Friends Furever</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'><h5>Where Tails Wag and Hearts Melt</h5></div>", unsafe_allow_html=True)

    tabs = st.radio("Choose your action:", ["Sign Up", "Login"], horizontal=True)

    if tabs == "Sign Up":
        st.markdown("#### Sign Up")
        conn = create_connection()

        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        new_username = st.text_input("Username", key='signupusername')
        new_password = st.text_input("Password", key='loginpw', type="password")

        if st.button("Sign Up"):
            if not validate_email(email):
                st.error("Invalid Email. Please enter a valid email address.")
            elif not validate_username(new_username):
                st.error("Invalid Username. Please use only letters and numbers.")
            elif username_exists(conn, new_username):
                st.error("Username already exists. Please choose a different one.")
            else:
                create_user(conn, first_name, last_name, email, new_username, new_password)
                st.success("Account created successfully! You can now log in.")

        conn.close()

    elif tabs == "Login":
        # login_page()
        st.markdown("#### Login")

        conn = create_connection()

        username = st.text_input("Username", key='loginusername')
        password = st.text_input("Password", key='loginpw', type="password")

        if st.button("Login"):
            query = "SELECT * FROM users WHERE username = ?"
            cursor = conn.execute(query, (username,))
            row = cursor.fetchone()

            if row is not None:
                password_index = cursor.description.index(('password', None, None, None, None, None, None))

                saved_password = row[password_index]
                if verify_password(saved_password, password):
                    st.success("Logged in as {}".format(username))
                    st.session_state['username']=username
                    st.session_state['password']=password
                    st.switch_page("pages/landing.py")
                else:
                    st.error("Invalid credentials. Please try again.")
            else:
                st.error("User not found. Please sign up or check your credentials and try again.")

            conn.close()


if __name__ == "__main__":
    main()
