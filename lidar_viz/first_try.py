import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go

import streamlit as st

# load LiDAR data from raw_data scan0XX.txt
# format x, y, z, r, \theta, \phi, reflectance value
# only need x, y, z coordinates

colnames = ['x','y','z','r','theta','phi','reflectance']
@st.cache
def load():
    scan_000 = pd.read_csv("raw_data/scan000.txt",names=colnames,sep=' ', usecols=[0,1,2], skiprows=1, nrows=20000)
    return scan_000
scan_000 = load()

st.title('LiDAR Data of the City of Bremen')
#st.write(scan_000)

fig = plt.figure()
ax = fig.gca()

plt.scatter(scan_000['x'], scan_000['y'])

ax.set_ylabel("y-value", fontsize = 10)
ax.set_xlabel("x-value", fontsize = 10)

st.pyplot(fig)

the_data = go.Scatter3d(
    x=scan_000['x'],
    y=scan_000['y'],
    z=scan_000['z'],
    mode='markers',
    opacity=0.5,
    marker=dict(
            color='blue', #LightSkyBlue
            size=1)
)
the_layout = go.Layout(
    scene = {
    'xaxis':{'title':"x-coordinates"},
    'yaxis':{'title':"y-coordinates"},
    'zaxis':{'title':"z-coordinates"}
    })
fig4 = go.Figure(data=the_data, layout=the_layout)

st.plotly_chart(fig4, use_container_width=True)
