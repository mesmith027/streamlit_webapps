import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_colors
import random as rnd
import pickle as pkle
import os.path
import streamlit as st


# start with an explination of why MC
st.title("Using Monte Carlo to Estimate Pi")
st.write("Monte Carlo simulations are very useful in a wide variety \
of fields. That's because they give us a way to predict outcomes that would otherwise be \
impossible (translation: hard enough not to bother :rolling_on_the_floor_laughing:) because \
of random chance! ")
st.write("Some examples of every day uses include:")

# create 2 columns so we can add text on one side and a gif on the other
# Space out the maps so the first one is 2x the size of the second
col1, col2 = st.beta_columns((2,1))
#column 1

col1.write("**Finance and Business:** they can be used to evaluate risk in different \
options the business is looking at, such as investments")
col1.write("**Search and Rescue:** US coast guard uses it to predict likely locations of \
vessels in need of assistance")
col1.write("**Design and Visuals:** such as video games and producing 3D photo-realistic \
models and pictures")
col1.write("**Climate Change:** the Intergovernmental Panel on Climate Change uses it \
to help in the calculation of energy absorbed in the atmosphere due to greenhouse gasses")
col1.write("If you want to know more checkout the [Wiki link](https://en.wikipedia.org/wiki/Monte_Carlo_method)")

# column 2: a gif
col2.write('[Wiki for the image](https://en.wikipedia.org/wiki/Kinetic_theory_of_gases)')
# streamlit share launches from a directory above so need to account for this in the file path
col2.image('MC_pi/Translational_motion.gif', caption='Brownian motion is random!')

st.write("*Lets get going!*")

# section 2 running a MC simulation
st.header('Run Your First Monte Carlo Simulation! :sunglasses:')
st.write('From the sidebar type a number in the field (or use the plus/minus button) for \
the total number of points you want to use to estimate Pi! ')

st.write("The idea behind this simulation \
(yes your a computational person now! :star-struck:) is that the ratio of area of the circle \
to the area outside the circle but inside the square (those corner bits) has a ratio that happens to be Pi. \
It's not a coincidence! Someone *discovered* this ratio and found it to be \
**SO useful** that we decided to give it a special name and symbol!")

st.write("This graph shows all the points overlayed with a circle of radius = 1 and \
a square with sides of length = 2.")

st.sidebar.title("Simulation Parameter")
st.sidebar.markdown("This is where you select the total number of randomly generated \
points you want to use to estimate what Pi is:")
start_value = rnd.randint(1,10000)
iterations = st.sidebar.number_input("Total Number of Points", min_value=1,max_value= 10000, value=start_value)

# use the total number of points to generate pairs of x and y points for our graph
x_list = []
y_list = []
inside_count = 0
for num in range(iterations):
    # get the random values for the y and y coordinates, we want them to be generated
    # between -1 and 1 for both values to fit in our square
    x_random = rnd.uniform(-1,1)
    x_list.append(x_random)
    y_random = rnd.uniform(-1,1)
    y_list.append(y_random)

    #check if the point is inside the circle
    if (x_random**2 +y_random**2) <= 1.0:
        inside_count += 1

#create the circle for the graph
circle = plt.Circle((0,0), 1, color='b', fill=False)

#lets plot our paired points and circle on a graph!
fig = plt.figure()
ax = fig.gca()

# plot circle first
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.grid(linestyle='--')
ax.set_aspect(1)
ax.add_artist(circle)

#plot our points on it
plt.scatter(x_list, y_list,s=1, color='r')

ax.set_ylabel("y-value", fontsize = 10)
ax.set_xlabel("x-value", fontsize = 10)

st.pyplot(fig)

# finally lets display our estimation of Pi, the true value and the percent
# difference between the two (in this example r = 1, so dont need to divide by it)
estimated_pi = 4*inside_count/iterations
st.write("Your Estimation of Pi:", estimated_pi)
st.write("True Value of Pi:", np.pi)
#calculate the percent difference from the standard: |value - true_value|/|true_value|*100%
diff_percent = abs(estimated_pi-np.pi)/np.pi*100
st.write("The percent error between your estimation and the true value is:", round(diff_percent,3), "%")

# lets track how the estimations change as we change the number of iterations!
# actually going to add a new point to the graph for every new estimation of \pi
st.header("How the Total Number of Points Affects Your Estimate")
st.write("One really cool thing about Monte Carlo is as you increase \
the total number of points you use in your simulation, the more accurate your results. \
This actually relies on a basic principle of statistics called 'The Law of Large Numbers' \
([you can learn more about it in the first 2 minutes of this video](https://www.youtube.com/watch?v=MntX3zWNWec)).")

