from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.express as px
import numpy as np

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

def load_log_file():
    if "uploaded_file" in st.session_state:
        file = st.session_state.uploaded_file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp_file:
            shutil.copyfileobj(file, tmp_file)
            tmp_file_path = tmp_file.name

        anonymize(tmp_file_path)
        log = load_log(tmp_file_path)
        st.session_state.log = log

def plot_fluence_map():
    if "log" in st.session_state:
        log = st.session_state.log
        fluence_array = log.fluence.actual.calc_map()
        
        # Calculate the aspect ratio of the fluence array
        aspect_ratio = fluence_array.shape[1] / fluence_array.shape[0]
        
        # Create a figure with equal aspect ratio
        fig = plt.figure(figsize=(8, 8 / aspect_ratio))
        ax = fig.add_subplot(111)
        
        # Plot the fluence array using imshow
        im = ax.imshow(fluence_array, cmap='viridis', aspect='equal')
        
        # Add a colorbar
        plt.colorbar(im)
        
        # Remove the axes ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Convert the plot to PNG format
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        # Display the plot using Streamlit
        st.image(buf, use_column_width=True)

def plot_mu_calc():
    if "log" in st.session_state:
        log = st.session_state.log

        plt.figure()
        log.axis_data.mu.plot_actual()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        st.session_state.mu_calc = buf

uploaded_file = st.file_uploader("Upload log file", type=['bin'], on_change=save_uploaded_file, args=(st.session_state.get('uploaded_file', None),))

if "uploaded_file" not in st.session_state and uploaded_file is not None:
    save_uploaded_file(uploaded_file)

if "log" not in st.session_state:
    load_log_file()

# Fluence
if "log" in st.session_state:
    plot_fluence_map()

# MU Plot
if "mu_calc" not in st.session_state:
    plot_mu_calc()
if "mu_calc" in st.session_state:
    st.image(st.session_state.mu_calc, caption='MU Actual')
