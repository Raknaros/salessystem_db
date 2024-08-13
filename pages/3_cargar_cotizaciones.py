import streamlit as st

from services.Querys import bancarizaciones_poremitir

st.set_page_config(page_title="Cotizaciones", page_icon=":material/edit:", layout="wide")

if st.session_state["username"] == 'gerencia':
    st.session_state.gerencia_sidebar()
else:
    st.session_state.other_sidebar()

st.title('Cotizaciones')

st.dataframe(bancarizaciones_poremitir, height=450, hide_index=True)
