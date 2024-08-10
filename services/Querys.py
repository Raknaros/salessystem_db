import pandas as pd
from sqlalchemy import create_engine

salessystem = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                            ':3306/salessystem')

warehouse = create_engine('postgresql://admindb:72656770@datawarehouse.cgvmexzrrsgs.us-east-1.rds.amazonaws.com'
                          ':5432/warehouse')

pedidos_pendientes = pd.read_sql("SELECT * FROM pedidos WHERE estado='PENDIENTE'", salessystem)
