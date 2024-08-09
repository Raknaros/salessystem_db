from models import *
from sqlalchemy import create_engine
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

passwords_to_hash = ['emisor2024','EvelynCBM1968', 'p259E9C695+']
hashed_passwords = Hasher(passwords_to_hash).generate()

print(hashed_passwords)