from datetime import date

import numpy as np
import pandas as pd
import streamlit as st
from time import sleep

from services.PutPedidos import put_pedidos
from services.GetPrecuadro import get_precuadros
import Querys

st.set_page_config(page_title="Pedidos", page_icon=":material/edit:", layout="wide")

if st.session_state.get("authentication_status"):
    st.session_state.sidebar()
    st.session_state['authenticator'].logout(location='sidebar', button_name='Cerrar Sesion')
    st.title('Pedidos por entregar')

    st.dataframe(st.session_state.pedidos[st.session_state.pedidos['estado'].isin(['EN PROCESO', 'PENDIENTE'])],
                 height=300, hide_index=True,
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
                         help="Periodo al que corresponde el pedido, por ejemplo facturas de diciembre del 2020 seria "
                              "202012",
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

    with st.form(key='load_pedidos', border=False, clear_on_submit=True):

        row1 = st.columns(4)
        row2 = st.columns(4)
        row3 = st.columns(3, vertical_alignment="center")

        row4 = st.container(height=50, border=False)

        fecha_pedido = row1[0].date_input('Fecha del pedido',
                                          help='Indicar la fecha en la que fue solicitado el pedido')
        periodo = row1[1].text_input('Periodo', placeholder='Ejem: 202407 o 202309',
                                     help='Indicar a que periodo corresponde el pedido')
        adquiriente = row1[2].text_input('Adquiriente', placeholder='Ejem: 20131312955 o ALIAS',
                                         help='Indicar el ruc o el alias de la empresa a la que se le facturara')
        total = row1[3].text_input('Total', placeholder='Ejem: 400000', help='Indicar total incluido igv del pedido')
        rubro = row2[0].text_input('Rubro', placeholder='Ejem: MINERO, FERRETERO, EMBALAJE, DIVERSO',
                                   help='Indicar a que rubro o de que categoria son los articulos del pedido')
        promedio = row2[1].text_input('Promedio', placeholder='Ejm: 12000 o 5000 o 2000',
                                      help='Total promedio por factura')
        punto_llegada = row2[2].text_input('Punto de llegada',
                                           placeholder='Ejm: DE.DEPOSITO 0014 o CAR.CENTRAL KM. 8.6 LIMA - LIMA - ATE',
                                           help='Indicar punto de llegada para consignar en las guias, ya sea direccion, '
                                                'o codigo de establecimiento anexo')
        forma_pago = row2[3].container(height=97, border=False).text_input('Tipo de pago',
                                                                           placeholder='Ejm: CONTADO o CREDITO MIN 3 DIAS',
                                                                           help='Indicar si el pago a consignar en las '
                                                                                'facturas sera al contado o a credito, si es '
                                                                                'credito indicar a cuantos dias')

        notas = row3[0].text_area('Notas',
                                  placeholder='Ejm: CLIENTE BANCARIZA, EVITAR PROVEEDORES A Y B, ENTREGAR MAXIMO EL DIA XX',
                                  height=75, help='Indicar detalles adicionales o solicitudes puntuales del cliente')

        masivo = row3[1].file_uploader("Subir Masivo", type=['xlsx'],
                                       help='Subir archivo excel para ingreso de varios pedidos, si sube excel no ingresar '
                                            'otros datos.')

        submit = row3[2].form_submit_button('Subir')

    col1, col2, col3 = st.columns(3)

    with col1.container(key='precuadro', height=200, border=False):
        st.subheader("Generar Pre-cuadro")
        ped_seleccionados = st.multiselect("pedidos_precuadro", placeholder='Elige los pedidos',
                                           options=
                                           st.session_state.pedidos.loc[
                                               st.session_state.pedidos['estado'] == 'PENDIENTE'][
                                               'adquiriente'].tolist(), label_visibility='collapsed')

        st.download_button(
            label='Generar',
            data=get_precuadros(ped_seleccionados=ped_seleccionados),
            file_name='precuadro' + date.today().strftime('%Y%m%d') + '.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        #DOWNLOAD BUTTON EJECUTA LA CARGA DE DATA CADA QUE CAMBIE LOS PARAMETROS, ARRANCANDO VACIO

    if submit:
        if masivo is not None:
            pedidos = pd.read_excel(masivo, sheet_name='pedidos', date_format='%d/%m/%Y',
                                    dtype={'periodo': np.int32, 'adquiriente': object, 'importe_total': np.int64,
                                           'rubro': str,
                                           'promedio_factura': None, 'contado_credito': str,
                                           'punto_llegada': str, 'notas': str, 'estado': str},
                                    parse_dates=[0, ],
                                    na_values=' ', false_values=['no', 'NO', 'No'], true_values=['si', 'Si', 'SI'])

            str_columns = ['rubro', 'contado_credito', 'punto_llegada', 'notas', 'estado']
            for column in str_columns:
                if pedidos[column].notna().any():
                    pedidos[column] = pedidos[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)
            pedidos.replace(np.nan, None, inplace=True)
            st.success(put_pedidos(pedidos.to_dict(orient='records')))
            sleep(2)
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
            st.success(put_pedidos(data))
            sleep(2)

        st.session_state.pedidos = Querys.pedidos()
        st.rerun()


else:
    st.error("Por favor inicia sesion para continuar...")
    sleep(2)
    st.switch_page("app.py")

#TODO AGREGAR BOTON PARA DESCARGAR PRE CUADRO
