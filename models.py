from collections import defaultdict
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Float, Date, Boolean, Time
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                       ':3306/salessystem')

Base = declarative_base()

Session = sessionmaker(bind=engine)



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
    cod_pedido = Column(String(10), nullable=True)
    fecha_pedido = Column(Date, nullable=True)
    periodo = Column(Integer, nullable=True)
    adquiriente = Column(String(35), nullable=True)
    importe_total = Column(Float, nullable=True)
    rubro = Column(String(35), nullable=True)
    promedio_factura = Column(Integer, nullable=True)
    contado_credito = Column(String(7), nullable=True)
    bancariza = Column(Boolean, nullable=True)
    notas = Column(String(50), nullable=True)
    estado = Column(String(20), nullable=True)
    punto_entrega = Column(String(50), nullable=True)


class Bancarizaciones(Base):
    __tablename__ = 'v_bcp'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dato_referencial = Column(String(35), nullable=True)
    fecha_operacion = Column(Date, nullable=True)
    hora_operacion = Column(Time, nullable=True)
    numero_operacion = Column(Integer, nullable=True)
    importe = Column(Float, nullable=True)
    adquiriente = Column(String(35), nullable=True)
    proveedor = Column(String(35), nullable=True)
    documento_relacionado = Column(String(13), nullable=True)
    customer_id = Column(String(5), nullable=True)
    observaciones = Column(String(50), nullable=True)
    cui = Column(String(30), nullable=True)


class Facturas(Base):
    __tablename__ = 'facturas'
    cod_pedido = Column(String(10), primary_key=True)
    cuo = Column(Integer, primary_key=True)
    alias = Column(String(12), nullable=True)
    guia = Column(String(13), nullable=True)
    serie = Column(String(4), nullable=True)
    numero = Column(BigInteger, nullable=True)
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
    observaciones = Column(String(50), nullable=True)
    vencimiento = Column(Date, nullable=True)
    cuota1 = Column(Float, nullable=True)
    vencimiento2 = Column(Date, nullable=True)
    cuota2 = Column(Float, nullable=True)
    vencimiento3 = Column(Date, nullable=True)
    cuota3 = Column(Float, nullable=True)
    vencimiento4 = Column(Date, nullable=True)
    cuota4 = Column(Float, nullable=True)
    detraccion = Column(Boolean, nullable=True)
    retencion = Column(Boolean, nullable=True)


class RemisionRemitente(Base):
    __tablename__ = 'remision_remitente'
    cod_pedido = Column(String(8), primary_key=True)
    cuo = Column(String(35), primary_key=True)
    alias = Column(String(20), nullable=True)
    factura = Column(String(13), nullable=True)
    serie = Column(String(4), nullable=True)
    numero = Column(String(8), nullable=True)
    traslado = Column(Date, nullable=True)
    partida = Column(String(50), nullable=True)
    llegada = Column(String(50), nullable=True)
    placa = Column(String(8), nullable=True)
    conductor = Column(String(10), nullable=True)
    datos_adicionales = Column(String(35), nullable=True)
    estado = Column(String(20), nullable=True)
    observaciones = Column(String(50), nullable=True)


class Customers(Base):
    __tablename__ = 'customers'
    adquiriente_id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruc = Column(BigInteger, nullable=True)
    alias = Column(String(35), nullable=True)
    related_user = Column(String(35), nullable=True)
    observaciones = Column(String(50), nullable=True)
    nombre_razon = Column(String(100), nullable=True)


class Proveedores(Base):
    __tablename__ = 'proveedores'
    proveedor_id = Column(BigInteger, primary_key=True, autoincrement=True)
    tipo_proveedor = Column(String(35), nullable=True)
    numero_documento = Column(BigInteger, nullable=True)
    nombre_razon = Column(String(50), nullable=True)
    estado = Column(String(20), nullable=True)
    related_partner = Column(String(35), nullable=True)
    observaciones = Column(String(50), nullable=True)
    actividad_economica = Column(String(100), nullable=True)
    act_econ_sec_1 = Column(String(100), nullable=True)
    act_econ_sec_2 = Column(String(100), nullable=True)
    usuario_sol = Column(String(20), nullable=True)
    clave_sol = Column(String(10), nullable=True)
    alias = Column(String(20), nullable=True)


"""
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
"""
