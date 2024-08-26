import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep
from services.Querys import pedidos

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:", layout="wide")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Pedidos por entregar')

st.dataframe(pedidos[~pedidos['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])], height=300, hide_index=True, column_config={
            "cod_pedido": st.column_config.TextColumn(
                "Codigo de Pedido",
                help="Codigo unico de pedido"
            ),
            "fecha_pedido": st.column_config.DateColumn(
                "Fecha de Pedido",
                help="Fecha en la cual se solicita el pedido",
                format='DD/MM/YYYY'
            ),
            "periodo": st.column_config.NumberColumn(
                "Periodo",
                help="Periodo al que corresponde el pedido, por ejemplo facturas de diciembre del 2020 seria 202012",
                format='%d',
            ),
            "adquiriente": st.column_config.TextColumn(
                "Adquiriente",
                help="Alias o RUC del adquiriente o del receptor de las facturas"
            ),
            "importe_total": st.column_config.NumberColumn(
                "Total",
                help="Total del pedido incluido IGV",
                format='%d',
            ),
            "rubro": st.column_config.TextColumn(
                "Rubro",
                help="A que rubro o de que categoria son los articulos del pedido",
                width='medium'
            ),
            "promedio_factura": st.column_config.NumberColumn(
                "Promedio",
                help="Total promedio o maximo por factura",
                format='%d',
            ),
            "contado_credito": st.column_config.TextColumn(
                "Forma de pago",
                help="Forma de pago, al contado o a credito cuantos dias",
                width='medium'
            ),
            "notas": st.column_config.TextColumn(
                "Notas",
                help="Informacion adicional especifica del pedido",
                width='medium'
            ),
            "punto_entrega": st.column_config.TextColumn(
                "Direccion de Llegada",
                help="Direccion a consignar en las guias",
                width='medium'
            ),
            "estado": st.column_config.TextColumn(
                "Estado"
            )
        }, column_order=['cod_pedido', 'fecha_pedido', 'periodo', 'adquiriente', 'importe_total', 'rubro',
                         'promedio_factura', 'contado_credito', 'notas', 'punto_entrega', 'estado'])
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
