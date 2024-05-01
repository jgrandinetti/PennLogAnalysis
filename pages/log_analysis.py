from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
import plotly.subplots as sp
from io import BytesIO
import plotly.express as px
import numpy as np
from streamlit_echarts import st_echarts


def plot_heatmaps_to_buffer(calculated_fluence, expected_fluence, gamma):
    fig = sp.make_subplots(rows=1, cols=3, subplot_titles=("Calculated Fluence", "Expected Fluence", "Gamma"))

    # Plot calculated fluence heatmap
    trace1 = px.imshow(calculated_fluence, text_auto=True, aspect="square", colorscale="jet")
    fig.add_trace(trace1.data[0], row=1, col=1)

    # Plot expected fluence heatmap
    trace2 = px.imshow(expected_fluence, text_auto=True, aspect="square", colorscale="jet")
    fig.add_trace(trace2.data[0], row=1, col=2)

    # Plot gamma heatmap
    trace3 = px.imshow(gamma, text_auto=True, aspect="square", colorscale="jet")
    fig.add_trace(trace3.data[0], row=1, col=3)

    fig.update_layout(height=500, width=1000, title_text="Heatmaps")
    st.plotly_chart(fig)



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

        # st.write(f"Treatment type: {log.TreatmentType()}")
        st.write(f"Patient Name: {log.header.mlc_model}")
        
        log.fluence.gamma.calc_map(distTA=0.1, doseTA=0.1, resolution=0.1)
        st.write(f"Gamma 0.1% / 0.1mm: {log.fluence.gamma.pass_prcnt}%")
        log.fluence.gamma.calc_map(distTA=2, doseTA=2, resolution=0.1)
        st.write(f"Gamma 1% / 1mm: {log.fluence.gamma.pass_prcnt}%")

        gamma_fluence_array = log.fluence.gamma.calc_map(distTA=1, doseTA=1, resolution=0.1)
        plot_heatmaps_to_buffer(calc_fluence_array, expected_fluence_array, gamma_fluence_array)
        # st.image(buffer, caption='Heatmaps of Fluence and Gamma')
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
