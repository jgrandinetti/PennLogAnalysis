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

def plot_heatmap(data):
    option = {
        "xAxis": {"show": False},
        "yAxis": {"show": False},
        "visualMap": {
            "show": True,
            "min": int(data.min()),
            "max": int(data.max()),
            "orient": "vertical",
            "left": "right",
            "top": "middle",
            "inRange": {
                "color": ["#000000", "#FFFFFF"]
            }
        },
        "series": [{
            "type": "heatmap",
            "data": [],
            "emphasis": {
                "itemStyle": {
                    "borderColor": "#333",
                    "borderWidth": 1
                }
            },
            "progressive": 1000,
            "animation": True
        }],
    }

    # Convert the NumPy array to the format required by ECharts
    height, width = data.shape
    echarts_data = [[j, height - i - 1, int(data[i, j])] for i in range(height) for j in range(width)]
    option["series"][0]["data"] = echarts_data

    st_echarts(options=option, height="600px")



def mu_calc_plot(mu, gantry):
    mu_list = mu.tolist()
    gantry_list = gantry.tolist()
    x_labels = list(range(1, len(mu_list) + 1))

    option = {
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
                "color": "#2980b9"
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
        fluence_array = log.fluence.actual.calc_map()
        # plot_heatmap(fluence_array)
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
