import streamlit as st
from .markdown import hyperlinked_img_to_html

def sidebar_menu():
    with st.sidebar:
        st.page_link("./app.py", label="Main page", icon = "🏠")
        st.page_link("./pages/stock.py", label="See stocks", icon="📈")
        st.page_link("./pages/file_upload.py", label="📄 Load data")
        st.page_link("./pages/inspect.py", label="🔎 Data inspection")
        st.page_link("./pages/compare.py", label="🥼 Compare models")

        image_links()  



def image_links():
    with st.sidebar:
        #c, col1, _ = st.columns(spec = [2, 1, 2], gap="large")
        _ , col1, _ = st.columns(3)
    
        with col1:
            st.sidebar.markdown(
            """
            <a href="https://twitter.com/cameronjoejones" target="_blank" style="text-decoration: none;">
                <div style="display: flex; align-items: center;">
                    <img src="./app/static/github-mark-white.png" width="25" height="25">
                </div>
            </a>
            """, unsafe_allow_html=True
            )

def icon_links():
     with st.sidebar:
        _, col1, col2 = st.columns(spec = [1, 1.5, 2], gap="small")

        with col1: 
            st.write("[:chart_with_upwards_trend:](google.com)")

        with col2:
            st.write("""<a href='https://google.com' id='Image 1'>
                    <img width='20%' src='https://img.icons8.com/ios-filled/50/FFFFFF/github.png'>
                    </a>"""
                    , 
            unsafe_allow_html=True)



            

