from models import *
from sqlalchemy import create_engine
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

passwords_to_hash = ['emisor2024','EvelynCBM1968', 'p259E9C695+']
hashed_passwords = Hasher(passwords_to_hash).generate()

salessystem = create_engine('mysql+pymysql://admin:Giu72656770@sales-system.c988owwqmmkd.us-east-1.rds.amazonaws.com'
                            ':3306/salessystem')

cotizaciones_poremitir = pd.read_sql("SELECT * FROM facturas WHERE estado NOT IN ('TERMINADO', 'ENTREGADO', 'ANULADA')",
                                        salessystem)

