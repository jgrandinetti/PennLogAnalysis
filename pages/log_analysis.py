from pylinac import load_log
import streamlit as st

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
    # This means the file is already uploaded and is stored in session_state
    # You can now read the file or process it as required
    log = st.session_state.uploaded_file
    st.write("File uploaded successfully. File name:", log.name)
    st.write(log)
    # log.fluence.actual.calc_map()
    # log.fluence.actual.plot_map()
