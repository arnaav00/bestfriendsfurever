import streamlit as st

def landing():
    st.markdown(
        """
        <style>
        .text1 {
            top: 50;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 10vh; 
            z-index: 1;
            margin-top:10vh;
            text-shadow: 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black;
        }
        .text2 {
            top: 70;
            left: 0;
            bottom: 100
            width: 100%;
            display: flex;
            text-align: center;
            font-size: 24px;
            margin-top: 10vh;
            justify-content: center;
            align-items: center;
            z-index: 1;
            text-shadow: 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
<style>
button {
    margin: 10px;
    font-size: 40px;
    font-weight: 500;
    color: #fff;
    cursor: pointer;
    border-radius: 3px;
    padding: 16px 18px 15px;
    white-space: nowrap;
    outline: none;
    border: none;
    display: inline-block;
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
    set_bg_hack('backgrounds/pet_bg.jpg')
    
    st.markdown("<div class='text2'>    </div>",unsafe_allow_html=True)
    st.markdown(f'<p style="font-family: Tahoma, sans-serif; color: black; font-size: 50px; font-weight: 900; text-align: center; margin-left:-7vh;">\
                    <br>Welcome Back, {st.session_state.username if "username" in st.session_state else "User"}!</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-family: Tahoma, sans-serif; color: black; font-size: 20px; font-weight: 900; text-align: center; margin-left:-7vh;">\
        What would you like to do today?</p>', unsafe_allow_html=True)
    st.markdown("<div class='text2'>    </div>",unsafe_allow_html=True)
    col1, col2, col3 , col4, col5, col6,col7,col8,col9,col10 = st.columns(10)

    with col1:
        pass
    with col2:
        if st.button("Take a peek at the catalog"):
            st.switch_page("pages/catalog.py")
        # pass
    with col3:
        pass
    with col5:
        pass
    with col6:
        if st.button("Put up a pet for adoption"):
            st.switch_page("pages/submitnewpet.py")
        # pass
    with col7:
        pass
    with col8:
        pass
    with col9:
        pass
    with col10:
        pass
    with col4 :
        st.markdown("<div class='text2'>    </div>",unsafe_allow_html=True)
        if st.button("Change account details"):
            st.switch_page("pages/changeaccount.py")
        if st.button("Log out of your account"):
            st.switch_page("main.py")

landing()
