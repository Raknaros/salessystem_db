import pandas as pd
from Querys import salessystem

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def put_bancarizaciones():
    pass


def load_bancarizar(dataframe: pd.DataFrame):
    """
    Loads a DataFrame with 'bancarizar' data into the v_bcp table.
    The DataFrame should be pre-processed and cleaned.
    """

    str_columns = ['adquiriente', 'proveedor', 'documento_relacionado', 'observaciones']
    for column in str_columns:
        if column in dataframe.columns and dataframe[column].notna().any():
            dataframe[column] = dataframe[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)

    # Use the imported engine
    dataframe.to_sql('v_bcp', salessystem, if_exists='append', index=False)
    return f"Se cargaron {len(dataframe)} registros de bancarización."

