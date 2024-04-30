from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
from io import BytesIO


def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

uploaded_file = st.file_uploader("Upload log file", type=['bin'], on_change=save_uploaded_file, args=(st.session_state.get('uploaded_file', None),))

if "uploaded_file" not in st.session_state and uploaded_file is not None:
    save_uploaded_file(uploaded_file)

if "uploaded_file" in st.session_state:
    file = st.session_state.uploaded_file
    # st.write("File uploaded successfully. File name:", file.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        shutil.copyfileobj(uploaded_file, tmp_file)
        tmp_file_path = tmp_file.name

    anonymize(tmp_file_path)
    log = load_log(tmp_file_path)

    st.write("Fluence Map")
    plt.figure()
    log.fluence.actual.calc_map()
    log.fluence.actual.plot_map()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    st.image(buf, caption='Fluence Map')
