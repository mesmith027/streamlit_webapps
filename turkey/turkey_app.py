import streamlit as st 
from PIL import Image
import os
import base64

# used to convert charlie brown & table image into rgb format dues to image.open error: OSError: cannot write mode P as JPEG
#Image.open('img/table.png').convert('RGB').save('img/table.png')

def get_binary_file_downloader_html(bin_file, file_label='File'):
    # borrowed from the streamlit community 
    # create a button to download a file
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def change_size(image, desired_size): 
    # change the size of the images selected to display on the screen 
    # desired_size represents a percentage of the size to be displayed
    size_dic = {
        'tiny': 0.25,
        's': 0.5,
        'm': 0.75,
        'true': 1,
        'l': 1.25,
        'xl': 1.5,
        'gigantic': 1.75
    }
    percent = size_dic[desired_size]
    resize = image.resize((int(image.width*percent),int(image.height*percent)))
    return resize

st.title('Thanksgiving Fun :turkey:')
st.write('pick your favourite Thanksgiving gif or emoji and download it to share!!!')

st.sidebar.markdown('## Make your selections here:')

pic_type = st.sidebar.radio('What do you want to see?', ['gif', 'emoji'])

if pic_type == 'gif': 
    choice = st.sidebar.selectbox('Pick your gif!', ['hungry_cat','rocking_hand_turkey','turkey', 'Joey', 'monica', 'sign_language'])
    file_name = 'img/%s.gif' %choice
    st.image(file_name)
else: 
    pic_list = ['charlie_brown','cornucopia', 'happy_thanksgiving','table','thanksgiving','turkey_basic','turkey_hat', 'turkey_sketch']
    choice = st.sidebar.selectbox('Pick your emoji!', pic_list)
    if choice == 'thanksgiving':
        file_name = 'img/%s.jpg' %choice
        pic_end = '.jpg'
    elif (choice =='happy_thanksgiving') or (choice =='cornucopia'):
        file_name = 'img/%s.jpeg' %choice
        pic_end = '.jpeg'
    else: 
        file_name = 'img/%s.png' %choice
        pic_end = '.png'

    file_name = 'img/{}{}'.format(choice,pic_end)
    size = st.sidebar.selectbox('Image Size', ['tiny','s','m','true','l','xl','gigantic'], index = 3)
    the_image = Image.open(file_name)

    modified_image = change_size(the_image,size)

    st.image(modified_image)

    modified_image.save('img/current_image{}'.format(pic_end))

st.markdown(get_binary_file_downloader_html(file_name, pic_type), unsafe_allow_html=True)