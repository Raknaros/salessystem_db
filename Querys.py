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


def ejecutar_consulta(query, conexion, parse_dates=None):
    result = None
    while result is None:
        try:
            result = pd.read_sql(query, con=conexion, parse_dates=parse_dates)
        except Exception as e:
            st.warning(f"Error en la consulta: {e}. Reintentando...")
    return result


# Consultas específicas
def bancarizaciones():
    query = "SELECT * FROM v_bcp WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')"
    return ejecutar_consulta(query, salessystem)


def adquirientes():
    query = "SELECT * FROM customers"
    return ejecutar_consulta(query, salessystem)


def proveedores():
    query = "SELECT * FROM proveedores"
    return ejecutar_consulta(query, salessystem)


def catalogo():
    query = "SELECT * FROM catalogo"
    return ejecutar_consulta(query, salessystem)


def pre_detalle():
    query = "SELECT * FROM pre_detalle ORDER BY fecha_emision"
    return ejecutar_consulta(query, warehouse)


def lista_facturas():
    query = "SELECT * FROM lista_facturas"
    return ejecutar_consulta(query, salessystem,
                             parse_dates=['emision', 'vencimiento', 'vencimiento2', 'vencimiento3', 'vencimiento4'])


def lista_guias():
    query = "SELECT * FROM lista_guias"
    return ejecutar_consulta(query, salessystem, parse_dates=['traslado'])


def pedidos():
    query = "SELECT id, cod_pedido, fecha_pedido, periodo, (CASE WHEN customers.alias IS NULL THEN a.adquiriente ELSE customers.alias END) AS adquiriente, a.adquiriente AS ruc,importe_total, rubro, promedio_factura, contado_credito, bancariza, notas, estado, punto_entrega FROM pedidos AS a LEFT JOIN customers ON customers.ruc=a.adquiriente ORDER BY id"
    return ejecutar_consulta(query, salessystem)


def cotizaciones():
    query = "SELECT * FROM facturas"
    return ejecutar_consulta(query, salessystem)


# Inicialización de datos
def inicializar_datos():
    if 'bancarizaciones' not in st.session_state:
        st.session_state.bancarizaciones = bancarizaciones()
    if 'adquirientes' not in st.session_state:
        st.session_state.adquirientes = adquirientes()
    if 'proveedores' not in st.session_state:
        st.session_state.proveedores = proveedores()
    if 'catalogo' not in st.session_state:
        st.session_state.catalogo = catalogo()
    if 'pre_detalle' not in st.session_state:
        st.session_state.pre_detalle = pre_detalle()
    if 'lista_facturas' not in st.session_state:
        st.session_state.lista_facturas = lista_facturas()
    if 'lista_guias' not in st.session_state:
        st.session_state.lista_guias = lista_guias()
    if 'pedidos' not in st.session_state:
        st.session_state.pedidos = pedidos()
    if 'cotizaciones' not in st.session_state:
        st.session_state.cotizaciones = cotizaciones()


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
