import pandas as pd
from sqlalchemy import create_engine

salessystem = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                            ':3306/salessystem')

warehouse = create_engine('postgresql://admindb:72656770@datawarehouse.cgvmexzrrsgs.us-east-1.rds.amazonaws.com'
                          ':5432/warehouse')

pedidos_porentregar = pd.read_sql("SELECT * FROM pedidos WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADO')",
                                  salessystem)

#df[~df['estado'].isin(['TERMINADO', 'ENTREGADO', 'ANULADO'])]

cotizaciones_poremitir = pd.read_sql("SELECT * FROM facturas WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                                        salessystem)

bancarizaciones_poremitir = pd.read_sql("SELECT * FROM v_bcp WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                                        salessystem)

adquirientes = pd.read_sql("SELECT * FROM customers", salessystem)

proveedores = pd.read_sql("SELECT * FROM proveedores", salessystem)

catalogo = pd.read_sql("SELECT * FROM catalogo", salessystem)

#vehiculos = pd.read_sql("SELECT * FROM vehiculos", salessystem)

