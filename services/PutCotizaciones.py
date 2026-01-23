import math

import pandas as pd
import os
from pathlib import Path

from openpyxl.reader.excel import load_workbook
from sqlalchemy import create_engine
import numpy as np

from models import Pedidos
from services.Querys import salessystem, Session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('future.no_silent_downcasting', True)


def load_cotizaciones(archivo):
    # Leer todas las hojas del Excel usando pandas
    # header=1 indica que la fila 2 (índice 1) contiene los encabezados
    # La fila 1 (índice 0) se ignora
    xls = pd.read_excel(archivo, sheet_name=None, header=1)
    
    dfs = []
    
    for sheet_name, df in xls.items():
        # Asignar el nombre de la hoja como cod_pedido
        df['cod_pedido'] = sheet_name
        
        # Eliminar columnas total y peso_total si existen
        cols_to_drop = [col for col in ['total', 'peso_total'] if col in df.columns]
        if cols_to_drop:
            df.drop(cols_to_drop, axis=1, inplace=True)
            
        # Filtrar filas donde 'cuo' no sea nulo
        if 'cuo' in df.columns and not df['cuo'].isnull().all():
             # Asegurarse de que solo tomamos filas válidas
             df = df.dropna(subset=['cuo'])
             dfs.append(df)
    
    if not dfs:
        return "No se encontraron datos válidos en el archivo."

    cotizaciones = pd.concat(dfs, ignore_index=True)

    # VERIFICAR CONSECUENCIA DE FECHAS DE VENCIMIENTO
    for index, value in cotizaciones['vencimiento4'].items():
        if pd.notnull(value) | pd.notna(value):
            if pd.isnull(cotizaciones.loc[index, 'vencimiento3']) | pd.isna(cotizaciones.loc[index, 'vencimiento3']):
                cotizaciones.loc[index, 'vencimiento3'] = cotizaciones.loc[index, 'vencimiento4']
                cotizaciones.loc[index, 'vencimiento4'] = pd.NaT
        elif pd.notnull(cotizaciones.loc[index, 'vencimiento3']) | pd.notna(cotizaciones.loc[index, 'vencimiento3']):
            if pd.isnull(cotizaciones.loc[index, 'vencimiento2']) | pd.isna(cotizaciones.loc[index, 'vencimiento2']):
                cotizaciones.loc[index, 'vencimiento2'] = cotizaciones.loc[index, 'vencimiento3']
                cotizaciones.loc[index, 'vencimiento3'] = pd.NaT
        elif pd.notnull(cotizaciones.loc[index, 'vencimiento2']) | pd.notna(cotizaciones.loc[index, 'vencimiento2']):
            if pd.isnull(cotizaciones.loc[index, 'vencimiento']) | pd.isna(cotizaciones.loc[index, 'vencimiento']):
                cotizaciones.loc[index, 'vencimiento'] = cotizaciones.loc[index, 'vencimiento2']
                cotizaciones.loc[index, 'vencimiento2'] = pd.NaT

    # Rellenar vacios en traslado con fecha de emision
    cotizaciones['traslado'] = cotizaciones['traslado'].infer_objects(copy=False).fillna(cotizaciones['emision'])

    # Cambiar datatype de las columnas de fecha a datetime con formato %Y-%m-%d
    cotizaciones[['emision', 'vencimiento', 'vencimiento2', 'vencimiento3', 'vencimiento4', 'traslado']] = cotizaciones[
        ['emision', 'vencimiento', 'vencimiento2', 'vencimiento3', 'vencimiento4', 'traslado']].apply(pd.to_datetime,
                                                                                                      format='%Y-%m-%d')

    # Cambiar nombre de columna lugar_entrega a llegada
    if 'lugar_entrega' in cotizaciones.columns:
        cotizaciones.rename(columns={'lugar_entrega': 'llegada'}, inplace=True)

    # Concatenar cod_pedido y cuo en columna cui
    cotizaciones['cui'] = cotizaciones['cod_pedido'].astype(str) + cotizaciones['cuo'].astype(str)

    # Definir columnas de texto
    str_columns = ['alias', 'moneda', 'descripcion', 'unid_medida', 'llegada', 'datos_adicionales',
                   'observaciones']

    # Definir columnas a formatear
    columns_to_round = ['precio_unit', 'cuota1', 'cuota2', 'cuota3', 'cuota4']

    # Aplica redondeo a cada columna en la lista
    for col in columns_to_round:
        if col in cotizaciones.columns:
            cotizaciones[col] = cotizaciones[col].apply(lambda x: round(x, 3) if pd.notna(x) else x)

    # Cambiar mayusculas y quitar espacios de los extremos a cada valor de cada columna de texto
    for column in str_columns:
        if column in cotizaciones.columns and cotizaciones[column].notna().any():
            cotizaciones[column] = cotizaciones[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)

    # Separar columnas de facturacion
    cols_facturas = ['cod_pedido', 'cuo', 'alias', 'emision', 'moneda', 'descripcion', 'unid_medida',
                             'cantidad', 'precio_unit', 'observaciones', 'vencimiento', 'cuota1',
                             'vencimiento2', 'cuota2', 'vencimiento3', 'cuota3', 'vencimiento4', 'cuota4']
    # Asegurar que existan las columnas antes de seleccionar
    cols_facturas = [c for c in cols_facturas if c in cotizaciones.columns]
    facturas = cotizaciones[cols_facturas]

    # Definir funcion de agrupamiento para las guias
    def columnas_guia(group):
        guia = group.iloc[0].copy()  # Tomar el primer valor de cada columna
        total_peso = (group['cantidad'] * group['peso_articulo']).sum()  # Sumar el producto de cantidad y peso
        guia['datos_adicionales'] = 'Peso: ' + str(
            math.ceil(total_peso))  # Actualizar el valor de 'peso' en el primer registro

        return guia

    # Separar columnas para la tabla remision_remitente, aplicar funcion de agrupamiento y retirar columnas sobrantes
    cols_remision = ['cui', 'cod_pedido', 'cuo', 'alias', 'traslado', 'llegada', 'cantidad',
                               'peso_articulo', 'placa', 'conductor',
                               'datos_adicionales', 'observaciones']
    cols_remision = [c for c in cols_remision if c in cotizaciones.columns]
    
    remision_remitente = (cotizaciones[cols_remision].groupby('cui').apply(columnas_guia, include_groups=False))
    
    if 'cantidad' in remision_remitente.columns:
        remision_remitente.drop(['cantidad'], axis=1, inplace=True)
    if 'peso_articulo' in remision_remitente.columns:
        remision_remitente.drop(['peso_articulo'], axis=1, inplace=True)

    session = Session()
    try:
        for cod_pedido in facturas['cod_pedido'].unique():
            pedido = session.query(Pedidos).filter(Pedidos.cod_pedido == cod_pedido)
            pedido.update({Pedidos.estado: 'EN PROCESO'})
        session.commit()
        
        facturas.to_sql('facturas', salessystem, if_exists='append', index=False)
        remision_remitente.to_sql('remision_remitente', salessystem, if_exists='append', index=False)
        return "Carga Exitosa"
    except Exception as e:
        session.rollback()
        return f"Error en la carga: {str(e)}"
    finally:
        session.close()
