from time import sleep

import streamlit as st

from services.Querys import facturas_poremitir

st.set_page_config(page_title="Cotizaciones", page_icon=":material/edit:", layout="wide")

if 'session_token' not in st.session_state:
    # Redirigir a la página principal
    st.warning("Su sesión ha expirado. Redirigiendo a la página principal...")
    sleep(2)
    st.switch_page("home.py")


if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Cotizaciones')

st.dataframe(facturas_poremitir, height=450, hide_index=True, column_config={
    "cod_pedido": st.column_config.TextColumn(
        "Codigo de Pedido",
        help="Codigo unico del pedido al que corresponde esta factura"
    ),
    "cuo": st.column_config.NumberColumn(
        "CUO",
        help="Codigo unico de la operacion, dentro del codigo de pedido",
        format="%d",
    ),
    "alias": st.column_config.TextColumn(
        "Alias",
    ),
    "emision": st.column_config.DateColumn(
        "Fecha de Emision",
        help="Total a bancarizar",
        format='DD/MM/YYYY',
    ),
    "ruc": st.column_config.NumberColumn(
        "RUC",
        format="%d",
    ),
    "nombre_razon": st.column_config.TextColumn(
        "Nombre o Razon Social",
        width='medium'
    ),
    "moneda": st.column_config.TextColumn(
        "Moneda",
        help="Tipo de moneda de la factura"
    ),
    "total": st.column_config.NumberColumn(
        "Total",
        help="Total incluido IGV",
        format="S/. %.2f",
        width='small'
    ),
    "forma_pago": st.column_config.TextColumn(
        "Forma de Pago",
        help="Forma de pago a consignar en la factura"
    ),
    "detraccion": st.column_config.TextColumn(
        "Detraccion",
        help="Codigo de detraccion correspondiente"
    ),
    "retencion": st.column_config.TextColumn(
        "Retencion",
        help="Porcentaje de retencion correspondiente"
    ),
    "observaciones": st.column_config.TextColumn(
        "Observaciones",
        width='medium'
    ),
    "estado": st.column_config.TextColumn(
        "Estado",
        width='medium'
    )
}, column_order=['cod_pedido', 'cuo', 'alias', 'emision', 'ruc', 'nombre_razon',
                 'moneda', 'total', 'forma_pago', 'detraccion', 'retencion', 'observaciones', 'estado'])

col1, col2, col3 = st.columns(3)

col1.subheader('Subir Cotizaciones')

col1.file_uploader("Subir Cotizaciones", type=['xlsx'],
                   help='Subir archivo excel de cotizaciones(pre-cuadro) ya elaborado segun el pedido',
                   label_visibility='collapsed')
col1.button(label='Subir', key='subir_cotizaciones')

col2.subheader('Descargar Cuadro para Emitir')

option = col2.selectbox(
    "descargar_pedidos",
    ("Proveedor", "Pedido"),
    index=None,
    placeholder="Descargar por", label_visibility='collapsed'
)

if option == "Proveedor":

    subcol1, subcol2 = col2.container().columns(2)
    fecha_inicio = subcol1.date_input(
        'Fecha Inicial',
        help='Indicar desde que fecha desea descargar (maximo 2 dias anteriores al dia de hoy)')
    fecha_final = subcol2.date_input(
        'Fecha Final',
        help='Indicar desde que fecha desea descargar (maximo 1 dia posterior al dia de hoy)')

    pick_proveedores = col2.multiselect("proveedores", placeholder='Elige  los proveedores',
                                        options=["Green", "Yellow", "Red", "Blue"], label_visibility='collapsed')
    col2.button(label='Descagar')
elif option == "Pedido":

    pick_pedidos = col2.multiselect("pedidos", placeholder='Elige  los pedidos',
                                    options=["Green", "Yellow", "Red", "Blue"], label_visibility='collapsed')
    col2.button(label='Descagar')
"""
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df(my_large_df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="large_df.csv",
    mime="text/csv",
)"""

col3.subheader('Subir Cotizaciones Emitidas')

col3.file_uploader("Subir Facturas Emitidas", type=['xlsx'],
                   help='Subir archivo excel de Cuadro para Emitir ya realizado y con numero de guia y factura colocada',
                   label_visibility='collapsed')
col3.button(label='Subir', key='subir_cotizaciones_emitidas')
