import pandas as pd
import numpy as np
import random as rnd
import pickle as pkle
import os.path
import streamlit as st
import plotly.express as px
import plotly.colors as pcolors

def gen_number():
    st.session_state["ran"] = rnd.randint(1,10000)
    return

st.set_page_config(page_title="Monte Carlo Pi", page_icon='🔢',layout="wide")

if "intro" not in st.session_state:
    st.session_state["intro"] = False

if "ran" not in st.session_state:
    st.session_state["ran"] = rnd.randint(1,10000)

# start with an explination of why MC
col1,col2,col3 = st.columns([1,2,1])

with col2:
    st.title("Using Monte Carlo to Estimate Pi")
    st.write("""Monte Carlo simulations are very useful in a wide variety \
    of fields. That's because they give us a way to predict outcomes that would otherwise be \
    impossible (translation: hard enough not to bother :rolling_on_the_floor_laughing:) because \
    of random chance!
    Some examples of every day uses include:""")

# create 2 columns so we can add text on one side and a gif on the other
# Space out the maps so the first one is 2x the size of the second
col1, col2,col3,col4 = st.columns((1,1,1,1))
#column 1
with col2:
    st.write("""
**Finance and Business:** they can be used to evaluate risk in different options the business \
is looking at, such as investments

**Search and Rescue:** US coast guard uses it to predict likely locations of \
vessels in need of assistance

**Design and Visuals:** such as video games and producing 3D photo-realistic \
    models and pictures

**Climate Change:** the Intergovernmental Panel on Climate Change uses it \
    to help in the calculation of energy absorbed in the atmosphere due to greenhouse gasses

Click here if you want to know more about [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method)""")
    st.write('[Wiki for the image](https://en.wikipedia.org/wiki/Kinetic_theory_of_gases)')

# column 2: a gif
with col3:
    # streamlit share launches from a directory above so need to account for this in the file path
    st.image('MC_pi/Translational_motion.gif', caption='Brownian motion is random!')
    #if running locally use the line below for the image
    #st.image('Translational_motion.gif', caption='Brownian motion is random!')

with col2:
    st.subheader("*Lets get going!*")

    if st.button("Open simulation", key='start_'):
        st.session_state.intro = True

if st.session_state['intro']:

    st.write("---")

    ### Create sidebar
    with st.sidebar:

        st.title("Simulation Parameter")
        st.markdown("This is where you select the total number of randomly generated \
        points you want to use to estimate what Pi is:")
        iterations = st.number_input("Total Number of Points:", min_value=1,max_value= 10000, value=st.session_state["ran"])
        st.button("Random number", on_click=gen_number)

    col1,col2 = st.columns(2)

    with col1:
        # section 2 running a MC simulation
        st.header('Run Your First Monte Carlo Simulation! :sunglasses:')
        st.write("""
From the sidebar type a number in the field (or use the plus/minus button) for \
the total number of points you want to use to estimate Pi!

The idea behind this simulation \
[yes your a computational person now! :star-struck:] is that the ratio of area of the circle \
to the area outside the circle but inside the square (those corner bits) has a ratio that happens to be Pi. \
It's not a coincidence! Someone *discovered* this ratio and found it to be \
**SO useful** that we decided to give it a special name and symbol!

This graph shows all the points overlayed with a circle of radius = 1 and \
a square with sides of length = 2.""")

    # use the total number of points to generate pairs of x and y points for our graph
    x_list = []
    y_list = []
    inside_count = 0
    iterations = int(iterations)
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

    fig2 = px.scatter(
            x=x_list,
            y=y_list)
            #size=1)
    fig2.update_layout(width=700,
    height=700)
    fig2.add_shape(
        type="circle",
        x0=-1, x1=1,
        y0=-1, y1=1,
        line_color="red")

    # sent plot to streamlit
    col2.plotly_chart(fig2)

    # finally lets display our estimation of Pi, the true value and the percent
    # difference between the two (in this example r = 1, so dont need to divide by it)
    estimated_pi = 4*inside_count/iterations

    #calculate the percent difference from the standard: |value - true_value|/|true_value|*100%
    diff_percent = abs(estimated_pi-np.pi)/np.pi*100

    with st.sidebar:
        st.write("Number of points:",iterations)
        st.write("Your Estimation of Pi:", estimated_pi)
        st.write("True Value of Pi:", np.pi)
        st.write("The percent error between your estimation and the true value is:", round(diff_percent,3), "%")

    st.write("---")
    # lets track how the estimations change as we change the number of iterations!
    # actually going to add a new point to the graph for every new estimation of \pi
    col3, col4 = st.columns(2)
    with col3:
        st.header("How the Total Number of Points Affects Pi :hash:")
        st.write("""
One really cool thing about Monte Carlo is as you increase \
the total number of points you use in your simulation, the more accurate your results. \
This actually relies on a basic principle of statistics called 'The Law of Large Numbers' \
([you can learn more about it in the first 2 minutes of this video](https://www.youtube.com/watch?v=MntX3zWNWec)).

In practice this means that a graph like this one, that tracks your calculated Pi value, \
against the total number of points you used in it's estimation, will show less spread \
as the total number of points increases. In math/statistics we call this convergence.

In this case the number we converge on is the true value of Pi (I have added it as a \
red horizantal line on the graph). Notice how spread out the estimations are \
at low orders of magnitude (small numbers such as 1, 10 or 100) and how at large \
estimations (1000 or more) you can barely distinguish individual points!""")

        x_log = st.checkbox("log Number of Points", key="graph_1")

    #calculate error to store in data
    error = abs(estimated_pi-np.pi)/np.pi*100

    # check if a pickled file with all the previous dat is there, if not create Data
    # this will check for and create a new pkl file in main directory on streamlit servers
    data_file = os.path.isfile('pkled_data.pkl')

    if data_file:
        #the file exists, we want to read in previous data
        converge = pd.read_pickle('pkled_data.pkl')
        ## leave os remove file here until change to database structure
        #os.remove('pkled_data.pkl')
    else:
        #create database to work with
        converge = pd.DataFrame([[iterations, estimated_pi, error]], columns=['N_points','pi_est',"error"])

    if converge.iloc[-1,1] != estimated_pi:
        # add a line with new data in the converge
        converge.loc[len(converge)] = [iterations,estimated_pi,error]

