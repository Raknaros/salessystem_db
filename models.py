from collections import defaultdict
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Float, Date, Boolean, Time
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

#engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
#                       ':3306/salessystem')

connection = pymysql.connect(
    host='sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Giu72656770',
    database='salessystem',
    connect_timeout=30  # Aumentar el valor de tiempo de espera
)

Base = declarative_base()

Session = sessionmaker(bind=connection)

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
