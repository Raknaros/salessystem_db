import pandas as pd
import streamlit as st

from Querys import pedidos, adquirientes, pre_detalle, catalogo

passwords_to_hash = ['emisor2024', 'EvelynCBM1968', 'p259E9C695+']
#hashed_passwords = Hasher(passwords_to_hash).generate()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pedidos_extendido = pd.merge(pedidos, adquirientes[['ruc', 'alias']], left_on='adquiriente', right_on='ruc',
                              how='left')
pedidos_pendientes = pedidos_extendido[['cod_pedido', 'periodo','alias','contado_credito', 'importe_total', 'promedio_factura', 'notas', 'rubro', 'punto_entrega','ruc']].loc[pedidos_extendido['estado'] == 'PENDIENTE']
#['cod_pedido','periodo','importe_total', 'rubro', 'promedio_factura', 'contado_credito', 'notas', 'punto_entrega', 'alias']
#ruc_pedido = int(pedidos_pendientes[['ruc','cod_pedido']].loc[pedidos_pendientes['cod_pedido'] == 'I134DADE4']['ruc'].values.item())

detalle_completo = pd.merge(pre_detalle, catalogo, on='descripcion', how='left').dropna(how='all')

#detalle = detalle_completo.loc[detalle_completo['numero_documento'] == str(int(pedidos_pendientes[['ruc','cod_pedido']].loc[pedidos_pendientes['cod_pedido'] == 'I134DADE4']['ruc'].values.item()))].sort_values(by='fecha_emision', ascending=False).head(30)

print(detalle_completo.head(50))

with st.form(key='load_pedidos', border=False, clear_on_submit=True):
        row1 = st.columns(4)
        row2 = st.columns(4)
        row3 = st.columns(3)

        fecha_pedido = row1[0].date_input('Fecha del pedido', help='Indicar la fecha en la que fue solicitado el pedido')
        periodo = row1[1].text_input('Periodo', placeholder='Ejem: 202407 o 202309',
                                  help='Indicar a que periodo corresponde el pedido')
        adquiriente = row1[2].text_input('Adquiriente', placeholder='Ejem: 20131312955 o ALIAS',
                                      help='Indicar el ruc o el alias de la empresa a la que se le facturara')
        total = row1[3].text_input('Total', placeholder='Ejem: 400000', help='Indicar total incluido igv del pedido')
        rubro = row2[0].text_input('Rubro', placeholder='Ejem: MINERO, FERRETERO, EMBALAJE, DIVERSO',
                                help='Indicar a que rubro o de que categoria son los articulos del pedido')
        promedio = row2[1].text_input('Promedio', placeholder='Ejm: 12000 o 5000 o 2000', help='Total promedio por factura')
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
                               height=100, help='Indicar detalles adicionales o solicitudes puntuales del cliente')

        masivo = row3[1].file_uploader("Subir Masivo", type=['xlsx'],
                                    help='Subir archivo excel para ingreso de varios pedidos, si sube excel no ingresar '
                                         'otros datos.')
        submit = row3[2].form_submit_button('Subir')