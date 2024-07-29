from collections import defaultdict
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Float, Date, Boolean
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
    alias = Column(String(12), nullable=True)
    cui = Column(String(35), primary_key=True)
    guia = Column(String(8), nullable=True)
    numero = Column(String(8), nullable=True)
    ruc = Column(BigInteger, nullable=True)
    emision = Column(Date, nullable=True)
    descripcion = Column(String(50), primary_key=True)
    unidad_medida = Column(String(5), nullable=True)
    cantidad = Column(Float, nullable=True)
    p_unit = Column(Float, nullable=True)
    sub_total = Column(Float, nullable=True)
    igv = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    vencimiento = Column(Date, nullable=True)
    moneda = Column(String(4), nullable=True)


class ListaGuias(Base):
    __tablename__ = 'lista_guias'
    alias = Column(String(35), nullable=True)
    cui = Column(String(35), primary_key=True)
    traslado = Column(Date, primary_key=True)
    partida = Column(String(50), nullable=True)
    llegada = Column(String(50), nullable=True)
    placa = Column(String(8), nullable=True)
    conductor = Column(String(10), nullable=True)
    datos_adicionales = Column(String(35), nullable=True)
    observaciones = Column(String(35), nullable=True)


class Pedidos(Base):
    __tablename__ = 'pedidos'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cod_pedido = Column(String(8), nullable=True)
    fecha_pedido = Column(Date, nullable=True)
    periodo = Column(Integer, nullable=True)
    adquiriente = Column(String(35), nullable=True)
    importe_total = Column(Float, nullable=True)
    rubro = Column(Float, nullable=True)
    promedio_factura = Column(Float, nullable=True)
    contado_credito = Column(Float, nullable=True)
    bancariza = Column(Float, nullable=True)
    notas = Column(Float, nullable=True)
    estado = Column(String(20), nullable=True)
    punto_entrega = Column(Float, nullable=True)


class Bancarizaciones(Base):
    __tablename__ = 'v_bcp'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dato_referencial = Column(Date, nullable=True)
    fecha_operacion = Column(Date, nullable=True)
    hora_operacion = Column(Date, nullable=True)
    numero_operacion = Column(Integer, nullable=True)
    importe = Column(Float, nullable=True)
    adquiriente = Column(String(35), nullable=True)
    proveedor = Column(String(35), nullable=True)
    documento_relacionado = Column(String(35), nullable=True)
    customer_id = Column(String(35), nullable=True)
    observaciones = Column(String(35), nullable=True)
    cui = Column(String(30), nullable=True)


class Facturas(Base):
    __tablename__ = 'facturas'
    cod_pedido = Column(String(8), nullable=True)
    cuo = Column(String(35), nullable=True)
    alias = Column(String(35), nullable=True)
    guia = Column(String(35), nullable=True)
    serie = Column(String(35), nullable=True)
    numero = Column(String(35), nullable=True)
    emision = Column(Date, nullable=True)
    ruc = Column(BigInteger, nullable=True)
    nombre_razon = Column(String(35), nullable=True)
    moneda = Column(String(4), nullable=True)
    descripcion = Column(String(50), nullable=True)
    unid_medida = Column(String(5), nullable=True)
    cantidad = Column(Float, nullable=True)
    precio_unit = Column(Float, nullable=True)
    forma_pago = Column(String(35), nullable=True)
    estado = Column(String(20), nullable=True)
    observaciones = Column(String(35), nullable=True)
    vencimiento = Column(Date, nullable=True)
    cuota1 = Column(Float, nullable=True)
    vencimiento2 = Column(Float, nullable=True)
    cuota2 = Column(Float, nullable=True)
    vencimiento3 = Column(Float, nullable=True)
    cuota3 = Column(Float, nullable=True)
    vencimiento4 = Column(Float, nullable=True)
    cuota4 = Column(Float, nullable=True)
    detraccion = Column(String(35), nullable=True)
    retencion = Column(String(35), nullable=True)


class RemisionRemitente(Base):
    __tablename__ = 'remision_remitente'
    cod_pedido = Column(String(8), nullable=True)
    cuo = Column(String(35), nullable=True)
    alias = Column(String(35), nullable=True)
    factura = Column(String(35), nullable=True)
    serie = Column(String(35), nullable=True)
    numero = Column(String(35), nullable=True)
    traslado = Column(Date, nullable=True)
    partida = Column(String(50), nullable=True)
    llegada = Column(String(50), nullable=True)
    placa = Column(String(8), nullable=True)
    conductor = Column(String(10), nullable=True)
    datos_adicionales = Column(String(35), nullable=True)
    estado = Column(String(20), nullable=True)
    observaciones = Column(String(35), nullable=True)


class Customers(Base):
    __tablename__ = 'customers'


class Proveedores(Base):
    __tablename__ = 'proveedores'


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
proveedores = ['TOCAM']  #'CHERRYS', 'CONSULCACH', 'CONSULCELIZ', 'NOVATEX', 'IMBOX',


# Función para cambiar formato de fecha a dd/mm/yyyy
def formato_fecha(fecha):
    return pd.to_datetime(fecha, format='%Y-%m-%d').strftime('%d/%m/%Y')


# Función para cambiar formato de float a str con dos decimales o entero
def formato_float(num):
    if pd.notna(num):
        # Convertir el número a string para contar los decimales
        num_str = f'{num:.10f}'  # Tomamos hasta 10 decimales para asegurarnos de capturar todos
        num_decimales = len(num_str.split('.')[1].rstrip('0'))  # Contar los decimales significativos

        # Mostrar hasta 4 decimales como máximo
        if num_decimales > 4:
            return f'{num:.4f}'
        elif 0 < num_decimales <= 2:
            return f'{num:.2f}'
        elif 2 < num_decimales <= 4:
            return f'{num:.{num_decimales}f}'
        else:
            return f'{num:.0f}'
    else:
        return ''


