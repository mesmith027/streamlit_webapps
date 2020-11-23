import streamlit as st 
import os
import base64
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

st.title('Thanksgiving Fun :turkey:')
st.subheader('The Turkey App!')
st.write('Use this app to create thanksgiving emojis!')

st.sidebar.markdown('## Make your selections here:')

pic_type = st.sidebar.radio('What do you want to see?', ['gif', 'emoji'])

if pic_type == 'gif': 
    choice = st.sidebar.selectbox('Pick your gif!', ['rocking_hand_turkey','turkey'])
    file_name = '%s.gif' %choice
else: 
    pic_list = ['charlie_brown','cornucopia', 'happy_thanksgiving','table','thanksgiving','turkey_basic','turkey_hat', 'turkey_sketch']
    choice = st.sidebar.selectbox('Pick your emoji!', pic_list)
    if choice == 'thanksgiving':
        file_name = '%s.jpg' %choice
    if (choice =='happy_thanksgiving') or (choice =='cornucopia'):
        file_name = '%s.jpeg' %choice
    else: 
        file_name = '%s.png' %choice

st.image('img/%s' %file_name)

st.markdown(get_binary_file_downloader_html('img/%s' %file_name, pic_type), unsafe_allow_html=True)