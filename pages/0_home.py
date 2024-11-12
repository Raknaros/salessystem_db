import streamlit as st

from services.Querys import proveedores, adquirientes, catalogo

st.set_page_config(page_title="Home", page_icon=":material/edit:", layout="wide")

if 'authenticator' not in st.session_state:
    st.error("Error: No se ha cargado el objeto de autenticación.")
else:
    authenticator = st.session_state['authenticator']
    if st.session_state.get("authentication_status"):
        st.session_state.sidebar()
        st.write("Bienvenido a la página de carga de pedidos")
        st.header("this is the markdown")
        st.markdown("this is the header")
        st.subheader("this is the subheader")
        st.caption("this is the caption")
        st.code("x=2021")
        st.latex(r''' a+a r^1+a r^2+a r^3 ''')
        # Continúa con el contenido de la página
    else:
        st.error("No estás autenticado.")
        st.stop()

tab1, tab2, tab3 = st.tabs(["Proveedores", "Adquirientes", "Catalogo"])

with tab1:
    st.dataframe(proveedores, height=300, hide_index=True, column_config={
        "tipo_proveedor": st.column_config.NumberColumn(
            "Tipo",
            help="Diferenciacion de los proveedores",
            format='%d',
        ),
        "numero_documento": st.column_config.NumberColumn(
            "RUC",
            format='%d'
        ),
        "nombre_razon": st.column_config.TextColumn(
            "Nombre o Razon Social"
        ),
        "alias": st.column_config.TextColumn(
            "Alias"
        ),
        "estado": st.column_config.TextColumn(
            "Estado"
        ),
        "observaciones": st.column_config.TextColumn(
            "Observaciones"
        ),
        "actividad_economica": st.column_config.TextColumn(
            "Actividad Economica"
        ),
        "act_econ_sec_1": st.column_config.TextColumn(
            "Act. Econ. Secundaria 1"
        ),
        "act_econ_sec_2": st.column_config.TextColumn(
            "Act. Econ. Secundaria 2"
        )
    }, column_order=['tipo_proveedor', 'numero_documento', 'nombre_razon', 'alias', 'estado', 'observaciones',
                     'actividad_economica', 'act_econ_sec_1', 'act_econ_sec_2'])
with tab2:
    st.dataframe(adquirientes, height=300, hide_index=True, column_config={
        "ruc": st.column_config.NumberColumn(
            "RUC",
            help="Numero de RUC del adquiriente o cliente",
            format='%d'
        ),
        "nombre_razon": st.column_config.TextColumn(
            "Nombre o Razon Social",
            width='large'
        ),
        "alias": st.column_config.TextColumn(
            "Alias",
            width='medium'
        ),
        "related_user": st.column_config.TextColumn(
            "Cliente",
            width='medium'
        ),
        "observaciones": st.column_config.TextColumn(
            "Observaciones",
            width='large'
        )
    }, column_order=['nombre_razon', 'alias', 'ruc', 'related_user', 'observaciones'])
with tab3:
    st.dataframe(catalogo, height=300, hide_index=True, column_config={
        "id": st.column_config.TextColumn(
            "Codigo"
        ),
        "categoria": st.column_config.TextColumn(
            "Categoria"
        ),
        "descripcion": st.column_config.TextColumn(
            "Descripcion"
        ),
        "precio": st.column_config.NumberColumn(
            "Precio",
            format='S/.%d',
        ),
        "unidad_medida": st.column_config.TextColumn(
            "U.M."
        ),
        "peso": st.column_config.NumberColumn(
            "Peso",
            format='%d',
        )
    }, column_order=['id', 'categoria', 'descripcion', 'precio', 'unidad_medida', 'peso'])