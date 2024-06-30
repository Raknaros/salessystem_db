from collections import defaultdict

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


# Using the 'Vehiculo' class (assuming you defined it)
results = session.query(ListaFacturas).all()  # Replace 'Vehiculo' with your actual class name if defined

for row in results:
    print(row.cui)

#facturas_por_cui = defaultdict(list)

# Iterar sobre los resultados y agrupar por 'cui'
#for factura in results:
#    facturas_por_cui[factura.cui].append(factura)


#for cui, facturas in facturas_por_cui.items():
#    print(f"CUI: {cui}")
#    for factura in facturas:
#        print(f"  Descripcion: {factura.descripcion}, Precio: {factura.p_unit}, Cantidad: {factura.cantidad}")

# O acceder directamente a un grupo específico
#cui_especifico = 'X134D8F41-2'
#facturas_cui_especifico = facturas_por_cui[cui_especifico]
#print(facturas_cui_especifico[1].descripcion)


"""vehiculo = session.query(Vehiculos).all()

# Loop through the results
for vehicle in vehiculo:
    print(vehicle.placa)  # Each 'vehicle' will be an instance of your 'Vehiculo' class


new_vehicle = Vehiculo(placa="PRUEBA", modelo="CarroPrueba", marca=)
session.add(new_vehicle)
session.commit()
"""
