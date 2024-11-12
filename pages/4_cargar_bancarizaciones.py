import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from time import sleep

from services.Querys import bancarizaciones

st.set_page_config(page_title="Bancarizaciones", page_icon=":material/edit:", layout="wide")

st.session_state.sidebar()

st.title('Bancarizaciones')

st.dataframe(bancarizaciones[~bancarizaciones['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])], height=300, hide_index=True, column_config={
            "fecha_operacion": st.column_config.DateColumn(
                "Fecha de operacion",
                help="Fecha de la bancarizacion",
                format='DD/MM/YYYY'
            ),
            "hora_operacion": st.column_config.DatetimeColumn(
                "Hora de operacion",
                help="Hora de la bancarizacion",
                format='HH:MM:SS'
            ),
            "numero_operacion": st.column_config.NumberColumn(
                "Numero de operacion",
                format='%d',
            ),
            "importe": st.column_config.NumberColumn(
                "Importe",
                help="Total a bancarizar",
                format='%d',
            ),
            "adquiriente": st.column_config.TextColumn(
                "Adquiriente",
                width='medium'
            ),
            "proveedor": st.column_config.TextColumn(
                "Proveedor",
                help="A que rubro o de que categoria son los articulos del pedido",
                width='medium'
            ),
            "documento_relacionado": st.column_config.TextColumn(
                "Factura",
                help="Total promedio o maximo por factura"
            ),
            "observaciones": st.column_config.TextColumn(
                "Observaciones",
                help="Forma de pago, al contado o a credito cuantos dias",
                width='medium'
            ),
            "estado": st.column_config.TextColumn(
                "Estado"
            )
        }, column_order=['fecha_operacion', 'hora_operacion', 'numero_operacion', 'importe', 'adquiriente', 'proveedor',
                         'documento_relacionado', 'observaciones', 'estado'])
st.header("Ingresar Bancarizaciones")

with st.form(key='load_pedidos', border=False):
    col1, col2, col3 = st.columns(3)

    adquiriente = col1.text_input('Adquiriente', placeholder='Ejem: 20131312955 o ALIAS',
                    help='Indicar a que adquiriente corresponde la factura')
    proveedor = col2.text_input('Proveedor', placeholder='Ejem: 20131312955 o ALIAS',
                    help='Indicar que proveedor emite la factura')

    fecha_operacion = col3.date_input('Fecha de Operacion', help='Indicar la fecha en la que se debe bancarizar')

    importe = col1.text_input('Importe', placeholder='Ejm: 12000 o 5000 o 2000',
                    help='Indicar total de la factura')

    doc_relacionado = col2.container(height=97, border=False).text_input('Documento relacionado',
                                                       placeholder='Ejem: E001-5982 o 0001-923',
                                                       help='Indicar a que factura corresponde la bancarizacion')
    observaciones = col3.text_input('Observaciones', placeholder='Ejem: HORA ENTRE LAS 3 Y LAS 5 o ANTES DE LAS 10AM',
                    help='Indicar si tiene alguna observacion en especial')

    masivo = col1.file_uploader("Subir Masivo", type=['xlsx'],
                       help='Subir archivo excel para ingreso de varias bancarizaciones, si sube excel no ingresar '
                            'otros datos.')
    submit = col2.form_submit_button('Subir')

    if submit:
        if masivo is not None:
            pedidos_masivo = pd.read_excel(masivo, sheet_name='bancarizar', date_format='%d/%m/%Y',
                          parse_dates=[2, ], dtype={'observaciones': str}
                          , na_values=' ')
            st.write(pedidos_masivo)

        else:
            st.write(adquiriente)
            st.write(proveedor)
            st.write(fecha_operacion)
            st.write(importe)
            st.write(doc_relacionado)
            st.write(observaciones)
