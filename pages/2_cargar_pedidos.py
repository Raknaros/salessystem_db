import numpy as np
import pandas as pd
import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from time import sleep

from services.PutPedidos import put_pedidos
from services.Querys import pedidos, cargar_datos

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:", layout="wide")

if st.session_state["authentication_status"] is False or st.session_state["authentication_status"] is None:
    st.warning("Su sesión ha expirado. Redirigiendo a la página principal...")
    sleep(2)
    st.switch_page("home.py")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()


st.title('Pedidos por entregar')

if 'datos' not in st.session_state:
    st.session_state.datos = cargar_datos()


st.dataframe(st.session_state.datos[~st.session_state.datos['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])], height=300, hide_index=True,
             column_config={
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
                              'promedio_factura', 'contado_credito', 'notas', 'punto_entrega', 'estado', 'alias'])
st.header("Ingresar Pedido")

if 'datos' not in st.session_state:
    st.session_state.datos = cargar_datos()

with st.form(key='load_pedidos', border=False, clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    fecha_pedido = col1.date_input('Fecha del pedido', help='Indicar la fecha en la que fue solicitado el pedido')
    periodo = col2.text_input('Periodo', placeholder='Ejem: 202407 o 202309',
                              help='Indicar a que periodo corresponde el pedido')
    adquiriente = col3.text_input('Adquiriente', placeholder='Ejem: 20131312955 o ALIAS',
                                  help='Indicar el ruc o el alias de la empresa a la '
                                       'que se le facturara')
    total = col1.text_input('Total', placeholder='Ejem: 400000', help='Indicar total incluido igv del pedido')
    rubro = col2.text_input('Rubro', placeholder='Ejem: MINERO, FERRETERO, EMBALAJE, DIVERSO',
                            help='Indicar a que rubro o de '
                                 'que categoria son los '
                                 'articulos del pedido')
    promedio = col3.text_input('Promedio', placeholder='Ejm: 12000 o 5000 o 2000', help='Total promedio por factura')
    punto_llegada = col1.text_input('Punto de llegada',
                                    placeholder='Ejm: DE.DEPOSITO 0014 o CAR.CENTRAL KM. 8.6 LIMA - LIMA - ATE',
                                    help='Indicar punto de llegada para consignar en las guias, ya sea direccion, o codigo de '
                                         'establecimiento anexo')
    forma_pago = col2.container(height=97, border=False).text_input('Tipo de pago',
                                                                    placeholder='Ejm: CONTADO o CREDITO MIN 3 DIAS',
                                                                    help='Indicar si el pago a consignar en las facturas sera al '
                                                                         'contado o a credito, si es credito'
                                                                         'indicar a cuantos dias')

    notas = col3.text_area('Notas',
                           placeholder='Ejm: CLIENTE BANCARIZA, EVITAR PROVEEDORES A Y B, ENTREGAR MAXIMO EL DIA XX',
                           height=100, help='Indicar detalles adicionales o solicitudes puntuales del cliente')

    masivo = col1.file_uploader("Subir Masivo", type=['xlsx'],
                                help='Subir archivo excel para ingreso de varios pedidos, si sube excel no ingresar '
                                     'otros datos.')
    submit = col2.form_submit_button('Subir')

if submit:
    if masivo is not None:
        pedidos = pd.read_excel(masivo, sheet_name='pedidos', date_format='%d/%m/%Y',
                                dtype={'periodo': np.int32, 'adquiriente': object, 'importe_total': np.int64,
                                       'rubro': str,
                                       'promedio_factura': None, 'contado_credito': str,
                                       'punto_entrega': str, 'notas': str, 'estado': str},
                                parse_dates=[0, ],
                                na_values=' ', false_values=['no', 'NO', 'No'], true_values=['si', 'Si', 'SI'])

        str_columns = ['rubro', 'contado_credito', 'punto_entrega', 'notas', 'estado']
        for column in str_columns:
            if pedidos[column].notna().any():
                pedidos[column] = pedidos[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)
        pedidos.replace(np.nan, None, inplace=True)
        st.info(put_pedidos(pedidos.to_dict(orient='records')))

    else:
        data = [{
            "fecha_pedido": fecha_pedido,
            "periodo": periodo,
            "adquiriente": adquiriente,
            "importe_total": total,
            "rubro": rubro,
            "promedio_factura": promedio,
            "punto_llegada": punto_llegada,
            "forma_pago": forma_pago,
            "notas": notas,
        }, ]
        st.info(put_pedidos(data))

    sleep(2)
    st.session_state.datos = cargar_datos()
    st.rerun()
