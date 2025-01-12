
import io

import pandas as pd
from datetime import date

from sqlalchemy import create_engine
import numpy as np
import streamlit as st
import services.Querys as Querys






def get_precuadros(ped_seleccionados):
    df = st.session_state.df_pedidos
    adquirientes = Querys.adquirientes()
    pre_detalle = Querys.pre_detalle()
    catalogo = Querys.catalogo()
    adquirientes['ruc'] = adquirientes['ruc'].astype(str)
    if ped_seleccionados == 'TODOS':
        seleccionados = df.loc[df['estado'] == 'PENDIENTE']['cod_pedido'].tolist()
    else:
        seleccionados = df[df['adquiriente'].isin(ped_seleccionados)]['cod_pedido'].tolist()

    #pedidos_extendido = pd.merge(df, adquirientes[['ruc', 'alias']], left_on='adquiriente', right_on='ruc',
    #                             how='left')

    encabezado = ['cuo', 'alias', 'emision', 'descripcion', 'cantidad', 'precio_unit', 'total',
                  'peso_articulo', 'peso_total', 'observaciones', 'vencimiento', 'cuota1', 'vencimiento2',
                  'cuota2', 'vencimiento3', 'cuota3', 'vencimiento4', 'cuota4', 'moneda',
                  'unid_medida', 'traslado', 'lugar_entrega', 'placa', 'conductor', 'datos_adicionales']

    detalle_completo = pd.merge(pre_detalle, catalogo, on='descripcion', how='left')
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        for cod_pedido in seleccionados:
            detalle = detalle_completo.loc[detalle_completo['numero_documento'] == str(int(df.loc[df['cod_pedido'] == cod_pedido]['ruc'].values.item()))].sort_values(by='fecha_emision', ascending=False).head(30)
            try:
                workbook = writer.book
                current_worksheet = workbook.add_worksheet(cod_pedido)
                #['cod_pedido','periodo','importe_total', 'rubro', 'promedio_factura', 'contado_credito''notas' 'punto_entrega''alias']
                current_worksheet.write_row(0, 0,
                                            df[
                                                ['cod_pedido', 'periodo', 'adquiriente', 'contado_credito', 'importe_total',
                                                 'promedio_factura', 'notas', 'rubro',
                                                 'punto_entrega', 'ruc']].loc[df['cod_pedido'] == cod_pedido].values.flatten().tolist())
                current_worksheet.write_column(2, 3, detalle['descripcion'].tolist()) #descripcion
                current_worksheet.write_column(2, 4, detalle['cantidad'].tolist()) #cantidad
                current_worksheet.write_column(2, 5, detalle['precio_unitario'].tolist()) #precio
                current_worksheet.write_column(2, 7, detalle['peso'].tolist()) #peso
                current_worksheet.write_column(2, 19, detalle['unidad_medida_y'].tolist()) #unidad_medida

            except:
                None
            finally:
                current_worksheet.write_row(1, 0, encabezado)
                cell_format1 = workbook.add_format({'bold': True, 'font_size': 12})
                cell_format2 = workbook.add_format({'bold': False, 'font_size': 10})
                current_worksheet.set_row(0, None, cell_format1)
                current_worksheet.set_row(1, None, cell_format1)
                current_worksheet.set_column(0, 0, 7, cell_format2)
                current_worksheet.set_column(1, 1, 9, cell_format2)
                current_worksheet.set_column(2, 2, 11, cell_format2)
                current_worksheet.set_column(3, 3, 45, cell_format2)
                current_worksheet.write('G3', 'ROUND(E3*F3*1.18;3)')
                current_worksheet.write('I3', 'ROUNDUP(E3*H3;0)')

    return buffer.getvalue()



#TODO en cargar_pedidos revisar que al ingresar un pedido de un adquiriente nuevo aparezca en la tabla