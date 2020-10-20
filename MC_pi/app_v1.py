import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mat_colors
import random as rnd
import pickle as pkle
import os.path
import streamlit as st

st.title("Using Monte Carlo to Estimate Pi")

st.write("Believe it or not Monte Carlo simulations are very useful in a wide variety \
of fields. That's because they give us a way to predict outcomes that would otherwise be \
impossible (translation: hard enough not to bother :rolling_on_the_floor_laughing:) because \
of random chance! ")

st.write("Some examples of every day uses include:")
st.write("**Finance and Business:** they can be used to evaluate risk in different \
options the business is looking at, such as investments")
st.write("**Search and Rescue:** US coast guard uses it to predict likely locations of \
vessels in need of assistance")
st.write("**Design and Visuals:** such as video games and producing 3D photo-realistic \
models and pictures")
st.write("**Climate Change:** the Intergovernmental Panel on Climate Change uses it \
to help in the calculation of energy absorbed in the atmosphere due to greenhouse gasses")
st.write("If you want to know more checkout the [Wiki link](https://en.wikipedia.org/wiki/Monte_Carlo_method)")
st.write("*Lets get going!*")

st.header('Run Your First Monte Carlo Simulation! :sunglasses:')

st.write('From the sidebar type a number in the field (or use the plus button) for \
the total number of points you want to use to estimate Pi! ')

st.write("The idea behind this simulation \
(yes your a computational person now! :star-struck:) is that the ratio of area of the circle \
to the area outside the circle but inside the square (those corner bits) has a ratio that happens to be Pi. \
It's not a coincidence! Someone *discovered* this ratio and found it to be \
**SO useful** that we decided to give it a special name and symbol!")

st.write("This graph shows all the points overlayed with a circle of radius = 1 and \
a square with sides of length = 2.")

st.sidebar.markdown("This is where you select the total number of randomly generated \
points you want to use to estimate what Pi is:")
iterations = st.sidebar.number_input("Total Number of Points", min_value=1,max_value= 10000, value=500)

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
plt.scatter(x_list, y_list,s=1, color='r')

ax.set_ylabel("y-value", fontsize = 10)
ax.set_xlabel("x-value", fontsize = 10)

st.pyplot(fig)

estimated_pi = 4*inside_count/iterations
st.write("Your Estimation of Pi:",estimated_pi )
st.write("True Value of Pi:", np.pi)
diff_percent = round(abs(estimated_pi-np.pi)/np.pi*100,3)
st.write("The percent error bewteen your estimation and the true value is:", diff_percent, "%")

# lets track how the estimations change as we change the number of iterations!
# actually going to add a new point to the graph for every new estimation of \pi
st.header("How the Total Number of Points Affects Your Estimate")
st.write("One really cool thing about Monte Carlo is that generally as you increase \
the total number of points you use in your smluation, the more accurate your results. \
This actually relies on a basic principle of statistics called 'The Law of Large Numbers' \
([you can learn more about it in the first 2 minutes of this video](https://www.youtube.com/watch?v=MntX3zWNWec)).")

st.write("In practice this means that a graph like the one below, that tracks your calculated Pi value \
against the total number of points you used in its estimation, will show less spread \
as the total number of points increases. In math/statistics we call this convergence. \
In this case the number we converge on is the true value of Pi (I have added it as a \
black horizantal line on the graph). Notice how spread out the estimations are \
at low orders of magnitude (small numbers such as 1, 10 or 100) and how at large \
estimations (1000 or more) you can barely distinguish individual points!")
# check if a pickled file with all the previous dat is there, if not create Data
data_file = os.path.isfile('pkled_data.pkl')

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

# plot the convergence
fig1 = plt.figure()
ax1 = fig1.gca()

plt.xlim(1,max(converge['N_points']+1000))
plt.ylim(1.5,4.25)
ax1.set_xscale('log')

plt.scatter(converge['N_points'], converge['pi_est'], color='r', s=5)
plt.hlines(np.pi, 0, max(converge['N_points']+1000), colors='k', label='True Pi', linewidth=2)

ax1.set_ylabel("Calculated Pi Values", fontsize = 10)
ax1.set_xlabel("Number of Points Used in Estimation", fontsize = 10)

st.pyplot(fig1)

st.header('Keeping Track of Each New Estimate of Pi')
st.write('This graph tracks the number of times you have estimated Pi and adds a \
point on the graph each time you try a different "Total Number of Points" or refresh the page! \
What is cool to see here is that the colour of the point depends on the total number of points. \
This is a log scale, so that you can really see the difference in how spread out the estimates are \
as you increase by an order of magnitude. (i.e. when only using 1-9 points versus using 5000) \
Notice how the pink numbers are all clustered near the true value of Pi (the black line), and as you decrease the \
number of points used to estimate, the points are spread over a larger and large range of values!')

fig2 = plt.figure()
ax2 = fig2.gca()

plt.scatter(converge.index, converge['pi_est'],s=6, c= converge['N_points'], cmap='cool', norm=mat_colors.LogNorm())
plt.hlines(np.pi, 0, max(converge['N_points'].index), colors='k', label='True Pi', linewidth=2)
plt.colorbar()
ax2.set_ylabel("Calculated Pi Values", fontsize = 10)
ax2.set_xlabel("Trial Number", fontsize = 10)

st.pyplot(fig2)


# math section
st.header("Show me the Math! :heart:  :nerd_face:")
math = st.checkbox('click to see the math behind the estimation')

if math:
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
