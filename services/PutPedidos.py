import pandas as pd
from datetime import date
from time import sleep
from sqlalchemy import create_engine, insert
import numpy as np;
import re

from models import Pedidos, session
from services.Querys import adquirientes, cargar_datos

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#REVISAR LA CONSULTA DEL RUC DEL CUSTOMER SI RECIBE MINUSCULAS, REVISAR SI SE ELIMINA ALGUN PEDIDO CAUSA UN ERROR EN EL CONTEO Y NUMERACION DE LOS PEDIDOS
def put_pedidos(data: list):
    #decidir entre insert interado y bulk insert, colocar el trigger de cambio de alias a ruc en el metodo put_pedidos
    try:
        for fila in data:
            ruc_adquiriente = fila['adquiriente']
            if re.search("[a-zA-Z]", str(fila.get('adquiriente'))):
                ruc_adquiriente = adquirientes.loc[adquirientes['alias'] == fila['adquiriente'], 'ruc'].values[0]
            nuevo_pedido = Pedidos(
                fecha_pedido=fila['fecha_pedido'],
                periodo=fila['periodo'],
                adquiriente=ruc_adquiriente,
                importe_total=fila['importe_total'],
                rubro=fila['rubro'],
                promedio_factura=fila['promedio_factura'],
                contado_credito=fila.get('forma_pago'),  # Usar .get() para evitar KeyError
                notas=fila.get('notas'),
            )
            session.add(nuevo_pedido)
        session.commit()  # Commit al final
        if len(data) > 1:
            return len(data)
        elif len(data) == 1:
            return cargar_datos().tail(1)["cod_pedido"]
    except Exception as e:
        session.rollback()
        return "Ocurrió un error al insertar el pedido"

