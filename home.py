import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep

from services.Querys import adquirientes, proveedores, catalogo, vehiculos

st.set_page_config(page_title="Home", page_icon=":material/edit:", layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main', fields={'Form name': 'Login'})


def other_sidebar():
    st.sidebar.header(st.session_state["name"])
    st.sidebar.page_link('home.py', label='Home')
    st.sidebar.page_link('pages/2_cargar_pedidos.py', label='Pedidos')
    st.sidebar.page_link('pages/3_cargar_cotizaciones.py', label='Cotizaciones')
    st.sidebar.page_link('pages/4_cargar_bancarizaciones.py', label='Bancarizaciones')
    st.sidebar.page_link('pages/5_informacion_adicional.py', label='Informacion Adicional', disabled=True)


def gerencia_sidebar():
    st.sidebar.header(st.session_state["name"])
    st.sidebar.page_link('home.py', label='Home')
    st.sidebar.page_link('pages/1_dashboard.py', label='Dashboard')
    st.sidebar.page_link('pages/2_cargar_pedidos.py', label='Pedidos')
    st.sidebar.page_link('pages/3_cargar_cotizaciones.py', label='Cotizaciones')
    st.sidebar.page_link('pages/4_cargar_bancarizaciones.py', label='Bancarizaciones')
    st.sidebar.page_link('pages/5_informacion_adicional.py', label='Informacion Adicional', disabled=True)


if st.session_state["authentication_status"]:
    sleep(1)
    authenticator.logout()
    st.write(f'Bienvenid@ *{st.session_state["name"]}*')
    st.title('Informacion Adicional')
    if username == 'gerencia':
        # Sidebar navigation
        if 'gerencia_sidebar' not in st.session_state:
            st.session_state.gerencia_sidebar = gerencia_sidebar
        gerencia_sidebar()
    else:
        # Using object notation
        if 'other_sidebar' not in st.session_state:
            st.session_state.other_sidebar = other_sidebar
        other_sidebar()

    tab1, tab2, tab3, tab4 = st.tabs(["Proveedores", "Adquirientes", "Catalogo", "Vehiculos"])

    with tab1:
        st.dataframe(adquirientes, height=300, hide_index=True, column_config={
            "ruc": st.column_config.NumberColumn(
                "RUC",
                help="Numero de RUC del adquiriente o cliente",
                format='%d',
            ),
            "nombre_razon": st.column_config.TextColumn(
                "Nombre o Razon Social"
            ),
            "alias": st.column_config.TextColumn(
                "Alias"
            ),
            "related_user": st.column_config.TextColumn(
                "Cliente"
            ),
            "observaciones": st.column_config.TextColumn(
                "Observaciones"
            )
        }, column_order=['nombre_razon', 'alias', 'ruc', 'related_user', 'observaciones'])
    with tab2:
        st.dataframe(proveedores, height=300, hide_index=True)
    with tab3:
        st.dataframe(catalogo, height=300, hide_index=True)
    with tab4:
        st.dataframe(vehiculos, height=300, hide_index=True)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