#plot the convergence
    fig2 = px.scatter(
            x=converge['N_points'],
            y=converge['pi_est'],
            log_x=x_log,
            labels={'x':"Number of Points Used in Estimation",'y':"Calculated Pi values"})
            #size=1)

    fig2.add_shape(
        type="line",
        x0=1, x1=10000,
        y0=np.pi, y1=np.pi,
        line_color="red")

#send figure to streamlit
    col4.plotly_chart(fig2)

    st.write("---")
    # section on the 3rd grph that sorts points based on their order

    col5,col6 = st.columns(2)

    with col5:
        st.header('Keeping Track of Each New Estimate of Pi :pie:')
        st.write("""
This graph tracks the number of times you have estimated Pi and adds a \
point on the graph each time you try a different "Total Number of Points"! \
What is cool to see here is that the colour of the point depends on the total number of points.

You can really see the difference in how spread out the estimates are \
as you increase by an order of magnitude (i.e. when only using 1-9 points versus using 5000).

Notice how the pink numbers are all clustered near the true value of Pi (the red line), and as you decrease the \
number of points used to estimate, the points are spread over a larger and larger range of values!""")

        color = st.radio("Color points by:", ["Number of Points", "% Error"])
        range = st.slider("Range of Pi values:",0.0,4.0,[0.0,4.0],0.5)
        range = [range[0]-0.25, range[1]+0.25]

        if color == "Number of Points":
            column = "N_points"
        else:
            column = "error"
    fig2 = px.scatter(
            x=converge.index,
            y=converge['pi_est'],
            color=converge[column],
            color_continuous_scale = px.colors.sequential.Sunsetdark,
            labels={'x':"Trial Number",'y':"Calculated Pi values", 'color':"# of Points"})
            #size=1)
    fig2.update_layout(yaxis=dict(range=range))
    fig2.add_shape(
        type="line",
        x0=0, x1=len(converge),
        y0=np.pi, y1=np.pi,
        line_color="red")

    col6.plotly_chart(fig2)

    st.write("---")
    # add in graph on how the % errors change as iterations are increased!

    col7,col8 = st.columns(2)

    with col7:
        st.header('% Error as Iterations Change :chart_with_downwards_trend:')

        st.write("""
A great way to visually show how extreme the change in error is as you increase \
the number of points used in your simulation, is to plot each % Error as a function of \
the number of points!

The change in the error is *extreme* at the low \
end of the number of points (bottom right). It's actaully so extreme that it jumps from errors \
of 100% (yikes thats high!) at 5 points and under to an averge of only a few percent around 100 \
points. To better see the spread in the points you can log the axes of both the y-axis \
(the % error) and the x-axis (the number of points).""")

        # add checkboxes to sidebar to make the axes log!
        st.markdown("""
##### % Error Graph Parameters
To see the details of the error graph you can log one or both axes \
of the graph. This will display the order of magnitude (the number of 0's before or after \
the decmal point) of the percent error and total number of points.""")

        x_log = st.checkbox("log Number of Points")
        y_log = st.checkbox("log % Error")

    fig2 = px.scatter(
            x=converge['N_points'],
            y=converge['error'],
            color=converge['N_points'],
            color_continuous_scale = px.colors.sequential.Sunsetdark,
            log_y=y_log, log_x=x_log,
            labels={'x':"Number of Points Used in Estimation",'y':"% Error",'color':"# of Points"})
            #size=1)
    col8.plotly_chart(fig2)

    #repickle file with added data
    converge.to_pickle('pkled_data.pkl')

    # math section
    st.header("Show me the Math! :heart:  :nerd_face:")
    math = st.expander('click to see the math behind the estimation')

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
