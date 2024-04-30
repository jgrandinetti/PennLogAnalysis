import streamlit as st
from pylinac import load_log
from pylinac.log_analyzer import anonymize
import tempfile
import shutil
import matplotlib.pyplot as plt
from io import BytesIO

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Saving the original uploaded file in session_state
        st.session_state.uploaded_file = uploaded_file
        # Resetting the processed data to force reprocessing with a new file
        st.session_state.pop('anonymized_content', None)
        st.session_state.pop('fluence_image', None)

uploaded_file = st.file_uploader("Upload log file", type=['bin'], on_change=save_uploaded_file, args=(st.session_state.get('uploaded_file', None),))

if "uploaded_file" in st.session_state:
    if "anonymized_content" not in st.session_state or "fluence_image" not in st.session_state:
        file = st.session_state.uploaded_file

        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
            shutil.copyfileobj(uploaded_file, tmp_file)
            tmp_file_path = tmp_file.name

        anonymize(tmp_file_path)

        # Saving anonymized file content to session_state for persistence
        with open(tmp_file_path, "rb") as anonymized_file:
            st.session_state.anonymized_content = anonymized_file.read()

        log = load_log(tmp_file_path)
        log.fluence.actual.calc_map()

        buf = BytesIO()
        plt.figure()
        log.fluence.actual.plot_map()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Saving fluence map image data to session_state for persistence
        st.session_state.fluence_image = buf.getvalue()

    # Retrieving and displaying the fluence map image from session_state
    st.write("Fluence Map")
    fluence_image_data = st.session_state.fluence_image
    st.image(fluence_image_data, caption='Fluence Map')

    # Note: If you want to save and deal with the anonymized file beyond displaying the image,
    # you might need to store it differently depending on what you want to do with it.
