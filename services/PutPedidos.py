import pandas as pd
from datetime import date
from time import sleep
from sqlalchemy import create_engine, insert
import numpy as np;

from models import Pedidos, Session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def put_pedidos(data: list):
    pedido = Session.execute(insert(Pedidos), data)
