import streamlit as st
import sqlite3
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime
conn = sqlite3.connect('pets.db')
c = conn.cursor()
animal_id = st.session_state['animal_id']
# from streamlit_modal import Modal
# import streamlit.components.v1 as components
import time

def clean_name(input):
    cleaned = input.replace("* ","")
    cleaned = input.replace("*","")
    return cleaned.title()

pet_name = pd.read_sql(f'select pet_name from animal where animal_id={animal_id}',conn)
df = pd.read_sql(f'select * FROM animal where animal_id = {animal_id};', conn)
df_intake = pd.read_sql(f'select intake_type_desc from intake i inner join animal a where a.intake_type=i.intake_type_id and a.animal_id={animal_id};',conn)
df_petsize = pd.read_sql(f'select pet_size_desc from pet_size p inner join animal a where p.pet_size_id=a.pet_size and a.animal_id={animal_id};',conn)  
df_petsize['pet_size_desc'][0] += 'IUM' if df_petsize['pet_size_desc'][0]=='MED' else ''
df_sex = pd.read_sql(f'select sex_desc from sex_type s inner join animal a where s.sex_id = a.sex and a.animal_id={animal_id};',conn)
if df['crossing'][0] is not None:
    crossing = "Address Found:   " + df['crossing'][0]
# elif len(df['crossing'][0])>1:
#     crossing = ""
else: crossing = ""

# crossing = "Address Found:   " + df['crossing'][0] if len(df['crossing'][0])>1 else ""
df_adopt = pd.read_sql(f'select * FROM adoption_status where animal_id = {animal_id};', conn)
pet_name = clean_name(pet_name['pet_name'][0])
date_string = df['in_date'][0]
date_obj=None
# try:
#     date_obj = datetime.strptime(date_string, "%m/%d/%y")
# except ValueError:
#     try:
#         date_obj = datetime.strptime(date_string, "%m/%d/%Y")
#     except ValueError:
#         print("Invalid date format")
# formatted_date = date_obj.strftime("%d %B %Y")


# modal = Modal(
#     f"Thank you for finding {pet_name} a new home!", 
#     key="demo-modal",
#     padding=20,    # default value
#     max_width=744     # default value
# )
# # modal.close()

# if modal.is_open():
#     with modal.container():
#         if st.button("Go back to catalog"):
#             st.switch_page('pages/catalog.py')

def details():
    adoption_completed = False
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
            text-align: center;
            height: 10vh; 
            z-index: 1;
            margin-top: -1vh;
            margin-bottom: 1vh;
        }
        .text1 {
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 10vh; 
            z-index: 1;
            margin-top:15vh;
            margin-bottom:20vh;
        }
        .text2 {
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 10vh; 
            z-index: 1;
            margin-top:15vh;
            margin-bottom:20vh;
        }
        </style>
        """,
        unsafe_allow_html=True
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


    with stylable_container(
        key="container_with_border1",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background-color: black;
            }
            """,
    ):
        st.markdown(f"<div class='centered'><h1>{pet_name}</h1></div>", unsafe_allow_html=True)


    with stylable_container(
        key="container_with_border2",
        css_styles="""
            {
                display: flex;
                justify-content: center;
                align-items: center;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                background-color: black;
            }
            """,
    ):
        if df['url_link'][0] is not None:
            st.image(df['url_link'][0], use_column_width=True)
        else:
            st.image(df['image'][0], use_column_width=True)
        st.markdown(f"<div class='text1'><h3> Type:&nbsp;&nbsp;&nbsp;{df['animal_type'][0].title()}\
                    <br>Intake Date:&nbsp;&nbsp;{date_string}\
                    <br>Intake Type:&nbsp;&nbsp;{df_intake['intake_type_desc'][0].upper().title()}\
                    <br>Breed:&nbsp;&nbsp;{df['breed'][0].title()}\
                    <br>Age:&nbsp;&nbsp;{df['pet_age'][0].title()}\
                    <br>Color:&nbsp;&nbsp;{df['color'][0].title()}\
                    <br>Pet Size:&nbsp;&nbsp;{df_petsize['pet_size_desc'][0].title()}\
                    <br>Sex:&nbsp;&nbsp;{df_sex['sex_desc'][0].title()}\
                    <br>{crossing}</h3></div>", unsafe_allow_html=True)
    # st.write(df)
    # st.write(df_adopt)
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col3:
        pass
    with col4:
        pass
    with col5:
        pass
    with col2:
        # pass
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
            if st.button("Adopt"):
                c.execute(f"UPDATE adoption_status SET adoption_status = 1 WHERE animal_id = {animal_id};")
                conn.commit()
                adoption_completed = True
                # modal.open()
                # conn.close()

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

            if not adoption_completed:
                if st.button("Cancel"):
                    st.switch_page('pages/catalog.py')

    if adoption_completed:
        st.success(f"Thank you for finding {pet_name} a lovely new home! You will now be redirected back to the pet catalog...")
        # st.markdown(f'<p style="font-family: sans-serif; color: green; font-size: 20px; font-weight: 900; text-align: center;">\
        #             Thank you for finding {pet_name} a new home!</p>', unsafe_allow_html=True)
        # st.markdown(f'<p style="font-family: sans-serif; color: black; font-size: 20px; font-weight: 900; text-align: center;">\
        #     You will now be redirected back to the catalog...</p>', unsafe_allow_html=True)
        time.sleep(6)
        st.switch_page('pages/catalog.py')
        


details()