st.write("In practice this means that a graph like the one below, that tracks your calculated Pi value \
against the total number of points you used in it's estimation, will show less spread \
as the total number of points increases. In math/statistics we call this convergence. \
In this case the number we converge on is the true value of Pi (I have added it as a \
grey horizantal line on the graph). Notice how spread out the estimations are \
at low orders of magnitude (small numbers such as 1, 10 or 100) and how at large \
estimations (1000 or more) you can barely distinguish individual points!")
# check if a pickled file with all the previous dat is there, if not create Data
# streamlit share launches from a directory above so need to account for this in the file path
data_file = os.path.isfile('MC_pi/pkled_data.pkl')

if data_file:
    #the file exists, we want to read in previous data
    converge = pd.read_pickle('MC_pi/pkled_data.pkl')
else:
    #create database to work with
    converge = pd.DataFrame([[iterations, estimated_pi]], columns=['N_points','pi_est'])

if converge.iloc[-1,1] != estimated_pi:
    # add a line with new data in the converge
    converge.loc[len(converge)] = [iterations,estimated_pi]

#repickle file with added data
converge.to_pickle('MC_pi/pkled_data.pkl')

# plot the convergence
fig1 = plt.figure()
ax1 = fig1.gca()

plt.xlim(0.9,max(converge['N_points']+1000))
#plt.ylim(,4.25)
ax1.set_xscale('log')

# zorder puts the line behind the points
plt.hlines(np.pi, 0, max(converge['N_points']+1000), colors='grey', label='True Pi', linewidth=2, zorder=0)
plt.scatter(converge['N_points'], converge['pi_est'], color='r', s=5, zorder=10)

ax1.set_ylabel("Calculated Pi Values", fontsize = 10)
ax1.set_xlabel("Number of Points Used in Estimation", fontsize = 10)

st.pyplot(fig1)

# section on the 3rd grph that sorts points based on their order
st.header('Keeping Track of Each New Estimate of Pi')
st.write('This graph tracks the number of times you have estimated Pi and adds a \
point on the graph each time you try a different "Total Number of Points" or refresh the page! \
What is cool to see here is that the colour of the point depends on the total number of points. \
This is a log scale, so that you can really see the difference in how spread out the estimates are \
as you increase by an order of magnitude. (i.e. when only using 1-9 points versus using 5000) \
Notice how the pink numbers are all clustered near the true value of Pi (the grey line), and as you decrease the \
number of points used to estimate, the points are spread over a larger and larger range of values!')

fig2 = plt.figure()
ax2 = fig2.gca()

plt.hlines(np.pi, 0, max(converge['N_points'].index), colors='grey', label='True Pi', linewidth=2, zorder=0)
plt.scatter(converge.index, converge['pi_est'],s=6, c= converge['N_points'], cmap='cool', norm=mat_colors.LogNorm(), zorder=10)
plt.colorbar()
ax2.set_ylabel("Calculated Pi Values", fontsize = 10)
ax2.set_xlabel("Trial Number", fontsize = 10)

st.pyplot(fig2)

# add in graph on how the % errors change as iterations are increased!
st.header('Difference in the % Error as Number of Points Change')

st.write("A great way to visually show how extreme the change in error is as you increase \
the number of points used in your simulation, is to plot each % Error as a function of \
the number of points- as we have done below! The change in the error is *extreme* at the low \
end of the number of points (bottom right). It's actaully so extreme that it jumps from errors \
of 100% (yikes thats high!) at 5 points and under to an averge of only a few percent around 100 \
points. To better see the spread in the points you can log the axes of both the y-axis \
(the % error) and the x-axis (the number of points).")

# add checkboxes to sidebar to make the axes log!
st.sidebar.title("% Error Graph Parameters")
st.sidebar.markdown("To see the details of the error graph you can log one or both axes \
of the graph. This will display the order of magnitude (the number of 0's before or after \
the decmal point) of the percent error and total number of points.")

x_log = st.sidebar.checkbox("Set x-axis to log (base 10)")
y_log = st.sidebar.checkbox("set y-axis to log (base 10)")
# create % error y values array
error_values = abs(converge['pi_est']-np.pi)/np.pi*100

# plot the graph
fig3 = plt.figure()
ax3 = fig3.gca()

if x_log:
    ax3.set_xscale('log')
if y_log:
    ax3.set_yscale('log')

plt.scatter(converge['N_points'], error_values, s=6, c= converge['N_points'], cmap='cool', norm=mat_colors.LogNorm(), zorder=10)

ax3.set_ylabel("% Error", fontsize = 10)

ax3.set_xlabel("Number of Points Used in Estimation", fontsize = 10)

st.pyplot(fig3)

# math section
st.header("Show me the Math! :heart:  :nerd_face:")
math = st.beta_expander('click to see the math behind the estimation')

with math:
    st.write('The area of a circle and a square are as shown. In this case the length\
    of the square is 2 times the radius of the circle or 2r:')

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
