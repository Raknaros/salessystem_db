import pandas as pd
from datetime import date
from time import sleep
from sqlalchemy import create_engine, insert
import numpy as np;
import re

from models import Pedidos, session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def put_pedidos(data: list):
    #decidir entre insert interado y bulk insert, colocar el trigger de cambio de alias a ruc en el metodo put_pedidos
    try:
        for item in data:
            if re.search("[a-zA-Z]", item.get('adquiriente')):

            nuevo_pedido = Pedidos(
            fecha_pedido=item['fecha_pedido'],
            periodo=item['periodo'],
            adquiriente=item['adquiriente'],
            importe_total=item['total'],
            rubro=item['rubro'],
            promedio_factura=item['promedio'],
            contado_credito=item.get('forma_pago'),  # Usar .get() para evitar KeyError
            notas=item.get('notas'),
        )
            session.add(nuevo_pedido)
        session.commit()  # Commit al final
    except Exception as e:
        session.rollback()
        print(f"Error al insertar el pedido: {e}")
