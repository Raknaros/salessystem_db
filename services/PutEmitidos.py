import pandas as pd
import numpy as np
from Querys import salessystem

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def put_emitidos(dataframe: pd.DataFrame):
    """
    Loads a DataFrame with 'pedidos' data into the pedidos table.
    The DataFrame should be pre-processed and cleaned.
    """
    str_columns = ['rubro', 'contado_credito', 'punto_entrega', 'notas', 'estado']
    for column in str_columns:
        if column in dataframe.columns and dataframe[column].notna().any():
            dataframe[column] = dataframe[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)

    # Use the imported engine
    dataframe.to_sql('pedidos', salessystem, if_exists='append', index=False)
    return f"Se cargaron {len(dataframe)} registros de emitidos."

