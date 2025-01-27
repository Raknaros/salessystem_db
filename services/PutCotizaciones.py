import math

import pandas as pd

from openpyxl.reader.excel import load_workbook

from models import Pedidos
from Querys import salessystem, Session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('future.no_silent_downcasting', True)


def load_cotizaciones(archivo):
    workbook = load_workbook(archivo)
    # Crear dataframe Cotizaciones
    cotizaciones = pd.DataFrame(
        columns=['cuo', 'alias', 'emision', 'descripcion', 'cantidad', 'precio_unit', 'total', 'peso_articulo',
                 'peso_total', 'observaciones', 'vencimiento', 'cuota1', 'vencimiento2', 'cuota2', 'vencimiento3',
                 'cuota3', 'vencimiento4', 'cuota4', 'moneda', 'unid_medida', 'traslado', 'lugar_entrega', 'placa',
                 'conductor', 'datos_adicionales'])

    # Iterar sobre todas las hojas del libro
    for sheet_name in workbook.sheetnames:
        # Seleccionar la hoja actual
        sheet = workbook[sheet_name]

        # Recuperar la primera fila
        pedido = sheet['A1'].value

        # Crear una lista de listas con el resto del contenido de la hoja
        resto_filas = [[cell.value for cell in row[:25]] for row in sheet.iter_rows(min_row=2)]

        # Convertir el resto del contenido en un DataFrame
        df = pd.DataFrame(resto_filas[1:], columns=resto_filas[0])

        # Agregar cod_pedido de la celda A1
        df['cod_pedido'] = pedido

        # Eliminar columnas total y peso_total
        df.drop(['total', 'peso_total'], axis=1, inplace=True)

        # Unir verticalmente al dataframe cotizaciones solo si ningun valor de la columna cuo es nulo
        if not df['cuo'].isnull().any():
            cotizaciones = pd.concat([cotizaciones, df], ignore_index=True, axis=0)

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
    cotizaciones.rename(columns={'lugar_entrega': 'llegada'}, inplace=True)

    # Concatenar cod_pedido y cuo en columna cui
    cotizaciones['cui'] = cotizaciones['cod_pedido'] + cotizaciones['cuo'].astype(str)

    # Definir columnas de texto
    str_columns = ['alias', 'moneda', 'descripcion', 'unid_medida', 'llegada', 'datos_adicionales',
                   'observaciones']

    # Definir columnas a formatear
    columns_to_round = ['precio_unit', 'cuota1', 'cuota2', 'cuota3', 'cuota4']

    # Aplica redondeo a cada columna en la lista
    for col in columns_to_round:
        cotizaciones[col] = cotizaciones[col].apply(lambda x: round(x, 3) if pd.notna(x) else x)

    # Cambiar mayusculas y quitar espacios de los extremos a cada valor de cada columna de texto
    for column in str_columns:
        if cotizaciones[column].notna().any():
            cotizaciones[column] = cotizaciones[column].apply(lambda x: x.strip().upper() if pd.notna(x) else x)

    # Separar columnas de facturacion
    facturas = cotizaciones[['cod_pedido', 'cuo', 'alias', 'emision', 'moneda', 'descripcion', 'unid_medida',
                             'cantidad', 'precio_unit', 'observaciones', 'vencimiento', 'cuota1',
                             'vencimiento2', 'cuota2', 'vencimiento3', 'cuota3', 'vencimiento4', 'cuota4']]

    # Definir funcion de agrupamiento para las guias
    def columnas_guia(group):
        guia = group.iloc[0].copy()  # Tomar el primer valor de cada columna
        total_peso = (group['cantidad'] * group['peso_articulo']).sum()  # Sumar el producto de cantidad y peso
        guia['datos_adicionales'] = 'Peso: ' + str(
            math.ceil(total_peso))  # Actualizar el valor de 'peso' en el primer registro

        return guia

    # Separar columnas para la tabla remision_remitente, aplicar funcion de agrupamiento y retirar columnas sobrantes
    remision_remitente = (cotizaciones[
                              ['cui', 'cod_pedido', 'cuo', 'alias', 'traslado', 'llegada', 'cantidad',
                               'peso_articulo', 'placa', 'conductor',
                               'datos_adicionales', 'observaciones']].groupby('cui').apply(columnas_guia,
                                                                                           include_groups=False)
                          .drop(['cantidad', 'peso_articulo'], axis=1))

    session = Session()
    for cod_pedido in facturas['cod_pedido'].unique():
        pedido = session.query(Pedidos).filter(Pedidos.cod_pedido == cod_pedido)
        pedido.update({Pedidos.estado: 'EN PROCESO'})
    session.commit()

    return print(facturas.to_sql('facturas', salessystem, if_exists='append', index=False),
                 remision_remitente.to_sql('remision_remitente', salessystem, if_exists='append', index=False))


