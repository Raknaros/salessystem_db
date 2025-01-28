from datetime import date
from time import sleep

import streamlit as st

from services.GetEmitir import get_emitir, update_enproceso
from services.PutCotizaciones import load_cotizaciones
from Querys import facturas_poremitir, lista_facturas, cotizaciones

st.set_page_config(page_title="Cotizaciones", page_icon=":material/edit:", layout="wide")

if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False

if st.session_state.get("authentication_status"):
    st.session_state.sidebar()
    st.session_state['authenticator'].logout(location='sidebar', button_name='Cerrar Sesion')
    st.title('Cotizaciones')


    def actualizar_cargar_cotizaciones():
        st.session_state.lista_facturas = lista_facturas()
        st.session_state.cotizaciones = cotizaciones()
        sleep(2)
        st.rerun()


    st.dataframe(facturas_poremitir, height=450, hide_index=True, column_config={
        "Codigo de Pedido": st.column_config.TextColumn(
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

    cotizaciones_masivo = col1.file_uploader("Subir Cotizaciones", type=['xlsx'],
                                             help='Subir archivo excel de cotizaciones(pre-cuadro) ya elaborado segun el pedido',
                                             label_visibility='collapsed')
    subir_cotizaciones = col1.button(label='Subir', key='subir_cotizaciones', on_click=load_cotizaciones,
                                     args=(cotizaciones_masivo,))

    if subir_cotizaciones:
        sleep(2)
        st.session_state.cotizaciones = cotizaciones()
        st.rerun()

    col2.subheader('Descargar Cuadro para Emitir')

    option = col2.selectbox(
        "descargar_pedidos",
        ("Proveedor", "Pedido"),
        index=None,
        placeholder="Descargar por", label_visibility='collapsed'
    )
    #fecha_final = datetime.now() - timedelta(days=4)
    if option == "Proveedor":

        #    subcol1, subcol2 = col2.container().columns(2)

        fecha_final = col2.date_input(
            'Fecha',
            help='Indicar hasta que fecha desea solicitar las emisiones del proveedor (ejem. desde hace dos dias hasta la '
                 'fecha escogida)')

        pick_proveedores = col2.multiselect("proveedores", placeholder='Elige  los proveedores',
                                            options=st.session_state.lista_facturas['alias'].unique().tolist(),
                                            label_visibility='collapsed')
        if col2.download_button(
                label='Generar',
                data=get_emitir(fecha=fecha_final, proveedores=pick_proveedores),
                file_name='emitir_' + date.today().strftime('%Y%m%d') + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ):
            st.session_state.download_clicked = True
        if st.session_state.download_clicked:
            update_enproceso(proveedores=pick_proveedores, fecha=fecha_final)
        # Reiniciar el estado para evitar ejecuciones múltiples
            st.session_state.download_clicked = False

    elif option == "Pedido":

        pick_pedidos = col2.multiselect("pedidos", placeholder='Elige  los pedidos',
                                        options=st.session_state.lista_facturas['cod_pedido'].unique().tolist(), label_visibility='collapsed')

        if col2.download_button(
                label='Generar',
                data=get_emitir(pedidos=pick_pedidos),
                file_name='emitir_' + date.today().strftime('%Y%m%d') + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ):
            st.session_state.download_clicked = True

        if st.session_state.download_clicked:
            update_enproceso(pedidos=pick_pedidos)
        # Reiniciar el estado para evitar ejecuciones múltiples
            st.session_state.download_clicked = False

    col3.subheader('Subir Cotizaciones Emitidas')

    col3.file_uploader("Subir Facturas Emitidas", type=['xlsx'],
                       help='Subir archivo excel de Cuadro para Emitir ya realizado y con numero de guia y factura colocada',
                       label_visibility='collapsed', disabled=True)
    col3.button(label='Subir', key='subir_cotizaciones_emitidas')

else:
    st.error("Por favor inicia sesion para continuar...")
    sleep(2)
    st.switch_page("app.py")
