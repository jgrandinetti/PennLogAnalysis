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

    # Create a 2x2 grid of plots
    fig, axs = plt.subplots(2, 2)  # This creates a figure and a 2x2 array of axes
    fig.suptitle('Analysis Plots')

    # Plot 1 (Original fluence map plot)
    log.fluence.actual.calc_map()
    log.fluence.actual.plot_map(ax=axs[0, 0])
    axs[0, 0].set_title('Fluence Map')  # You can set individual titles for each subplot

    # Plot 2 (Placeholder for your 2nd function)
    # your_function_2(axs[0, 1])  # Replace with your actual function
    axs[0, 1].set_title('Your Plot 2 Title')

    # Plot 3 (Placeholder for your 3rd function)
    # your_function_3(axs[1, 0])  # Replace with your actual function
    axs[1, 0].set_title('Your Plot 3 Title')

    # Plot 4 (Placeholder for your 4th function)
    # your_function_4(axs[1, 1])  # Replace with your actual function
    axs[1, 1].set_title('Your Plot 4 Title')

    # Show the plots
    buf = BytesIO()
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the layout
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    st.image(buf, caption='2x2 Analysis Plots')
