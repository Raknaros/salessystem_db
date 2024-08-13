import streamlit as st

from services.Querys import cotizaciones_poremitir

st.set_page_config(page_title="Cotizaciones", page_icon=":material/edit:", layout="wide")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Cotizaciones')

st.dataframe(cotizaciones_poremitir, height=450, hide_index=True)

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

    pick_proveedores = col2.multiselect("proveedores", placeholder='Elige  los proveedores',
                                        options=["Green", "Yellow", "Red", "Blue"], label_visibility='collapsed')
    col2.button(label='Descagar')
elif option == "Pedido":

    pick_pedidos = col2.multiselect("pedidos", placeholder='Elige  los pedidos',
                                    options=["Green", "Yellow", "Red", "Blue"], label_visibility='collapsed')
    col2.button(label='Descagar')

col3.subheader('Subir Cotizaciones Emitidas')

col3.file_uploader("Subir Cotizaciones Emitidas", type=['xlsx'],
                   help='Subir archivo excel de Cuadro para Emitir ya realizado y con numero de guia y factura colocada',
                   label_visibility='collapsed')
col3.button(label='Subir',key='subir_cotizaciones_emitidas')
