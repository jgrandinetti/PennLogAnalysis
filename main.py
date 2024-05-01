import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_extras.streaming_write import write
import sys
from st_pages import Page, Section, show_pages, add_page_title, add_indentation

favicon = """
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 32 40" enable-background="new 0 0 32 32" xml:space="preserve"><g display="none"><rect x="-195.323" y="-102.677" display="inline" fill="#000000" width="473.333" height="236"/></g><g display="none"><g display="inline"><polygon fill="#000000" points="0,7.582 11.51,0.972 23.019,7.582 23.019,20.804 11.51,27.415 0,20.804   "/><polygon points="21.677,31.028 32,13.189 11.355,13.189   "/></g></g><g display="none"><g display="inline"><polygon fill="#000000" points="17.505,22.819 11.51,26.262 1,20.225 1,8.161 11.51,2.125 22.019,8.161 22.019,13.689     23.019,13.689 23.019,7.582 11.51,0.972 0,7.582 0,20.804 11.51,27.415 18.005,23.684   "/><path fill="#000000" d="M30.266,14.189l-8.589,14.843l-8.589-14.843H30.266 M32,13.189H11.355l10.323,17.839L32,13.189L32,13.189z    "/></g></g><g display="none"><g display="inline"><circle fill="#000000" cx="16" cy="16" r="16"/></g><g display="inline"><polygon fill="#000000" points="12.615,13.761 30.948,13.761 21.586,29.601   "/></g><g display="inline"><polygon fill="#000000" points="0,7.865 11.573,1.552 22.448,7.927 22.448,13.677 12.323,13.802 17.76,23.365 11.385,26.615     0,20.552   "/></g><g display="inline"><polygon points="17.505,22.819 11.51,26.262 1,20.225 1,8.161 11.51,2.125 22.019,8.161 22.019,13.689 23.019,13.689     23.019,7.582 11.51,0.972 0,7.582 0,20.804 11.51,27.415 18.005,23.684   "/></g><g display="inline"><path d="M30.266,14.189l-8.589,14.843l-8.589-14.843H30.266 M32,13.189H11.355l10.323,17.839L32,13.189L32,13.189z"/></g></g><g><g><path d="M17.572,23.933l4.106,7.095L32,13.189h-8.981V7.582L11.51,0.972L0,7.582v13.222l11.51,6.611L17.572,23.933z     M28.532,15.189l-6.855,11.846l-6.855-11.846H28.532z"/></g></g></svg>    """

# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="collapsed")
st.set_page_config(
    page_title="Penn Log Analysis",
    page_icon = favicon,
    initial_sidebar_state="collapsed",
)

with open('style.css', 'r') as f:
    css_to_apply = f.read()

add_indentation()
show_pages(
    [
        Page("main.py", "Home"),
        Page("pages/log_analysis.py", "Log Analysis"),
    ]
)



st.markdown("""
    <h1 style='text-align: center;'>Penn Log File Dashboard</h1>
    """, unsafe_allow_html=True)
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
