import pandas as pd
from datetime import date

from sqlalchemy import create_engine
import numpy as np

from services.Querys import salessystem, pedidos, adquirientes, pre_detalle, catalogo
from streamlit_authenticator.utilities.hasher import Hasher

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