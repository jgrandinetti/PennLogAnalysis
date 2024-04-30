from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
from io import BytesIO


# Function to handle file upload; this function will be called only when the file is uploaded.
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file into the session_state
        st.session_state.uploaded_file = uploaded_file

# Create a file uploader widget
uploaded_file = st.file_uploader("Upload log file", type=['bin'], on_change=save_uploaded_file, args=(st.session_state.get('uploaded_file', None),))

# Using the 'uploaded_file' directly for first-time upload.
# For subsequent accesses or page reruns, the file doesn't need to be re-uploaded and can be accessed from 'st.session_state'.
if "uploaded_file" not in st.session_state and uploaded_file is not None:
    save_uploaded_file(uploaded_file)

if "uploaded_file" in st.session_state:
    file = st.session_state.uploaded_file
    # st.write("File uploaded successfully. File name:", file.name)

    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        shutil.copyfileobj(uploaded_file, tmp_file)
        tmp_file_path = tmp_file.name  # Store the temporary file path

    # After saving the file to a temporary location, anonymize it before processing
    anonymize(tmp_file_path)  # Anonymize the log file at the temp path

    log = load_log(tmp_file_path)  # Now load the anonymized log file
    log.fluence.actual.calc_map()

    plt.figure()  # Creates a new figure
    log.fluence.actual.plot_map()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Display the plot
    st.image(buf, caption='Fluence Map')
