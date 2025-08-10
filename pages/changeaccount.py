import streamlit as st
import sqlite3
import pandas as pd
import re
from passlib.hash import pbkdf2_sha256
from streamlit_extras.stylable_container import stylable_container
import time

conn = sqlite3.connect('user_credentials.db')
c = conn.cursor()
username = st.session_state.username if "username" in st.session_state else "User"

def delete_account():
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

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

if st.button("Go Back"):
    st.switch_page('pages/landing.py')

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

def change_account_details():
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
            margin-bottom: 5vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='centered'><h1>Change Account Details</h1></div>", unsafe_allow_html=True)


    user_df = pd.read_sql(f"select * from users where username='{st.session_state.username}'",conn)#.fetchall()
    # st.write(user_df['email'])
    email, firstname,lastname = user_df['email'][0],user_df['first_name'][0],user_df['last_name'][0]
    # st.write(email,firstname,lastname)

    df=pd.DataFrame(pd.read_sql('select * FROM users;', conn))
    tabs = st.radio("What would you like to update?   ", ["Username", "Email", "Password","Name"], horizontal=True)
    
    if tabs=='Username':
        new_username = st.text_input("Enter new Username:", key='signupusername')
        if st.button('Update'):
            if username_exists(conn, new_username):
                st.error("Username already exists. Please choose a different one.")
            elif new_username==username:
                st.error("New username cannot be the same as current username.")
            else:
                st.session_state.username = new_username
                st.write(st.session_state.username)
                c.execute(f"update users set username='{new_username}' where username='{username}'")
                conn.commit()
                st.success("Username successfully updated!")
            conn.close()

    elif tabs=='Email':
        new_email = st.text_input("Enter new email:")
        new_email2 = st.text_input("Confirm new email:")
        if st.button('Update Email'):
            if not validate_email(new_email):
                st.error("Invalid Email. Please enter a valid email address.")
            elif email==new_email:
                st.error("The email address is the same as the current email address. Please enter a new one.")
            elif new_email!=new_email2:
                st.error("The emails do not match. Please try again.")
            else:
                c.execute(f"update users set email='{new_email}' where username='{username}'")
                conn.commit()
                st.success("Email address successfully updated!")
            conn.close()

    elif tabs=='Password':
        curr_password = st.text_input("Enter Current Password:", type="password")
        new_password = st.text_input("Enter New Password:", type='password')
        new_password2 = st.text_input("Confirm New Password:", type='password')
        
        if st.button('Change Password'):
            if len(curr_password)>0:
                if curr_password != st.session_state.password:
                    st.error("Current password is incorrect. Please try again.")
                elif new_password == curr_password:
                    st.error("New password cannot be the same as the current password.")
                elif new_password!=new_password2:
                    st.error("The new passwords do not match. Please try again.")
                else:
                    password_hash = pbkdf2_sha256.hash(new_password)
                    c.execute(f"update users set password='{password_hash}' where username='{username}'")
                    conn.commit()
                    st.session_state.password=new_password
                    st.success("Password changed successfully!")
            conn.close()

    elif tabs=='Name':
        new_fn = st.text_input("Enter New First Name")
        new_ln = st.text_input("Enter New Last Name:")
        
        if st.button('Update'):
            if new_fn+new_ln==firstname+lastname:
                st.error("Your full name cannot be the same as the current one. Please change either first or last name.")
            else:
                c.execute(f"update users set first_name='{new_fn}' where username='{username}'")
                c.execute(f"update users set last_name='{new_ln}' where username='{username}'")
                conn.commit()
                st.success("Name successfully updated!")
            conn.close()
    st.write('<p><br><br><br><br><br></p>',unsafe_allow_html=True)

    with stylable_container(
            key="green_button",
            css_styles="""
                button {
                    border-radius: 3px;
                    height: 100px;
                    width: 400px;
                    font-size: 80px;
                    color: red;
                }
                """,
        ):
            if st.button("Delete Account"):
                delete_account()
                st.success("Account deleted successfully. Please wait...")
                conn.close()
                time.sleep(6)
                st.switch_page('main.py')
    
    # if st.button("Show DB"):
    #     st.write(df)

change_account_details()