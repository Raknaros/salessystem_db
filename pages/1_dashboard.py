import streamlit as st
from home import authenticator

st.set_page_config(page_title="Dashboard", page_icon=":material/edit:")

st.title("this is the app title")
st.write("Hello ,let's learn how to build a streamlit app together")

st.session_state.sidebar()

st.write("Contenido de otra página")



st.header("this is the markdown")
st.markdown("this is the header")
st.subheader("this is the subheader")
st.caption("this is the caption")
st.code("x=2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

#st.image("pages/media/testlogo.png",caption="testlogo")
#st.audio("Audio.mp3")
#st.video("video.mp4")



st.checkbox('yes')
st.button('Click')
st.radio('Pick your gender', ['Male', 'Female'])
st.selectbox('Pick your gender', ['Male', 'Female'])
st.multiselect('choose a planet', ['Jupiter', 'Mars', 'neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0, 50)

st.number_input('Pick a number', 0,10)
st.text_input('Email address')
st.date_input('Travelling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')
