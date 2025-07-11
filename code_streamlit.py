from matplotlib import pyplot as plt
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Insecap",
    page_icon="images/Insecap_Favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados y logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    .header { color: #485CC7; margin-bottom: 0.5rem; margin-top: -2rem;}
    .section-title { color: #333; margin-top: 2rem; margin-bottom: 0.5rem; font-weight: 600; }
    .destacado-card {background: white; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border: 2px solid #00B8DE;}
    .insecap-card { background: linear-gradient(135deg, #485CC7 0%, #00B8DE 100%); padding: 1.5rem; border-radius: 15px; color: white; margin: 0.5rem 0; text-align: center;box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);}
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

with st.expander("🧾 Ver descripción del problema"):
    col1, col2 = st.columns([1, 5])  # Imagen más angosta, texto más ancho

    with col1:
        st.image("images/CapinInicial.png", width=140)

    with col2:
        st.markdown("""
        ### Descripción del problema

        Insecap no cuenta con una forma clara de conocer cuánto tardan sus clientes en pagar, lo cual dificulta
        anticiparse a retrasos y tomar decisiones oportunas. Esta herramienta permite visualizar y estimar los
        tiempos de pago, entregando una visión clara del comportamiento financiero de cada cliente.
        """)

# --- Sección Clientes/Empresas ---
if seccion == "Clientes/Empresas":

    st.markdown("<h3 class='section-title '>🏢 Análisis de Clientes</h3>", unsafe_allow_html=True)

        # Resumen general
    url_general = f"http://127.0.0.1:8000/comercializaciones/tiempo_pago_promedio"
    response_general = requests.get(url_general)
    if response_general.status_code == 200:
        data_general = response_general.json()

        promedio_general = data_general['promedio_dias_para_pago']
        st.markdown(f"""
        <div class="insecap-card">
            <h3>📊 Promedio General de Pago</h3>
            <h2>{promedio_general:.1f} días</h2>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

    nombre_cliente = st.text_input("🔍 Buscar cliente por nombre:")

    if nombre_cliente:
        # --- Obtener datos de cliente ---
        url_info = f"http://127.0.0.1:8000/clientes/tiempo_pago_promedio/{nombre_cliente}"
        url_etapas = f"http://127.0.0.1:8000/clientes/tiempos_etapa/{nombre_cliente}"

        response_info = requests.get(url_info)
        response_etapas = requests.get(url_etapas)

        if response_info.status_code == 200 and response_etapas.status_code == 200:
            data_info = response_info.json()
            data_etapas = response_etapas.json()

            # Perfil extendido del cliente
            st.subheader(f"👤 Perfil del Cliente: {data_info['nombre_cliente']}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Días Pago Promedio", f"{data_info['promedio_dias_para_pago']:.1f}")
            with col2:
                st.metric("Total Pagado", f"${data_info['valor_total_pagado']:,.0f}")
            with col3:
                st.metric("Valor Promedio Factura", f"${data_info['valor_promedio_factura']:,.0f}")
            with col4:
                st.metric("Total de ventas", f"{data_info['total_facturas_cliente']:,.0f}")  # o data_etapas['total_comercializaciones_cliente']

            # Mostrar tabla con tiempos de etapa
            st.subheader("⏱️ Tiempos promedio por etapa")
            df_etapas = pd.DataFrame({
                "Etapa": ["Proceso → Término", "Término → Factura", "Factura → Pago"],
                "Días Promedio": [
                    data_etapas['promedio_dias_proceso_a_termino'],
                    data_etapas['promedio_dias_termino_a_factura'],
                    data_etapas['promedio_dias_factura_a_pago']
                ]
            })
            st.table(df_etapas)

            # --- Predicción ---
            st.subheader("🔮 Predicción de pago estimado")

                # Parámetros de predicción
            col1, col2 = st.columns(2)

            with col1:
                cliente_id = st.number_input("Id del cliente:", min_value=0)

            with col2:
                valor_venta = st.number_input("Valor de venta ($):", min_value=1000, step=1000, value=100000)

            if st.button("Predecir días de pago"):
                url_pred = f"http://127.0.0.1:8000/clientes/predict_cliente?cliente_id={cliente_id}&valor_venta={valor_venta}"
                pred_response = requests.get(url_pred)

                if pred_response.status_code == 200:
                    pred_data = pred_response.json()['data']
                    dias = pred_data['dias_estimados_pago']
                    fecha_estimada = datetime.today() + timedelta(days=int(dias))
                    dias_pago_min = pred_data["dias_pago_min"]
                    dias_pago_max = pred_data["dias_pago_max"]
                    por_pago_prom = pred_data["porcentaje_pago_promedio"]*100
                    total_vend = pred_data["total_vendido"] # Informacion a verificar
                    total_pag = pred_data["total_pagado"] # Informacion a verificar
                    comport = pred_data["perfil"]

                    st.success(f"Predicción para Cliente '{cliente_id}'")
                    st.markdown(f"""
                    <div style="background-color: #f5f9ff; padding: 1.5rem; border-radius: 10px; border-left: 6px solid #4a90e2;">
                        <h4 style="color: #4a90e2;"> Predicción para Cliente <code>{cliente_id}</code></h4>
                        <ul style="list-style: none; padding-left: 0; font-size: 1rem;">
                            <li><strong>💰 Valor de venta:</strong> ${valor_venta:,.0f}</li>
                            <li><strong>📅 Días estimados de pago:</strong> {dias} días</li>
                            <li><strong>🗓️ Fecha estimada de pago:</strong> {fecha_estimada.strftime('%d-%m-%y')}</li>
                            <li><strong>📊 Rango de pago:</strong> {dias_pago_min} - {dias_pago_max} días</li>
                            <li><strong>✅ % Pago promedio:</strong> {por_pago_prom:.1f}%</li>
                            <li><strong>💵 Total vendido:</strong> ${total_vend:,}</li>
                            <li><strong>💸 Total pagado:</strong> ${total_pag:,}</li>
                            <li><strong>🧾 Comportamiento:</strong> {comport}</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Error al obtener la predicción.")

        else:
            st.warning("No se pudo obtener información del cliente. Verifica el nombre ingresado.")

# --- Sección: Líderes Comerciales ---
elif seccion == "Líderes Comerciales":
    st.markdown("<h3 class='section-title'>Buscar Líder Comercial</h3>", unsafe_allow_html=True)
    lider = st.text_input("Buscar vendedor/líder comercial")

    if lider:
        st.subheader(f"👤 Lider Comercial: {lider}") # Reemplazar por valor real

        tiempos_lider = [10, 8, 20]  # Reemplazar por valores reales
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

    # Reemplazar por datos reales
    top_clientes_data = [
        {"nombre": "FCAB", "dias": 18}, 
        {"nombre": "PYC", "dias": 20},
        {"nombre": "Komatsu", "dias": 22}
    ]

    # Mostrar top 3 con medallas
    cols = st.columns(3)
    medallas = ["🥇", "🥈", "🥉"]

    for idx in range(min(3, len(top_clientes_data))):
        cliente = top_clientes_data[idx]
        with cols[idx]:
            st.markdown(f"""
            <div class="destacado-card">
                <h3>{medallas[idx]} {cliente['nombre']}</h3>
                <h2>{cliente['dias']} días</h2>
                <p>Promedio de pago</p>
            </div>
            """, unsafe_allow_html=True)

    # Tabla completa expandible
    with st.expander("📊 Ver Top Clientes"):
        top_10_data = []
        for i, cliente in enumerate(top_clientes_data):
            top_10_data.append({
                "Posición": i + 1,
                "Nombre": cliente['nombre'],
                "Días Promedio": f"{cliente['dias']} días"
            })

        df_top_10 = pd.DataFrame(top_10_data)
        st.dataframe(df_top_10, use_container_width=True)

    # Líderes comerciales destacados (simulado)
    st.markdown("<h3 class='section-title'>🌟 Líderes Comerciales Destacados</h3>", unsafe_allow_html=True)

    # Reemplazar por datos reales
    lideres_destacados = [
        {"nombre": "Luis Pérez", "dias": 18},
        {"nombre": "Camila González", "dias": 20},
        {"nombre": "Jorge Martínez", "dias": 22}
    ]

    # Mostrar top 3 con medallas
    cols = st.columns(3)
    medallas = ["🥇", "🥈", "🥉"]

    for idx in range(min(3, len(lideres_destacados))):
        lideres_comerciales = lideres_destacados[idx]
        with cols[idx]:
            st.markdown(f"""
            <div class="destacado-card">
                <h3>{medallas[idx]} {lideres_comerciales['nombre']}</h3>
                <h2>{lideres_comerciales['dias']} días</h2>
                <p>Promedio de pago</p>
            </div>
            """, unsafe_allow_html=True)

    # Tabla completa expandible
    with st.expander("📊 Ver Top Lideres comerciales"):
        top_10_data = []
        for i, lideres_comerciales in enumerate(lideres_destacados):
            top_10_data.append({
                "Posición": i + 1,
                "Nombre": lideres_comerciales['nombre'],
                "Días Promedio": f"{lideres_comerciales['dias']} días"
            })

        df_top_10 = pd.DataFrame(top_10_data)
        st.dataframe(df_top_10, use_container_width=True)