import pandas as pd
from sqlalchemy import create_engine
import toml
import streamlit as st
import psycopg2
from sqlalchemy.orm import sessionmaker

salessystem_user = st.secrets['DB_USERNAME_SS']
salessystem_token = st.secrets['DB_TOKEN_SS']
salessystem_database = st.secrets['DB_DATABASE_SS']
salessystem_source = st.secrets['DB_SOURCE_SS']
warehouse_user = st.secrets['DB_USERNAME_WH']
warehouse_token = st.secrets['DB_TOKEN_WH']
warehouse_database = st.secrets['DB_DATABASE_WH']
warehouse_source = st.secrets['DB_SOURCE_WH']

salessystem_url = f'mysql+pymysql://{salessystem_user}:{salessystem_token}@{salessystem_source}:3306/{salessystem_database}'
warehouse_url = f'postgresql://{warehouse_user}:{warehouse_token}@{warehouse_source}:5432/{warehouse_database}'

salessystem = create_engine(salessystem_url, connect_args={"connect_timeout": 5})

warehouse = create_engine(warehouse_url, connect_args={"connect_timeout": 5})

Session = sessionmaker(bind=salessystem)

pedidos = pd.read_sql("SELECT * FROM pedidos",
                      salessystem)


def cargar_datos():
    # Función para cargar datos de la base de datos
    query = "SELECT id, cod_pedido, fecha_pedido, periodo, (CASE customers.alias WHEN null THEN adquiriente ELSE customers.alias END) AS adquiriente, importe_total, rubro, promedio_factura, contado_credito, bancariza, notas, estado, punto_entrega FROM pedidos AS a JOIN customers ON customers.ruc=a.adquiriente ORDER BY id"
    #REVISAR CONSULTA POR INDICES DUPLICADOS, O HACER RESET_INDEX(DROP=TRUE)
    return pd.read_sql(query, salessystem)


cotizaciones = pd.read_sql("SELECT * FROM facturas WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                           salessystem)

cotizaciones_poremitir = cotizaciones[~cotizaciones['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])]

facturas_poremitir = (cotizaciones_poremitir.groupby(['cod_pedido', 'cuo'])
                      .agg({
    'alias': 'first',
    'emision': 'first',
    'ruc': 'first',
    'nombre_razon': 'first',
    'moneda': 'first',
    'precio_unit': lambda x: (x * cotizaciones_poremitir.loc[x.index, 'cantidad']).sum() * 1.18,
    'forma_pago': 'first',
    'observaciones': 'first',
    'detraccion': 'first',
    'retencion': 'first',
    'estado': 'first'
}).reset_index())

# Renombramos la columna de precio_unit para que tenga el nombre correcto si es necesario
facturas_poremitir.rename(columns={'precio_unit': 'total'}, inplace=True)

# Ordenamos por 'cod_pedido' y 'cuo'
facturas_poremitir.sort_values(by=['cod_pedido', 'cuo'], inplace=True)

bancarizaciones = pd.read_sql("SELECT * FROM v_bcp WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                              salessystem)

adquirientes = pd.read_sql("SELECT * FROM customers", salessystem)

proveedores = pd.read_sql("SELECT * FROM proveedores", salessystem)

catalogo = pd.read_sql("SELECT * FROM catalogo", salessystem)

#vehiculos = pd.read_sql("SELECT * FROM vehiculos", salessystem)

pre_detalle = pd.read_sql('SELECT * FROM pre_detalle ORDER BY fecha_emision', warehouse)

detalle_completo = pd.merge(pre_detalle, catalogo, on='descripcion', how='left')
