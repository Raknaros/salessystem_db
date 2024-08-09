import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Some content')

col1, col2 = st.columns(2)

col1.subheader("Ingresar Pedido Individual")
col1.date_input('Fecha del pedido')
col1.text_input('periodo', placeholder='Periodo', label_visibility='collapsed')
col1.text_input('adquiriente', placeholder='Adquiriente', label_visibility='collapsed')
col1.text_input('total', placeholder='Total', label_visibility='collapsed')
col1.text_input('rubro', placeholder='Rubro', label_visibility='collapsed')
col1.text_input('promedio', placeholder='Promedio por factura', label_visibility='collapsed')
col1.text_input('llegada', placeholder='Punto de llegada para las guias', label_visibility='collapsed')
col1.checkbox('Bancariza')
col1.text_input('Notas')

col2.file_uploader("Ingresar Pedido Masivo")
col2.button("Subir")

container3 = st.container(height=100)

container3.write("seguindo contenedor")
