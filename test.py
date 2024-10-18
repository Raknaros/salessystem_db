import numpy as np

from models import *
from sqlalchemy import create_engine
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

from services.PutPedidos import put_pedidos
from services.Querys import cargar_datos

passwords_to_hash = ['emisor2024', 'EvelynCBM1968', 'p259E9C695+']
#hashed_passwords = Hasher(passwords_to_hash).generate()



pedidos = pd.read_excel('D:/OneDrive/facturacion/importar.xlsx', sheet_name='pedidos', date_format='%d/%m/%Y',
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


datos=cargar_datos()


duplicados_filas = datos.duplicated()
print("Filas duplicadas:", duplicados_filas.sum())