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

col1.date_input('Fecha del pedido', help='Indicar la fecha en la que fue solicitado el pedido')
col2.text_input('Periodo', placeholder='202407',help='Indicar a que periodo corresponde el pedido')
col3.container(height=67, border=False).text_input('Adquiriente', placeholder='10999999203 o ALIAS', help='Indicar el ruc o el alias de la empresa a la '
                                                                       'que se le facturara')
col1.text_input('Total', placeholder='400000', help='Indicar total incluido igv del pedido')
col2.text_input('Rubro', placeholder='Ejemplos: MINERO, FERRETERO, EMBALAJE, DIVERSO', help='Indicar a que rubro o de '
                                                                                            'que categoria son los '
                                                                                            'articulos del pedido')
col3.container(height=100, border=False).text_input('Promedio', placeholder='Ejm: 12000 o 5000 o 2000', help='Total promedio por factura')
col1.text_input('llegada', placeholder='Ejm: DE.DEPOSITO 0014 o CAR.CENTRAL KM. 8.6 LIMA - LIMA - ATE',
                help='Indicar punto de llegada para consignar en las guias, ya sea direccion, o codigo de '
                     'establecimiento anexo')
col2.text_input('Tipo de pago', placeholder='Ejm: CONTADO o CREDITO MIN 3 DIAS',
                help='Indicar si el pago a consignar en las facturas sera al contado o a credito, si es credito indicar a cuantos dias')

col3.container(height=80, border=False).checkbox('Bancariza',
              help='Indicar si el cliente bancarizara sus facturas o no, si es no, lo bancarizamos nosotros')
#bancariza_container
col1.text_input('notas', placeholder='Notas', label_visibility='collapsed')


col2.file_uploader("ingresar_pedido_masivo", type=['xlsx'], help='SUBE TU ARCHIVO EXCEL PARA MULTIPLES INGRESOS')
col2.button("Subir")


