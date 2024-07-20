from collections import defaultdict
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                       ':3306/salessystem')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Vehiculo(Base):
    __tablename__ = 'vehiculos'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    placa = Column(String(8), nullable=True)
    modelo = Column(String(35), nullable=True)
    marca = Column(String(35), nullable=True)
    carga_util = Column(Integer, nullable=True)
    nro_constancia = Column(String(20), nullable=True)
    conductor = Column(String(12), nullable=True)
    empresa_trans = Column(String(35), nullable=True)
    ruc = Column(BigInteger, nullable=True)
    nro_autorizacion = Column(String(20), nullable=True)
    estado = Column(String(15), nullable=True)


class ListaFacturas(Base):
    __tablename__ = 'lista_facturas'
    #__table_args__ = {'extend_existing': True}
    alias = Column(String(35), nullable=True)
    cui = Column(String(35), primary_key=True)
    guia = Column(String(35), nullable=True)
    numero = Column(String(35), nullable=True)
    ruc = Column(BigInteger, nullable=True)
    emision = Column(String(35), nullable=True)
    descripcion = Column(String(35), primary_key=True)
    unidad_medida = Column(String(35), nullable=True)
    cantidad = Column(String(35), nullable=True)
    p_unit = Column(String(35), nullable=True)
    sub_total = Column(String(35), nullable=True)
    igv = Column(String(35), nullable=True)
    total = Column(String(35), nullable=True)
    vencimiento = Column(String(35), nullable=True)
    moneda = Column(String(35), nullable=True)


class ListaGuias(Base):
    __tablename__ = 'lista_guias'
    alias = Column(String(35), nullable=True)
    cui = Column(String(35), primary_key=True)
    traslado = Column(String(35), primary_key=True)
    partida = Column(String(35), nullable=True)
    llegada = Column(String(35), nullable=True)
    placa = Column(String(35), nullable=True)
    conductor = Column(String(35), nullable=True)
    datos_adicionales = Column(String(35), nullable=True)
    observaciones = Column(String(35), nullable=True)


# VISTA LISTAFACTURAS DE FACTURAS CON ESTADO 'POR EMITIR'
lista_facturas_query = session.query(ListaFacturas).statement
# VISTA LISTAGUIAS DE GUIAS CON ESTADO 'POR EMITIR'
lista_guias_query = session.query(ListaGuias).statement
# QUERY DE PROVEEDORES CON LOS DATOS DE ACCESO
lista_proveedores = pd.read_sql('SELECT alias, numero_documento, usuario_sol, clave_sol FROM proveedores', engine)

# DATAFRAME LISTAFACTURAS
lista_facturas = pd.read_sql(lista_facturas_query, con=engine)
# DATAFRAME LISTAGUIAS
lista_guias = pd.read_sql(lista_guias_query, con=engine)

# PROVEEDORES SOLICITADOS
proveedores = ['CHERRYS', 'CONSULCACH', 'CONSULCELIZ', 'NOVATEX', 'IMBOX', 'TOCAM']

