import streamlit as st
from .markdown import hyperlinked_img_to_html

def sidebar_menu():
    # st.sidebar.page_link("./app.py", label="Main page", icon = "👈")
    # st.sidebar.page_link("./pages/stock_price_graph.py", label="Stock Price Graph")
    # st.sidebar.page_link("./pages/plotting_demo.py", label="Plotting Demo")
    # st.sidebar.page_link("./pages/write_stream.py", label="Write Stream Demo")
    # st.sidebar.success("Select a demo above.")


    with st.sidebar:

        st.page_link("./app.py", label="Main page", icon = "🏠")

      
        st.page_link("./pages/stock.py", label="Stocks", icon="📈")
        st.page_link("./pages/file_upload.py", label="📄 File Upload")
        st.page_link("./pages/experiment.py", label="Experiment")
        st.page_link("./pages/compare.py", label="Compare")

        
        with st.spinner("Loading..."):
            st.success("Done!")

        image_links()  



def image_links():
    with st.sidebar:
        #c, col1, _ = st.columns(spec = [2, 1, 2], gap="large")
        c , col1, d = st.columns(3)
        with c:
            st.write(123)
            pass

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

        with d:
            st.write(00)

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



            

