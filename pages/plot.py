import plotly.express as px
import streamlit as st

z = [[.1, .3, .5, .7, .9],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1]]

fig = px.imshow(z, text_auto=True)

# Update layout to maintain equal aspect ratio
fig.update_layout(
    autosize=False,
    width=500,  # Adjust width to your preference
    height=500,  # Adjust height to match the width or according to your data aspect ratio
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(fig)