with pd.ExcelWriter('PorEmitir.xlsx', engine='xlsxwriter') as writer:
    for proveedor in proveedores:
        lista_proveedor = lista_facturas[lista_facturas['alias'] == proveedor]
        # LISTA DE CUI SIN DUPLICADOS BASADA EN LAS FACTURAS
        lista_cui = lista_proveedor['cui'].drop_duplicates().tolist()
        if lista_proveedor.empty:
            break
        workbook = writer.book
        current_worksheet = workbook.add_worksheet(proveedor)
        fila = 0
        current_worksheet.write_row(fila, 0, lista_proveedores.loc[
            lista_proveedores['alias'] == proveedor].values.flatten().tolist())
        fila += 1
        current_worksheet.write_row(fila, 0, list(lista_facturas.columns))
        cell_format = workbook.add_format({'bold': True, 'font_size': 10})
        for cui in lista_cui:
            # SELECCIONAR LAS FACTURAS QUE COINCIDAN CON EL CUI SELECCIONADO RESETEANDO EL INDICE PARA QUE EMPIECE DESDE 0
            facturas = lista_facturas[lista_facturas['cui'] == cui].reset_index(drop=False)
            # POR CADA INDICE Y FILA
            for index, row in facturas.iterrows():
                # SI EL INDICE ES 0 O ES LA PRIMERA LINEA DE LA FACTURA
                if index == 0:
                    # COLOCAR TODOS LOS DATOS
                    current_worksheet.write_row(fila, 0, (cui, row['guia'], row['numero'], row['emision'], row['ruc'],
                                                          row['descripcion'], row['cantidad'], row['p_unit'],
                                                          row['sub_total'], row['vencimiento'], row['unidad_medida'],
                                                          row['moneda']))
                    fila += 1

                # SI EL INDICE ES EL ULTIMO COLOCAR TOTALES (en la emision solo figuran cantidad, p.unit, igv total y total por item)
                elif index == len(facturas) - 1:
                    current_worksheet.write_row(fila, 5, (row['descripcion'], row['cantidad'],
                                                          row['p_unit'], row['sub_total']))
                    fila += 1
                    # SUBTOTALIZAR CADA ARTICULO Y EL TOTAL DE LA FACTURA TAMBIEN CON SU ENCABEZADO PEQUENO
                    print(facturas['sub_total'].sum(), facturas['sub_total'].sum() * 0.18,
                          facturas['sub_total'].sum() * 1.18)
                    fila += 1
                    # CONSIDERAR COLOCAR CADA DETALLE DE LA GUIA CON SU ENCABEZADO EN FORMATO MAS PEQUENO
                    print(lista_guias[lista_guias['cui'] == cui])
                    # +2 REEMPLAZA A LA FILA VACIA QUE SE NECESITA
                    fila += 2
                else:
                    current_worksheet.write_row(fila, 5, (row['descripcion'], row['cantidad'],
                                                          row['p_unit'], row['sub_total']))
                    fila += 1

# POR CADA CUI EN LA LISTA
for cui in lista_cui:
    # SELECCIONAR LAS FACTURAS QUE COINCIDAN CON EL CUI SELECCIONADO RESETEANDO EL INDICE PARA QUE EMPIECE DESDE 0
    facturas = lista_facturas[lista_facturas['cui'] == cui].reset_index(drop=False)

    # POR CADA INDICE Y FILA
    for index, row in facturas.iterrows():

        # SI EL INDICE ES 0 O ES LA PRIMERA LINEA DE LA FACTURA
        if index == 0:
            #COLOCAR TODOS LOS DATOS
            print(cui, row['guia'], row['numero'], row['emision'], row['ruc'], row['descripcion'], row['cantidad'],
                  row['p_unit'], row['sub_total'], row['vencimiento'], row['unidad_medida'], row['moneda'])
        # SI EL INDICE ES EL ULTIMO COLOCAR TOTALES
        elif index == len(facturas) - 1:
            print(row['descripcion'], row['cantidad'],
                  row['p_unit'], row['sub_total'])
            print(facturas['sub_total'].sum(), facturas['sub_total'].sum() * 0.18, facturas['sub_total'].sum() * 1.18)
            print(lista_guias[lista_guias['cui'] == cui])
            print('\n')
        else:
            print(row['descripcion'], row['cantidad'],
                  row['p_unit'], row['sub_total'])

"""""
    with pd.ExcelWriter('PorEmitir.xlsx', engine='xlsxwriter') as writer:
        for proveedor in proveedores:
            lista_proveedor = lista_facturas[lista_facturas['alias'] == proveedor]
            if lista_proveedor.empty:
                break
            workbook = writer.book
            current_worksheet = workbook.add_worksheet(proveedor)
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
            current_worksheet.set_column(12, 12, 10)
"""
