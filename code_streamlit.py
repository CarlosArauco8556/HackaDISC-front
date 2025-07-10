import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Insecap",
    page_icon="images/Insecap_Logo-14.png",
    layout="wide"
)

# Estilos personalizados y logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .main > div:first-child { padding-top: 1rem !important; }
    .block-container { padding-left: 1rem !important; padding-right: 1rem !important; max-width: 95% !important; }
    .logo-container { display: flex; align-items: center; margin-bottom: 1rem; }
    .header { color: #485CC7; margin-bottom: 0.5rem; }
    .section-title { color: #333; margin-top: 2rem; margin-bottom: 0.5rem; font-weight: 600; }
    .small-text { font-size: 0.9rem; color: #666; }
    </style>
""", unsafe_allow_html=True)

# Logo en el sidebar
with st.sidebar:
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    st.image("images/Insecap_Logo-01.png", width=200)
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar de navegación
seccion = st.sidebar.selectbox("Selecciona una sección:", [
    "Clientes/Empresas",
    "Líderes Comerciales",
    "Destacados"
])

# Título institucional
st.markdown("<h1 class='header'>Insecap - Tiempos de Pago</h1>", unsafe_allow_html=True)

# --- Sección: Clientes/Empresas ---
if seccion == "Clientes/Empresas":
    st.markdown("<h3 class='section-title'>Resumen General</h3>", unsafe_allow_html=True)
    promedio_general = 45  # placeholder
    st.metric("Promedio de pago general", f"{promedio_general} días")

    st.divider()
    st.markdown("<h3 class='section-title'>Buscar Cliente</h3>", unsafe_allow_html=True)
    cliente = st.text_input("Buscar empresa/cliente")

    if cliente:
        datos = {
            "tiempos": [12, 7, 26],
            "historial": pd.DataFrame({
                'Venta': ['V1', 'V2'],
                'Inicio': ['2024-01-01', '2024-02-01'],
                'Pago Total': ['2024-01-30', '2024-03-10']
            }),
            "ventas_activas": pd.DataFrame({
                'ID': [101, 102],
                'Inicio': ['2024-04-01', '2024-05-01'],
                'Estimado Pago': ['2024-06-01', '2024-07-01']
            }),
            "estimacion_nueva": 33,
            "promedio_pago_total": 45
        }

        # Nombre de la empresa
        st.markdown("<h3 class='section-title'>'Nombre de la empresa'</h3>", unsafe_allow_html=True)

        # Mostrar métricas en columnas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Promedio histórico de pago", f"{datos['promedio_pago_total']} días")
        with col2:
            st.metric("Estimado de pago para nueva comercialización", f"{datos['estimacion_nueva']} días")

        st.markdown("**Tiempos promedio por etapa:**")
        etapas = ['En Proceso → Terminado', 'Terminado → Facturado', 'Facturado → Pagado']
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(etapas, datos['tiempos'], color='#00B8DE')
        ax.set_ylabel("Días")
        ax.set_title("Tiempos Promedio por Etapa")
        plt.xticks(rotation=15, ha='right')
        st.pyplot(fig)

        with st.expander("📄 Historial de Pagos"):
            st.dataframe(datos['historial'], use_container_width=True)

        with st.expander("📈 Ventas Activas (Estimación de Pago)"):
            st.dataframe(datos['ventas_activas'], use_container_width=True)

        st.info(f"⏱️ Tiempo estimado de pago para una nueva venta: **{datos['estimacion_nueva']} días**")

# --- Sección: Líderes Comerciales ---
elif seccion == "Líderes Comerciales":
    st.markdown("<h3 class='section-title'>Buscar Líder Comercial</h3>", unsafe_allow_html=True)
    lider = st.text_input("Buscar vendedor/líder comercial")

    if lider:
        tiempos_lider = [10, 8, 20]  # placeholder
        st.markdown("**Tiempos promedio por etapa:**")
        etapas = ['En Proceso → Terminado', 'Terminado → Facturado', 'Facturado → Pagado']
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(etapas, tiempos_lider, color='#00B8DE')
        ax.set_ylabel("Días")
        ax.set_title("Tiempos Promedio por Etapa del Vendedor")
        plt.xticks(rotation=15, ha='right')
        st.pyplot(fig)

# --- Sección: Destacados ---
elif seccion == "Destacados":
    st.markdown("<h3 class='section-title'>🏆 Empresas Destacadas</h3>", unsafe_allow_html=True)

    top_clientes = [
        {"nombre": "Empresa A", "dias": 22, "img": "images/Capin-11.png"},
        {"nombre": "Empresa B", "dias": 25, "img": "images/Capin-11.png"},
        {"nombre": "Empresa C", "dias": 27, "img": "images/Capin-11.png"}
    ]

    cols = st.columns(3)
    for idx, col in enumerate(cols):
        empresa = top_clientes[idx]
        medalla = ["🥇", "🥈", "🥉"][idx]
        with col:
            st.image(empresa["img"], width=100)
            st.markdown(f"### {medalla} {empresa['nombre']}")
            st.markdown(f"**{empresa['dias']} días promedio**")

    with st.expander("Ver Top 10 Clientes"):
        st.dataframe(pd.DataFrame(top_clientes), use_container_width=True)

    st.markdown("<h3 class='section-title'>🌟 Líderes Comerciales Destacados</h3>", unsafe_allow_html=True)

    top_lideres = [
        {"nombre": "Luis", "dias": 18, "img": "images/Capin-11.png"},
        {"nombre": "Camila", "dias": 20, "img": "images/Capin-11.png"},
        {"nombre": "Jorge", "dias": 22, "img": "images/Capin-11.png"}
    ]

    cols = st.columns(3)
    for idx, col in enumerate(cols):
        lider = top_lideres[idx]
        medalla = ["🥇", "🥈", "🥉"][idx]
        with col:
            st.image(lider["img"], width=100)
            st.markdown(f"### {medalla} {lider['nombre']}")
            st.markdown(f"**{lider['dias']} días promedio**")

    with st.expander("Ver Top 10 Vendedores"):
        st.dataframe(pd.DataFrame(top_lideres), use_container_width=True)

# --- Footer ---
st.markdown("""
    <hr>
    <div class='small-text'>© 2024 Insecap - Proyecto HackaDISC</div>
""", unsafe_allow_html=True)
