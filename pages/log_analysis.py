from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.express as px
import numpy as np
from streamlit_echarts import st_echarts


def plot_heatmaps_to_buffer(calculated_fluence, expected_fluence, gamma):
    # Calculate the aspect ratio based on the data dimensions
    data = [calculated_fluence, expected_fluence, gamma]
    nrows, ncols = data[0].shape  # Assuming all data arrays have the same shape

    # Create a figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Titles for each subplot
    titles = ['Measured Fluence', 'Expected Fluence', 'Gamma 3%/3mm']

    for ax, d, title in zip(axes, data, titles):
        # Display the heatmap
        im = ax.imshow(d, cmap='jet', interpolation='nearest', aspect='equal')

        # Set the aspect of the plot to be equal
        ax.set_aspect(aspect=(ncols / nrows))

        # Set title and add colorbar
        ax.set_title(title)
        fig.colorbar(im, ax=ax)

    # Adjust layout
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    return buf



def mu_calc_plot(mu, gantry):
    mu_list = mu.tolist()
    gantry_list = gantry.tolist()
    x_labels = list(range(1, len(mu_list) + 1))

    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'line'  # Shows a vertical line across the chart when hovering
            }
        },
        "xAxis": {
            "type": "category",
            "data": x_labels,
        },
        "yAxis": [
            {
                "type": "value",
                "name": "MU",
                "nameLocation": "middle",
                "nameGap": 50
            },
            {
                "type": "value",
                "name": "Gantry Angle",
                "nameLocation": "middle",
                "nameGap": 50,
                "position": "right"
            }
        ],
        "series": [
            {
                "data": mu_list,
                "type": "line",
                "areaStyle": {},
                "name": "MU",
                "color": "#3498db"
            },
            {
                "data": gantry_list,
                "type": "line",
                "yAxisIndex": 1,
                "name": "Gantry Angle",
                "color": "#e74c3c"
            }
        ],
        "legend": {
            "data": ["MU", "Gantry Angle"]
        }
    }
    st_echarts(options=option, height="400px")


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
        calc_fluence_array = log.fluence.actual.calc_map()
        expected_fluence_array = log.fluence.expected.calc_map()
        gamma_fluence_array = log.fluence.gamma.calc_map(distTA=2, doseTA=2, resolution=0.1)
        buffer = plot_heatmaps_to_buffer(calc_fluence_array, expected_fluence_array, gamma_fluence_array)
        st.image(buffer, caption='Heatmaps of Fluence and Gamma')
        # fig = px.imshow(fluence_array, aspect='equal')
        # st.plotly_chart(fig)

def plot_mu_calc():
    if "log" in st.session_state:
        log = st.session_state.log
        mu_calc = log.axis_data.mu.actual
        gantry_angle = log.axis_data.gantry.actual
        mu_calc_plot(mu_calc, gantry_angle)
        # plt.figure()
        # log.axis_data.mu.plot_actual()
        # buf = BytesIO()
        # plt.savefig(buf, format='png')
        # plt.close()
        # buf.seek(0)
        # st.session_state.mu_calc = buf

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
