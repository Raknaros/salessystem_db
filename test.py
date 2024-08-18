from models import *
from sqlalchemy import create_engine
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

passwords_to_hash = ['emisor2024','EvelynCBM1968', 'p259E9C695+']
hashed_passwords = Hasher(passwords_to_hash).generate()

salessystem = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                            ':3306/salessystem')

cotizaciones_poremitir = pd.read_sql("SELECT * FROM facturas WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                                        salessystem)

result = (cotizaciones_poremitir.groupby(['cod_pedido', 'cuo'])
          .agg({
              'alias': 'first',
              'emision': 'first',
              'ruc': 'first',
              'nombre_razon': 'first',
              'moneda': 'first',
              'precio_unit': lambda x: (x * cotizaciones_poremitir.loc[x.index, 'cantidad']).sum() * 1.18,
              'observaciones': 'first',
              'detraccion': 'first',
              'retencion': 'first',
              'estado': 'first'
          })
          .reset_index())

# Renombramos la columna de precio_unit para que tenga el nombre correcto si es necesario
result.rename(columns={'precio_unit': 'total_con_iva'}, inplace=True)

# Ordenamos por 'cod_pedido' y 'cuo'
result.sort_values(by=['cod_pedido', 'cuo'], inplace=True)

print(result)