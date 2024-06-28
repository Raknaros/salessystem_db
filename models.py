from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, ForeignKey, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                       ':3306/salessystem')

metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

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


# Using the 'Vehiculo' class (assuming you defined it)
result = session.query(Vehiculo).all()  # Replace 'Vehiculo' with your actual class name if defined

# Loop through the results
for vehicle in result:
    print(vehicle)  # Each 'vehicle' will be an instance of your 'Vehiculo' class
