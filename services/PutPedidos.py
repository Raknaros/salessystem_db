import pandas as pd
from datetime import date
from time import sleep
from sqlalchemy import create_engine, insert
import numpy as np;

from models import Pedidos, session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def put_pedidos(data: list):
    #decidir entre insert interado y bulk insert, colocar el trigger de cambio de alias a ruc en el metodo put_pedidos
    try:
        session.execute(insert(Pedidos), data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error al insertar el pedido: {e}")
