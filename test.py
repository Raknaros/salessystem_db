from models import *
from sqlalchemy import create_engine
import pandas as pd


session = Session()
# Realizar la consulta
consulta = session.query(Facturas).filter(Facturas.estado == 'POR EMITIR')

# Convertir la consulta a un DataFrame
df = pd.read_sql_query(consulta.statement, session.bind)
df2 = pd.DataFrame(session.execute(consulta.statement).fetchall())

print(df2.head())