# Aplicar las funciones de formato a las columnas respectivas
lista_facturas['emision'] = lista_facturas['emision'].apply(formato_fecha)
lista_facturas['vencimiento'] = lista_facturas['vencimiento'].apply(formato_fecha)
lista_guias['traslado'] = lista_guias['traslado'].apply(formato_fecha)

lista_facturas[['cantidad', 'p_unit']] = lista_facturas[['cantidad', 'p_unit']].applymap(formato_float)

with pd.ExcelWriter('PorEmitir.xlsx', engine='xlsxwriter') as writer:
    workbook = writer.book
    formato1 = workbook.add_format({'bold': True, 'font_size': 12})
    formato2 = workbook.add_format({'italic': True, 'font_size': 10})
    formato3 = workbook.add_format({'font_size': 10})
    formato4 = workbook.add_format({'bold': True, 'font_size': 8})
    alineamiento = workbook.add_format()
    alineamiento.set_align('vright')
    for proveedor in proveedores:
        lista_proveedor = lista_facturas[lista_facturas['alias'] == proveedor]
        # LISTA DE CUI SIN DUPLICADOS BASADA EN LAS FACTURAS
        lista_cui = lista_proveedor['cui'].drop_duplicates().tolist()
        if lista_proveedor.empty:
            break
        current_worksheet = workbook.add_worksheet(proveedor)
        fila = 0
        current_worksheet.write_row(fila, 0, lista_proveedores.loc[
            lista_proveedores['alias'] == proveedor].values.flatten().tolist(), formato4)
        fila += 1
        current_worksheet.write_row(fila, 0, ['CUI', 'GUIA', 'FACTURA', 'EMISION', 'ADQUIRIENTE', 'U. MED',
                                              'DESCRIPCION', 'CANTIDAD', 'P. UNIT.', 'SUB-TOTAL', 'VENCIMIENTO',
                                              'MONEDA'], formato1)
        fila += 1
        for cui in lista_cui:
            # SELECCIONAR LAS FACTURAS QUE COINCIDAN CON EL CUI SELECCIONADO RESETEANDO EL INDICE PARA QUE EMPIECE DESDE 0
            factura = lista_facturas[lista_facturas['cui'] == cui].reset_index(drop=False)
            # POR CADA INDICE Y FILA
            for index, row in factura.iterrows():
                # SI EL INDICE ES 0 O ES LA PRIMERA LINEA DE LA FACTURA
                if index == 0:
                    # COLOCAR TODOS LOS DATOS
                    current_worksheet.write_row(fila, 0, (cui, row['guia'], row['numero'], row['emision'], row['ruc'],
                                                          row['unidad_medida'], row['descripcion'], row['cantidad'],
                                                          row['p_unit'], row['sub_total'], row['vencimiento'],
                                                          row['moneda']), formato3)
                    fila += 1

                # SI EL INDICE ES EL ULTIMO COLOCAR TOTALES (en la emision solo figuran cantidad, p.unit, igv total y total por item)
                elif index == len(factura) - 1:
                    current_worksheet.write_row(fila, 5, (row['unidad_medida'], row['descripcion'], row['cantidad'],
                                                          row['p_unit'], row['sub_total']), formato3)
                    fila += 1
                    # SUBTOTALIZAR CADA ARTICULO Y EL TOTAL DE LA FACTURA TAMBIEN CON SU ENCABEZADO PEQUENO
                    current_worksheet.write_row(fila, 9, (factura['sub_total'].sum(),
                                                          factura['sub_total'].sum() * 0.18,
                                                          factura['sub_total'].sum() * 1.18), formato3)
                    fila += 1
                    # CONSIDERAR COLOCAR CADA DETALLE DE LA GUIA CON SU ENCABEZADO EN FORMATO MAS PEQUENO
                    current_worksheet.write_row(fila, 1,
                                                lista_guias[lista_guias['cui'] == cui].drop(['cui', 'alias'],
                                                                                            axis=1).values.flatten().tolist(),
                                                formato2)
                    # +2 REEMPLAZA A LA FILA VACIA QUE SE NECESITA
                    fila += 2
                else:
                    current_worksheet.write_row(fila, 5, (row['unidad_medida'], row['descripcion'], row['cantidad'],
                                                          row['p_unit'], row['sub_total']), formato3)
                    fila += 1
        current_worksheet.set_column(0, 0, 12)  #COLUMNA CUI
        current_worksheet.set_column(1, 1, 10)  #COLUMNA GUIA
        current_worksheet.set_column(2, 2, 10)  #COLUMNA FACTURA
        current_worksheet.set_column(3, 3, 10)  #COLUMNA EMISION
        current_worksheet.set_column(4, 4, 11)  #COLUMNA ADQUIRIENTE
        current_worksheet.set_column(5, 5, 4)  #COLUMNA UNIDAD DE MEDIDA
        current_worksheet.set_column(6, 6, 45)  #COLUMNA DESCRIPCION
        current_worksheet.set_column(7, 8, None, alineamiento)
        current_worksheet.set_column(10, 10, 10)  #COLUMNA VENCIMIENTO

# POR CADA CUI EN LA LISTA
"""for cui in lista_cui:
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
            #print('n')
        else:
            print(row['descripcion'], row['cantidad'],
                  row['p_unit'], row['sub_total'])

""
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
