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


def pedidos():
    result = None
    while result is None:
        try:
            query = "SELECT id, cod_pedido, fecha_pedido, periodo, (CASE WHEN customers.alias IS NULL THEN a.adquiriente ELSE customers.alias END) AS adquiriente, a.adquiriente AS ruc,importe_total, rubro, promedio_factura, contado_credito, bancariza, notas, estado, punto_entrega FROM pedidos AS a LEFT JOIN customers ON customers.ruc=a.adquiriente ORDER BY id"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


def cotizaciones():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM facturas"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


cotizaciones_poremitir = cotizaciones()

cotizaciones_poremitir = cotizaciones_poremitir[
    ~cotizaciones_poremitir['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])]

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


def bancarizaciones():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM v_bcp WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


def adquirientes():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM customers"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


def proveedores():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM proveedores"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


def catalogo():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM catalogo"
            result = pd.read_sql(query, salessystem)
        except Exception as e:
            pass
    return result


#vehiculos = pd.read_sql("SELECT * FROM vehiculos", salessystem)

def pre_detalle():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM pre_detalle ORDER BY fecha_emision"
            result = pd.read_sql(query, warehouse)
        except Exception as e:
            pass
    return result


def lista_facturas():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM lista_facturas"
            result = pd.read_sql(query, con=salessystem,
                                 parse_dates=['emision', 'vencimiento', 'vencimiento2', 'vencimiento3', 'vencimiento4'])
        except Exception as e:
            pass
    return result


def lista_guias():
    result = None
    while result is None:
        try:
            query = "SELECT * FROM lista_guias"
            result = pd.read_sql(query, con=salessystem, parse_dates=['traslado'])
        except Exception as e:
            pass
    return result
