import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep
from services.Querys import pedidos_porentregar

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:", layout="wide")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Pedidos por entregar')

st.dataframe(pedidos_porentregar, height=300, hide_index=True, column_config={
            "tipo_proveedor": st.column_config.NumberColumn(
                "Tipo",
                help="Diferenciacion de los proveedores",
                format='%d',
            ),
            "numero_documento": st.column_config.NumberColumn(
                "RUC",
                format='%d'
            ),
            "nombre_razon": st.column_config.TextColumn(
                "Nombre o Razon Social"
            ),
            "alias": st.column_config.TextColumn(
                "Alias"
            ),
            "estado": st.column_config.TextColumn(
                "Estado"
            ),
            "observaciones": st.column_config.TextColumn(
                "Observaciones"
            ),
            "actividad_economica": st.column_config.TextColumn(
                "Actividad Economica"
            ),
            "act_econ_sec_1": st.column_config.TextColumn(
                "Act. Econ. Secundaria 1"
            ),
            "act_econ_sec_2": st.column_config.TextColumn(
                "Act. Econ. Secundaria 2"
            )
        }, column_order=['tipo_proveedor', 'numero_documento', 'nombre_razon', 'alias', 'estado', 'observaciones',
                         'actividad_economica', 'act_econ_sec_1', 'act_econ_sec_2'])
st.header("Ingresar Pedido")

with st.form(key='load_pedidos', border=False):
    col1, col2, col3 = st.columns(3)

    col1.date_input('Fecha del pedido', help='Indicar la fecha en la que fue solicitado el pedido')
    col2.text_input('Periodo', placeholder='Ejem: 202407 o 202309', help='Indicar a que periodo corresponde el pedido')
    col3.text_input('Adquiriente', placeholder='Ejem: 20131312955 o ALIAS',
                    help='Indicar el ruc o el alias de la empresa a la '
                         'que se le facturara')
    col1.text_input('Total', placeholder='Ejem: 400000', help='Indicar total incluido igv del pedido')
    col2.text_input('Rubro', placeholder='Ejem: MINERO, FERRETERO, EMBALAJE, DIVERSO', help='Indicar a que rubro o de '
                                                                                            'que categoria son los '
                                                                                            'articulos del pedido')
    col3.text_input('Promedio', placeholder='Ejm: 12000 o 5000 o 2000', help='Total promedio por factura')
    col1.text_input('Punto de llegada', placeholder='Ejm: DE.DEPOSITO 0014 o CAR.CENTRAL KM. 8.6 LIMA - LIMA - ATE',
                    help='Indicar punto de llegada para consignar en las guias, ya sea direccion, o codigo de '
                         'establecimiento anexo')
    col2.container(height=97, border=False).text_input('Tipo de pago', placeholder='Ejm: CONTADO o CREDITO MIN 3 DIAS',
                                                       help='Indicar si el pago a consignar en las facturas sera al '
                                                            'contado o a credito, si es credito'
                                                            'indicar a cuantos dias')

    col3.text_area('Notas', placeholder='Ejm: CLIENTE BANCARIZA, EVITAR PROVEEDORES A Y B, ENTREGAR MAXIMO EL DIA XX',
                   height=100, help='Indicar detalles adicionales o solicitudes puntuales del cliente')

    col1.file_uploader("Subir Masivo", type=['xlsx'],
                       help='Subir archivo excel para ingreso de varios pedidos, si sube excel no ingresar otros datos.')
    col2.form_submit_button('Subir')
