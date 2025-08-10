import streamlit as st
import os
#langchain
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.prompts.prompt import PromptTemplate

#streamlit-catalog
from streamlit_extras import grid
import pandas as pd
import numpy as np
import sqlite3
from streamlit_extras.stylable_container import stylable_container
from passlib.hash import pbkdf2_sha256
import base64

conn = sqlite3.connect('pets.db')
# <<<<<<< HEAD
# <<<<<<< HEAD
# # os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# =======
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# >>>>>>> 3b784fa93e97f829d2cc8efb4e15cb7bbb9a681a
# =======
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# >>>>>>> 3b784fa93e97f829d2cc8efb4e15cb7bbb9a681a

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

#user query

adopt_df = pd.DataFrame(pd.read_sql('select adoption_status FROM adoption_status ad inner join animal a using(animal_id);', conn))

def get_sql_query(query):

    #Prompt template
    _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct sqlite query to run, then look at the results of the query and return the answer.
        Use the following format:

        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"

        Only use the following tables:

        {table_info}

        Top K value: {top_k}

        For any query you generate, all columns from the animal table should be selected

        Also color can be something like 'BROWN/WHITE' in the animal table, so when I ask something like show me all brown coloured pets use LIKE %BROWN%
        Same for breed, use LIKE since there are records with breed as 'BOXER/MIX'
        For age, some records have format like '7 YEARS', some have format 'NO AGE', some have format like '3 MONTHS', so use conditional filtering accordingly to get the best query.
        For example a query related to age should be like this:
        SELECT * 
        FROM animal 
        WHERE 
        (CASE 
            WHEN pet_age LIKE '%YEARS' THEN CAST(SUBSTR(pet_age, 1, INSTR(pet_age, ' ') - 1) AS INTEGER) < 2
            WHEN pet_age LIKE '%MONTHS' THEN CAST(SUBSTR(pet_age, 1, INSTR(pet_age, ' ') - 1) AS INTEGER) < 24
            ELSE 0
        END) = 1;

        Question: {input}
        """

    PROMPT = PromptTemplate(
    input_variables=["input", "top_k", "table_info"], template=_DEFAULT_TEMPLATE)

    #langchain connection
    db = SQLDatabase.from_uri("sqlite:///pets.db")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature="0", api_key= os.getenv('OPENAI_API_KEY'))
    chain = create_sql_query_chain(llm, db, prompt = PROMPT)

    if query:
        response = chain.invoke(dict(question = query, top_k = 100, table_info=db.get_table_info(), dialect = db.dialect))
    else:
        response = 'SELECT * FROM animal'

    return response

def clean_name(input):
    cleaned = input.replace("* ","")
    cleaned = input.replace("*","")
    return cleaned.title()

if st.button("Go Back"):
    st.switch_page('pages/landing.py')

def pet_catalog():
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
            margin-top: -1vh;
            margin-bottom: 1vh;
        }
        .name{
        display:flex
        justify-content: center;
        align-items: center;
        width:100%;
        z-index: 1;
        font-weight: bold;
        }
        .text {
        display: flex;
        justify-content: left;
        align-items: left;
        width: 100%;
        }</text>
        </style>

        
        """,
        unsafe_allow_html=True
    )
    with stylable_container(
        key="container_with_border2",
        css_styles="""
            {
            }
            """,
    ):
        st.markdown("<div class='centered'><h1>Pet Catalog</h1></div>", unsafe_allow_html=True)

    query = st.text_input("What are you looking for?")

    adopt_df = pd.DataFrame(pd.read_sql('select adoption_status FROM adoption_status ad inner join animal a using(animal_id);', conn))
    pets = pd.DataFrame(pd.read_sql('select * FROM animal;', conn))
    # pets = pd.DataFrame(pd.read_sql(get_sql_query(query), conn))
    rows = np.array_split(pets,3)
    col1, col2, col3 = st.columns(3)
    
    for i in rows:
            for ind in i.index:
                if ind % 3 == 0:
                    with col1:
                        try:
                            with stylable_container(
                                key="container_with_border1",
                                css_styles="""
                                    {   
                                        border: 1px solid rgba(49, 51, 63, 0.2);
                                        border-radius: 5px;
                                        border-color: gray;
                                        width: 220px;
                                        background-color: black;
                                        padding-left: 2px;
                                        padding-right: 2px;
                                        padding-top: 2px;
                                        padding-bottom: 2px;
                                    }
                                    """,
                            ):
                                if pets['url_link'][ind] is not None:
                                    st.image(pets['url_link'][ind], width=200)
                                else:
                                    st.image(pets['image'][ind], width=200)
                                st.markdown(f"<div class=name> {clean_name(pets['pet_name'][ind])} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {pets['breed'][ind].title()} </div>", unsafe_allow_html=True)
                                if pets['pet_age'][ind].title().strip()=='No Age':
                                    st.markdown("<div class=text> Unknown Age </div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class=text> {pets['pet_age'][ind].title() + ' Old'} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {(pd.read_sql('select sex_desc from sex_type s inner join animal a where s.sex_id = a.sex and a.animal_id=' + str(pets['animal_id'][ind]), conn))['sex_desc'].iloc[0]} </div>", unsafe_allow_html=True)
                                st.write("")
                                if adopt_df['adoption_status'][ind]==1:
                                    st.write(":red[ALREADY ADOPTED]")
                                else:
                                    if st.button("View Details", key=ind):
                                        st.session_state['animal_id'] = pets['animal_id'][ind]
                                        st.switch_page("pages/pet_details.py")
                        except Exception as err:
                            st.write(f"Error on {pets['pet_name'][ind]} : {err}")
                            
                elif ind % 3 == 1:
                    with col2:
                        try:
                            with stylable_container(
                                key="container_with_border1",
                                css_styles="""
                                    {   
                                        border: 1px solid rgba(49, 51, 63, 0.2);
                                        border-radius: 5px;
                                        border-color: gray;
                                        width: 220px;
                                        background-color: black;
                                        padding-left: 2px;
                                        padding-right: 2px;
                                        padding-top: 2px;
                                        padding-bottom: 2px;
                                    }
                                    """,
                            ):
                                if pets['url_link'][ind] is not None:
                                    st.image(pets['url_link'][ind], width=200)
                                else:
                                    st.image(pets['image'][ind], width=200)
                                st.markdown(f"<div class=name> {clean_name(pets['pet_name'][ind])} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {pets['breed'][ind].title()} </div>", unsafe_allow_html=True)
                                if pets['pet_age'][ind].title().strip()=='No Age':
                                    st.markdown("<div class=text> Unknown Age </div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class=text> {pets['pet_age'][ind].title() + ' Old'} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {(pd.read_sql(f'select sex_desc from sex_type s inner join animal a where s.sex_id = a.sex and a.animal_id={pets['animal_id'][ind]};',conn))['sex_desc'][0]} </div>", unsafe_allow_html=True)
                                st.write("")
                                if adopt_df['adoption_status'][ind]==1:
                                    st.write(":red[ALREADY ADOPTED]")
                                else:
                                    if st.button("View Details",key=ind):
                                        st.session_state['animal_id'] = pets['animal_id'][ind]
                                        st.switch_page("pages/pet_details.py")
                        except Exception as err:
                            st.write(f'Error on {pets['pet_name'][ind]} : {err}')
                elif ind % 3 == 2:
                    with col3:
                        try:
                            with stylable_container(
                                key="container_with_border1",
                                css_styles="""
                                    {   
                                        border: 1px solid rgba(49, 51, 63, 0.2);
                                        border-radius: 5px;
                                        border-color: gray;
                                        width: 220px;
                                        background-color: black;
                                        padding-left: 10px;
                                        padding-right: 2px;
                                        padding-top: 10px;
                                        padding-bottom: 15px;
                                    }
                                    """,
                            ):
                                if pets['url_link'][ind] is not None:
                                    st.image(pets['url_link'][ind], width=200)
                                else:
                                    st.image(pets['image'][ind], width=200)
                                st.markdown(f"<div class=name> {clean_name(pets['pet_name'][ind])} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {pets['breed'][ind].title()} </div>", unsafe_allow_html=True)
                                if pets['pet_age'][ind].title().strip()=='No Age':
                                    st.markdown("<div class=text> Unknown Age </div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class=text> {pets['pet_age'][ind].title() + ' Old'} </div>", unsafe_allow_html=True)
                                st.markdown(f"<div class=text> {(pd.read_sql(f'select sex_desc from sex_type s inner join animal a where s.sex_id = a.sex and a.animal_id={pets['animal_id'][ind]};',conn))['sex_desc'][0]} </div>", unsafe_allow_html=True)
                                st.write("")
                                if adopt_df['adoption_status'][ind]==1:
                                    st.write(":red[ALREADY ADOPTED]")
                                else:
                                    if st.button("View Details",key=ind):
                                        st.session_state['animal_id'] = pets['animal_id'][ind]
                                        st.switch_page("pages/pet_details.py")
                        except Exception as err:
                            st.write(f'Error on {pets['pet_name'][ind]} : {err}')

    # for ind in pets.index:
    #     with st.container(border=True):
    #         st.write(pets['pet_name'][ind])
    #         st.image(pets['url_link'][ind], width=200)


    # with st.container():
    #     groups = np.array_split(pets,3)
    #     groups[0].insert(0,'group',pets)

pet_catalog()

