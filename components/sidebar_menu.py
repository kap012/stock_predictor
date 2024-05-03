import streamlit as st

def sidebar_menu():
    with st.sidebar:
        st.page_link("./app.py", label="Main page", icon = "🏠")
        st.page_link("./pages/upload_data_page.py", label="📄 Load data")
        st.page_link("./pages/inspect_data_page.py", label="🔎 Data inspection")
        st.page_link("./pages/decompose_ts_page.py", label="Decompose timeseries", icon="📈")
        st.page_link("./pages/autocorrelation_page.py", label="Autocorrelation plots", icon="📈")
        st.page_link("./pages/persistence_forecast_page.py", label="Persistence forecast", icon="▶️")
        st.page_link("./pages/arima_page.py", label="ARIMA", icon="▶️")
        st.page_link("./pages/exponential_smoothing_page.py", label="Exponential Smoothing", icon="▶️")
        st.page_link("./pages/compare_models_page.py", label="🥼 Compare models")

        #st.page_link("./pages/experiment.py", label="experiment")

        image_links() 

def image_links():
    # email icon source: https://uxwing.com/envelope-line-icon/
    st.sidebar.markdown(
        
        
    """
    <div style="display: flex; justify-content: space-around;">
    <a href="https://github.com/kap012" target="_blank" style="text-decoration: none;">
            <img src="./app/static/github-mark-white.png" width="25" height="25">
    </a>
    <a href="https://www.linkedin.com/in/kacper-prywata-69b348228/" target="_blank" style="text-decoration: none;">
            <img src="./app/static/LinkedIn_logo.png" width="25" height="25">
    </a>
    <a href="mailto:prywata.kacper@gmail.com" >
            <img src="./app/static/email-logo2.png" width="30" height="25">
    </a>
    </div>
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



            

