import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credenciales desde st.secrets
salessystem_user = st.secrets['DB_USERNAME_SS']
salessystem_token = st.secrets['DB_TOKEN_SS']
salessystem_database = st.secrets['DB_DATABASE_SS']
salessystem_source = st.secrets['DB_SOURCE_SS']
salessystem_port = st.secrets['DB_PORT_SS']
warehouse_user = st.secrets['DB_USERNAME_WH']
warehouse_token = st.secrets['DB_TOKEN_WH']
warehouse_database = st.secrets['DB_DATABASE_WH']
warehouse_source = st.secrets['DB_SOURCE_WH']
warehouse_port = st.secrets['DB_PORT_WH']

salessystem_url = f'mysql+pymysql://{salessystem_user}:{salessystem_token}@{salessystem_source}:{salessystem_port}/{salessystem_database}'
warehouse_url = f'postgresql://{warehouse_user}:{warehouse_token}@{warehouse_source}:{warehouse_port}/{warehouse_database}'

@st.cache_resource
def get_db_engine(db_type: str):
    """
    Crea y cachea el engine de SQLAlchemy.
    Args:
        db_type: 'salessystem' o 'warehouse'
    Returns:
        SQLAlchemy Engine
    """
    if db_type == 'salessystem':
        return create_engine(salessystem_url, connect_args={"connect_timeout": 5}, pool_pre_ping=True)
    elif db_type == 'warehouse':
        return create_engine(warehouse_url, connect_args={"connect_timeout": 5}, pool_pre_ping=True)
    else:
        raise ValueError(f"Tipo de base de datos desconocido: {db_type}")

# Instancias globales (ahora usan caché)
salessystem = get_db_engine('salessystem')
warehouse = get_db_engine('warehouse')

Session = sessionmaker(bind=salessystem)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError),
    reraise=True
)
def run_query(engine, query, parse_dates=None):
    """
    Ejecuta una consulta SQL de manera segura con reintentos.
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn, parse_dates=parse_dates)

def safe_query_execution(query_func, *args, **kwargs):
    """
    Wrapper para manejar excepciones finales y evitar crash de UI.
    """
    try:
        return query_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error ejecutando consulta: {e}")
        st.error("Error de conexión con la base de datos. Por favor intente nuevamente.")
        return pd.DataFrame()

# --- FUNCIONES DE CONSULTA CON CACHÉ DE DATOS ---

@st.cache_data(ttl=60, show_spinner=False)
def pedidos():
    query = "SELECT id, cod_pedido, fecha_pedido, periodo, (CASE WHEN customers.alias IS NULL THEN a.adquiriente ELSE customers.alias END) AS adquiriente, a.adquiriente AS ruc,importe_total, rubro, promedio_factura, contado_credito, bancariza, notas, estado, punto_entrega FROM pedidos AS a LEFT JOIN customers ON customers.ruc=a.adquiriente ORDER BY id"
    return safe_query_execution(run_query, salessystem, query)

@st.cache_data(ttl=60, show_spinner=False)
def cotizaciones():
    query = "SELECT * FROM facturas WHERE estado= IN ('PENDIENTE','EN PROCESO') ORDER BY emision"
    return safe_query_execution(run_query, salessystem, query)

def get_facturas_poremitir():
    """
    Obtiene y procesa las facturas por emitir.
    Reemplaza la lógica global que causaba ejecución prematura.
    """
    cotizaciones_poremitir = cotizaciones()

    if not cotizaciones_poremitir.empty:
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
        return facturas_poremitir
    else:
        return pd.DataFrame(columns=['cod_pedido', 'cuo', 'alias', 'emision', 'ruc', 'nombre_razon', 'moneda', 'total', 'forma_pago', 'observaciones', 'detraccion', 'retencion', 'estado'])

@st.cache_data(ttl=60, show_spinner=False)
def bancarizaciones():
    query = "SELECT * FROM v_bcp WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')"
    return safe_query_execution(run_query, salessystem, query)

@st.cache_data(ttl=300, show_spinner=False) # Cache más largo para catálogos que cambian poco
def adquirientes():
    query = "SELECT * FROM customers"
    return safe_query_execution(run_query, salessystem, query)

@st.cache_data(ttl=300, show_spinner=False)
def proveedores():
    query = "SELECT * FROM proveedores"
    return safe_query_execution(run_query, salessystem, query)

@st.cache_data(ttl=300, show_spinner=False)
def catalogo():
    query = "SELECT * FROM catalogo"
    return safe_query_execution(run_query, salessystem, query)

@st.cache_data(ttl=60, show_spinner=False)
def pre_detalle():
    query = "SELECT * FROM pre_detalle ORDER BY fecha_emision"
    return safe_query_execution(run_query, warehouse, query)

@st.cache_data(ttl=60, show_spinner=False)
def lista_facturas():
    query = "SELECT * FROM lista_facturas"
    return safe_query_execution(run_query, salessystem, query, parse_dates=['emision', 'vencimiento', 'vencimiento2', 'vencimiento3', 'vencimiento4'])

@st.cache_data(ttl=60, show_spinner=False)
def lista_guias():
    query = "SELECT * FROM lista_guias"
    return safe_query_execution(run_query, salessystem, query, parse_dates=['traslado'])
