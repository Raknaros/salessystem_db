from sqlalchemy import Column, Integer, String, BigInteger, MetaData, create_engine, text

engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                       ':3306/salessystem')

connection = engine.connect()

query = "SELECT * FROM lista_facturas WHERE emision > '2024-06-25'"
result = connection.execute(text(query))


for row in result:
    print(row)






"""    with pd.ExcelWriter('PorEmitir.xlsx', engine='xlsxwriter') as writer:
        for proveedor in proveedores:
            lista_proveedor = lista_facturas[lista_facturas['alias'] == proveedor]
            if lista_proveedor.empty:
                break
            current_lista = pd.pivot_table(lista_proveedor,
                                           values=["sub_total", "igv", "total", "vencimiento", "moneda"],
                                           index=['cui', 'guia', 'numero', 'ruc', 'emision', 'descripcion', 'unidad_medida',
                                                  'cantidad', 'p_unit'],
                                           aggfunc={'sub_total': 'sum', 'igv': 'sum', 'total': 'sum',
                                                    'vencimiento': 'first',
                                                    'moneda': 'first'})

            current_lista = current_lista[['sub_total', 'igv', 'total', 'vencimiento', 'moneda']]
            current_lista = pd.concat([
                y._append(
                    y[['sub_total', 'igv', 'total']].sum().rename(
                        (x, list_guias.at[x, 'placa'], list_guias.at[x, 'conductor'],
                         '', '', list_guias.at[x, 'llegada'],
                         list_guias.at[x, 'datos_adicionales'], '', 'Totales')))
                for x, y in current_lista.groupby(level=0)
            ])
            current_lista.to_excel(writer, sheet_name=proveedor, float_format='%.3f', startrow=1)
            workbook = writer.book
            current_worksheet = writer.sheets[proveedor]
            current_worksheet.write_row(0, 0, lista_proveedores.loc[lista_proveedores['alias'] == proveedor].values.flatten().tolist())
            cell_format = workbook.add_format({'bold': True, 'font_size': 10})

            current_worksheet.set_column(1, 15, None, cell_format)
            current_worksheet.set_column(0, 0, 13)
            current_worksheet.set_column(1, 1, 11)
            current_worksheet.set_column(2, 2, 10)
            current_worksheet.set_column(3, 3, 12)
            current_worksheet.set_column(4, 4, 11)
            current_worksheet.set_column(5, 5, 45)
            current_worksheet.set_column(6, 6, 5)
            current_worksheet.set_column(12, 12, 10)"""