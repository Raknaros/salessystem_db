import pandas as pd
from sqlalchemy import create_engine



salessystem = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                            ':3306/salessystem')

warehouse = create_engine('postgresql://admindb:72656770@datawarehouse.cgvmexzrrsgs.us-east-1.rds.amazonaws.com'
                          ':5432/warehouse')

pedidos = pd.read_sql("SELECT * FROM pedidos",
                      salessystem)

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
