import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep
from services.Querys import pedidos_pendientes

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:", layout="wide")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Some content')

container3 = st.container(height=300)
container3.dataframe(pedidos_pendientes, use_container_width=True)
st.header("Ingresar Pedido")
col1, col2, col3 = st.columns(3)

col1.date_input('Fecha del pedido')
col2.text_input('Periodo', placeholder='202407',help='Indicar a que periodo corresponde el pedido')
col3.text_input('Adquiriente', placeholder='10999999203 o ALIAS', help='Indicar el ruc o el alias de la empresa a la '
                                                                       'que se le facturara')
col1.text_input('Total', placeholder='400000', help='Indicar total incluido igv del pedido')
col2.text_input('Rubro', placeholder='Ejemplos: MINERO, FERRETERO, EMBALAJE, DIVERSO', help='Indicar a que rubro o de '
                                                                                            'que categoria son los '
                                                                                            'articulos del pedido')
col3.text_input('Promedio', placeholder='Promedio por factura', label_visibility='collapsed')
col1.text_input('llegada', placeholder='Punto de llegada para las guias', label_visibility='collapsed')
col2.text_input('contado_credito', placeholder='Contado o credito', label_visibility='collapsed')
col1.checkbox('Bancariza')
col3.text_input('notas', placeholder='Notas', label_visibility='collapsed')


col2.file_uploader("ingresar_pedido_masivo",type=['xlsx'], help='SUBE TU ARCHIVO EXCEL PARA MULTIPLES INGRESOS')
col2.button("Subir")


