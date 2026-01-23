
import io

import pandas as pd
from datetime import date

from sqlalchemy import create_engine
import numpy as np
import streamlit as st
import services.Querys as Querys






def get_precuadros(ped_seleccionados):
    # print(1)
    df = Querys.pedidos()
    # print(2)
    df = df.loc[df['estado'] == 'PENDIENTE']
    # print(3)
    adquirientes = Querys.adquirientes()
    # print(4)
    pre_detalle = Querys.pre_detalle()
    # print(5)
    catalogo = Querys.catalogo()
    # print(6)
    adquirientes['ruc'] = adquirientes['ruc'].astype(str)
    # print(7)
    if ped_seleccionados == 'TODOS':
        seleccionados = df['cod_pedido'].tolist()
    else:
        seleccionados = df[df['adquiriente'].isin(ped_seleccionados)]['cod_pedido'].tolist()
    # print(8)
    #pedidos_extendido = pd.merge(df, adquirientes[['ruc', 'alias']], left_on='adquiriente', right_on='ruc',
    #                             how='left')
    # print(9)
    encabezado = ['cuo', 'alias', 'emision', 'descripcion', 'cantidad', 'precio_unit', 'total',
                  'peso_articulo', 'peso_total', 'observaciones', 'vencimiento', 'cuota1', 'vencimiento2',
                  'cuota2', 'vencimiento3', 'cuota3', 'vencimiento4', 'cuota4', 'moneda',
                  'unid_medida', 'traslado', 'lugar_entrega', 'placa', 'conductor', 'datos_adicionales']
    # print(10)
    detalle_completo = pd.merge(pre_detalle, catalogo, on='descripcion', how='left')
    # print(11)
    buffer = io.BytesIO()
    # print(12)
    with pd.ExcelWriter(buffer) as writer:
        # print(13)
        for cod_pedido in seleccionados:
            # print(14)
            detalle = detalle_completo.loc[detalle_completo['numero_documento'] == str(int(df.loc[df['cod_pedido'] == cod_pedido]['ruc'].values.item()))].sort_values(by='fecha_emision', ascending=False).head(30)
            try:
                # print(15)
                workbook = writer.book
                # print(16)
                current_worksheet = workbook.add_worksheet(cod_pedido)
                # print(17)
                #['cod_pedido','periodo','importe_total', 'rubro', 'promedio_factura', 'contado_credito''notas' 'punto_entrega''alias']
                current_worksheet.write_row(0, 0,
                                            df[
                                                ['cod_pedido', 'periodo', 'adquiriente', 'contado_credito', 'importe_total',
                                                 'promedio_factura', 'notas', 'rubro',
                                                 'punto_entrega', 'ruc']].loc[df['cod_pedido'] == cod_pedido].values.flatten().tolist())
                # print(18)
                current_worksheet.write_column(2, 3, detalle['descripcion'].tolist()) #descripcion
                # print(19)
                current_worksheet.write_column(2, 4, detalle['cantidad'].tolist()) #cantidad
                # print(20)
                current_worksheet.write_column(2, 5, detalle['precio_unitario'].tolist()) #precio
                # print(21)
                current_worksheet.write_column(2, 7, detalle['peso'].tolist()) #peso
                # print(22)
                current_worksheet.write_column(2, 19, detalle['unidad_medida_y'].tolist()) #unidad_medida
                # print(23)

            except:
                None
            finally:
                # print(24)
                current_worksheet.write_row(1, 0, encabezado)
                # print(25)
                cell_format1 = workbook.add_format({'bold': True, 'font_size': 12})
                # print(26)
                cell_format2 = workbook.add_format({'bold': False, 'font_size': 10})
                # print(27)
                current_worksheet.set_row(0, None, cell_format1)
                # print(28)
                current_worksheet.set_row(1, None, cell_format1)
                # print(29)
                current_worksheet.set_column(0, 0, 7, cell_format2)
                # print(30)
                current_worksheet.set_column(1, 1, 9, cell_format2)
                # print(31)
                current_worksheet.set_column(2, 2, 11, cell_format2)
                # print(32)
                current_worksheet.set_column(3, 3, 45, cell_format2)
                # print(33)
                current_worksheet.write('G3', 'ROUND(E3*F3*1.18;3)')
                # print(34)
                current_worksheet.write('I3', 'ROUNDUP(E3*H3;0)')
                # print(35)

    return buffer.getvalue()



#TODO en cargar_pedidos revisar que al ingresar un pedido de un adquiriente nuevo aparezca en la tabla