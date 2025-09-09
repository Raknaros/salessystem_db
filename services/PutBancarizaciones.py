import pandas as pd
import os
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def put_bancarizaciones():
    pass
def load_bancarizar(ruta: str):
    engine = create_engine('mysql+pymysql://admin:Giu72656770@giumarchan.dev'
                           ':13306/salessystem')

    bancarizar = pd.read_excel(ruta + '/importar.xlsx', sheet_name='bancarizar', date_format='%d/%m/%Y',
                               parse_dates=[2, ], dtype={'observaciones': str}
                               , na_values=' ')

    str_columns = ['adquiriente', 'proveedor', 'documento_relacionado', 'observaciones']
    for column in str_columns:
        if bancarizar[column].notna().any():
            bancarizar[column] = bancarizar[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)

    return print(bancarizar.to_sql('v_bcp', engine, if_exists='append', index=False))


load_bancarizar('D:/OneDrive/facturacion')
