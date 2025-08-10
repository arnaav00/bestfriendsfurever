import streamlit as st
import sqlite3
from datetime import date
from streamlit_extras.stylable_container import stylable_container
import time
import pandas as pd
conn = sqlite3.connect('pets.db')
c = conn.cursor()

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

def newpet():
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
            margin-top: 5vh;
            margin-bottom: 5vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='centered'><h1>Enter Pet Details</h1></div>", unsafe_allow_html=True)

    pet_age = ''
    animal_name = st.text_input("Pet Name:")
    animal_type = st.selectbox("Pet Type:", [animal[0] for animal in c.execute("SELECT DISTINCT animal_type from animal;").fetchall()])
    intake_types_query = c.execute('SELECT intake_type_desc FROM intake;').fetchall()
    intake_types = []
    for i in range(5):
        intake_types.append(intake_types_query[i][0])
    intake_type = st.selectbox("Intake Type:", intake_types)
    intake_type = [i for i in c.execute(f"SELECT intake_type_id from intake where intake_type_desc='{intake_type}'").fetchall()[0]][0]
    st.write("Pet Age: ")
    col1, col2 = st.columns(2)
    with col1:
        pet_age_years = st.number_input("Years", min_value=0, step=1,key="pet_years")
    with col2:
        pet_age_months = st.number_input("Months", min_value=0, max_value=11, step=1,key="pet_months")
    pet_age = str(pet_age_years) + " YEARS " + str(pet_age_months) + ' MONTHS' if pet_age_months!=0 else str(pet_age_years) + " YEARS"
    
    pet_size = st.radio("Pet Size:", ['Small', 'Medium', 'Large'], horizontal=True)
    pet_size = 'S' if pet_size == 'Small' else 'M' if pet_size=='Medium' else 'L'

    color = st.text_input("Color:")
    breed = st.text_input("Breed:")
    sex_query = c.execute('SELECT sex_desc FROM sex_type;').fetchall()
    sexes = []
    for i in range(5):
        sexes.append(sex_query[i][0])
    sex = st.selectbox("Sex:", sexes)
    sex = [i for i in c.execute(f"SELECT sex_id from sex_type where sex_desc='{sex}'").fetchall()[0]][0]

    crossing = st.text_input("Address Found (Leave blank if not stray):")   #, "" if intake_type != 'Stray' else None)
    image = st.file_uploader("Upload Image:")
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 , col4, col5 = st.columns(5)
    submission_completed = False 

    with col1:
        pass
    with col3:
        pass
    with col4:
        pass
    with col5:
        pass
    with col2:
        with stylable_container(
            key="green_button",
            css_styles="""
                button {
                    border-radius: 3px;
                    height: 100px;
                    width: 400px;
                    font-size: 80px;
                }
                """,
        ):
            if st.button("Submit"):
                c.execute("INSERT INTO animal (animal_type, pet_name, intake_type, in_date, pet_age, pet_size, color, breed, sex, crossing, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                        (animal_type, animal_name, intake_type, date.today().strftime("%m/%d/%y"), pet_age, pet_size, color, breed, sex, crossing, image.read()))
                conn.commit()

                submission_completed=True
                # st.write("Submitted!")
        with stylable_container(
            key="red_button",
            css_styles="""
                button {
                    border-radius: 3px;
                    height: 100px;
                    width: 400px;
                    font-size: 80px;
                }
                """,
        ):
            if not submission_completed:
                if st.button("Go Back"):
                    st.switch_page('pages/landing.py')
    if submission_completed:
        st.success(f'{animal_name} is in good hands now! Please wait...')
        adopt_query = c.execute(f"SELECT animal_id FROM animal where pet_name='{animal_name}';").fetchall()
        new_animal_id = adopt_query[0][0]
        c.execute(f"insert into adoption_status (animal_id, adoption_status) VALUES (?,?);",(new_animal_id,0))
        conn.commit()
        time.sleep(7)
        st.switch_page('pages/landing.py')
newpet()