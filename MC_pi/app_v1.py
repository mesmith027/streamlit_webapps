import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import pickle as pkle
import os.path
import streamlit as st

st.title("Using Monte Carlo to estimate Pi")

st.write("description of what Monte Carlo simulations are to go here")

st.header("Show me the Math! :heart:  :nerd_face:")
math = st.checkbox('click to see the math behind the estimation')

if math:
    st.write('The area of a circle and a square are as shown. In this case the length\
    of the square is 2r')

    st.latex(r'''A_{circle} = \pi r^2''')
    st.latex(r'''A_{square} = 2l = 2(2r) = 4r''')

    st.write("The trick here is that the ratio of the areas of the circle and square \
    can be related to the number of random points that fall inside the circle and \
    square respectively")

    st.latex(r'''\frac{A_{circle}}{A_{square}} = \frac{\text{points in circle}}{\text{total points}} ''')

    st.write("this becomes....")

    st.latex(r'''\frac{A_{circle}}{A_{square}} = \frac{\pi r^{\cancel{2}}}{4\cancel{r}}
    = \frac{\pi r}{4}''')

    st.latex(r''' \frac{\pi r}{4} = \frac{\text{points in circle}}{\text{total points}} ''')
    st.latex(r''' \pi = \frac{4}{r}\frac{\text{points in circle}}{\text{total points}} ''')

st.write("lets get going!")

iterations = st.sidebar.number_input("Total Number of Points", min_value=1,value=1)

# use the total number of points to generate pairs of x and y points for our graph
x_list = []
y_list = []
inside_count = 0
for num in range(iterations):
    # get the random values for the y and y coordinates, we want them to be generated
    # between -1 and 1 for both values
    x_random = rnd.uniform(-1,1)
    x_list.append(x_random)
    y_random = rnd.uniform(-1,1)
    y_list.append(y_random)

    #count if x^2 +y^2 <= 1 (inside circle)
    if (x_random**2 +y_random**2) <= 1.0:
        inside_count += 1

#create the circle
circle = plt.Circle((0,0), 1, color='b', fill=False)

#lets plot our paired points on a graph!
fig = plt.figure()
ax = fig.gca()

# plot circle first
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.grid(linestyle='--')
ax.set_aspect(1)
ax.add_artist(circle)

#plot our points on it
plt.scatter(x_list, y_list,s=0.7, color='r')

ax.set_ylabel("y-value", fontsize = 10)
ax.set_xlabel("x-value", fontsize = 10)

st.pyplot(fig)

estimated_pi = 4*inside_count/iterations
st.write("Estimation of Pi:",estimated_pi )
st.write("True value of Pi:", np.pi)

# lets track how the estimations change as we change the number of iterations!
# actually going to add a new point to the graph for every new estimation of \pi

# check if a pickled file with all the previous dat is there, if not create Data
data_file = os.path.isfile('pkled_data.pkl')
data_file

if data_file:
    #the file exists, we want to read in previous data
    converge = pd.read_pickle('pkled_data.pkl')
else:
    #create database to work with
    converge = pd.DataFrame([[iterations, estimated_pi]], columns=['N_points','pi_est'])

if converge.iloc[-1,1] != estimated_pi:
    # add a line with new data in the converge
    converge.loc[len(converge)] = [iterations,estimated_pi]

#repickle file with added data
converge.to_pickle('pkled_data.pkl')

fig1 = plt.figure()
ax1 = fig1.gca()

plt.xlim(1,max(converge['N_points']))
plt.ylim(1.5,4.25)
ax1.set_xscale('log')

plt.scatter(converge['N_points'], converge['pi_est'])
plt.hlines(np.pi, 0, max(converge['N_points']), colors='g', label='True Pi')

ax1.set_ylabel("Calculated Pi Values", fontsize = 10)
ax1.set_xlabel("Number of Points Used in Estimation", fontsize = 10)

st.pyplot(fig1)
