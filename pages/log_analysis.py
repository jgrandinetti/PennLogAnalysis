from pylinac import load_log
from pylinac.log_analyzer import anonymize
import streamlit as st
import tempfile
import shutil
import matplotlib.pyplot as plt
import plotly.subplots as sp
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Polar


def plot_heatmaps_to_buffer(calculated_fluence, expected_fluence, gamma):
    fig = sp.make_subplots(rows=1, cols=3, subplot_titles=("Calculated Fluence", "Expected Fluence", "Gamma"),
                           shared_yaxes=True, horizontal_spacing=0.02)

    # Plot calculated fluence
    trace1 = go.Heatmap(
        z=calculated_fluence, 
        colorscale='Jet', 
        hovertemplate='%{z}<extra></extra>'
    )
    fig.add_trace(trace1, row=1, col=1)

    # Plot expected fluence
    trace2 = go.Heatmap(
        z=expected_fluence, 
        colorscale='Jet', 
        hovertemplate='%{z}<extra></extra>'
    )
    fig.add_trace(trace2, row=1, col=2)

    # Plot gamma
    trace3 = go.Heatmap(
        z=gamma, 
        colorscale='Jet', 
        hovertemplate='%{z}<extra></extra>'
    )
    fig.add_trace(trace3, row=1, col=3)

    fig.update_layout(height=380, width=680, title_text="Heatmaps")
    fig.update_traces(showscale=False)
    st.plotly_chart(fig)


def create_polar_plot(monitor_units, gantry_angles, target_degree_change=1):
    # data = []
    # for i in range(0, len(gantry_angles) - step, step):
    #     theta = round(gantry_angles[i], 2)
    #     r = round(monitor_units[i + step] - monitor_units[i], 2)
    #     data.append([r, theta])
    
    # data = []
    # for i in range(0, len(gantry_angles) - step, step):
    #     theta = round(sum(gantry_angles[i:i+step]) / step, 2)
    #     r = sum(monitor_units[j+1] - monitor_units[j] for j in range(i, i + step))
    #     r = round(r, 2)
    #     data.append([r, theta])

    data = []
    average_degree_change_per_index = sum(abs(gantry_angles[i+1] - gantry_angles[i]) for i in range(len(gantry_angles) - 1)) / (len(gantry_angles) - 1)
    step = max(1, int(round(target_degree_change / average_degree_change_per_index)))
    for i in range(0, len(gantry_angles) - step, step):
        theta = round(sum(gantry_angles[i:i+step]) / step, 2)
        r = sum(monitor_units[j+1] - monitor_units[j] for j in range(i, i + step))
        r = round(r, 2)
        data.append([r, theta])
    
    c = (
        Polar()
        .add(
            series_name="MU (Insert arc info later)",
            data=data,
            label_opts=opts.LabelOpts(is_show=False),
            symbol="none",
            tooltip_opts=opts.TooltipOpts(
            formatter="{a}<br/>Monitor Units: {c}"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color="#3498db", border_width=3),
        )
        .add_schema(
            angleaxis_opts=opts.AngleAxisOpts(
                start_angle=90,
                min_=0,
                max_=360,
                type_="value",
                is_clockwise=True,
                interval=90,
                boundary_gap=False,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(formatter="{value}°"),
            )
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title="Monitor Units vs Gantry Angle"),
        )
    )
    st_pyecharts(c, height="600px", width="800px")



def mu_calc_plot(mu, gantry):
    mu_list = mu.tolist()
    gantry_list = gantry.tolist()
    
    mu_list = [round(value, 2) for value in mu_list]
    gantry_list = [round(value, 2) for value in gantry_list]
    
    x_labels = list(range(1, len(mu_list) + 1))

    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'line'
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


def log_info():
    if "log" in st.session_state:
        log = st.session_state.log

        st.write(" ")
        st.write(" ")
        st.markdown("<h4 style='text-align: center;'>Log Information</h4>", unsafe_allow_html=True)


        # No. of beams
        st.write(f"No. of beams: {log.header.num_subbeams}")

        # Treatment time
        samp_int = log.header.sampling_interval
        snaps = log.header.num_snapshots
        total_time = round(((samp_int * snaps) / 60000), 2)
        st.write(f"Total time: {total_time} min")

        # MLC Info
        mlc_95 = round((log.axis_data.mlc.get_error_percentile(percentile=95)*100), 2)
        mlc_rms = round(log.axis_data.mlc.get_RMS_avg(), 4)

        st.write(f"Total Leaves: {log.axis_data.mlc.num_leaves}")
        st.write(f"No. of leaves used: {log.axis_data.mlc.num_moving_leaves}")
        st.write(f"MLC 95% Error: {mlc_95}%")
        st.write(f"Avg. MLC RMS: {mlc_rms}")      


def plot_fluence_map():
    if "log" in st.session_state:
        log = st.session_state.log
        calc_fluence_array = log.fluence.actual.calc_map()
        expected_fluence_array = log.fluence.expected.calc_map()

        # log.fluence.gamma.calc_map(distTA=0.1, doseTA=0.1, resolution=0.1)
        # st.write(f"Gamma 0.1% / 0.1mm: {log.fluence.gamma.pass_prcnt}%")
        # log.fluence.gamma.calc_map(distTA=2, doseTA=2, resolution=0.1)
        # st.write(f"Gamma 1% / 1mm: {log.fluence.gamma.pass_prcnt}%")

        gamma_fluence_array = log.fluence.gamma.calc_map(distTA=1, doseTA=1, resolution=0.1)
        plot_heatmaps_to_buffer(calc_fluence_array, expected_fluence_array, gamma_fluence_array)


def plot_mu_calc():
    if "log" in st.session_state:
        log = st.session_state.log
        mu_calc = log.axis_data.mu.actual
        gantry_angle = log.axis_data.gantry.actual
        mu_calc_plot(mu_calc, gantry_angle)
        create_polar_plot(mu_calc, gantry_angle, target_degree_change=2)

uploaded_file = st.file_uploader("Upload log file", type=['bin'], on_change=save_uploaded_file, args=(st.session_state.get('uploaded_file', None),))

if "uploaded_file" not in st.session_state and uploaded_file is not None:
    save_uploaded_file(uploaded_file)

if "log" not in st.session_state:
    load_log_file()

# Log Info
if "log" in st.session_state:
    log_info()

# Fluence
if "log" in st.session_state:
    plot_fluence_map()

# MU Plot
if "mu_calc" not in st.session_state:
    plot_mu_calc()
