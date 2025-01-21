import pandas as pd
from datetime import date
from time import sleep
from sqlalchemy import create_engine, insert
import numpy as np
import re

from models import Pedidos
from services import Querys
from services.Querys import Session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#REVISAR LA CONSULTA DEL RUC DEL CUSTOMER SI RECIBE MINUSCULAS, REVISAR SI SE ELIMINA ALGUN PEDIDO CAUSA UN ERROR EN EL CONTEO Y NUMERACION DE LOS PEDIDOS
#TODO CORREGIR INGRESO DE LUGAR DE ENTREGA
#TODO CORREGIR MOSTRAR PEDIDOS CON CUSTOMER NO REGISTRADO
def put_pedidos(data: list):
    adquirientes = Querys.adquirientes()
    #decidir entre insert interado y bulk insert, colocar el trigger de cambio de alias a ruc en el metodo put_pedidos
    session = Session()
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
                punto_entrega=fila['punto_llegada'],
                contado_credito=fila.get('forma_pago'),  # Usar .get() para evitar KeyError
                notas=fila.get('notas'),
            )
            session.add(nuevo_pedido)
        session.commit()# Commit al final
        if len(data) > 1:
            return "Se ingresaron "+str(len(data))+" pedidos."
        elif len(data) == 1:
            print('4')
            return "Se ingresó el pedido con código "+Querys.pedidos().iloc[-1]['cod_pedido']+"."

    except Exception as e:
        session.rollback()
        return "Ocurrió un error al insertar el pedido"
    finally:
        session.close()

#VERIFICAR DEMORA EN LA APLICACION