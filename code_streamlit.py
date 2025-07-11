from matplotlib import pyplot as plt
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Insecap - Tiempos de Pago",
    page_icon="images/Insecap_Favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados mejorados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    /* Estilos generales */
    html, body, [class*="css"] { 
        font-family: 'Montserrat', sans-serif; 
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f2ff 100%);
    }
    
    /* Header principal */
    .main-header { 
        background: linear-gradient(135deg, #485CC7 0%, #00B8DE 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(72, 92, 199, 0.3);
    }
    .insecap-card p {
        font-size: 1rem;
        margin-bottom: 0.6rem;
    }   
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header .subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Sección de navegación */
    .nav-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border-left: 5px solid #485CC7;
    }
    
    /* Títulos de sección */
    .section-title { 
        color: #485CC7;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Cards destacados mejorados */
    .destacado-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 3px solid #00B8DE;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .destacado-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #485CC7, #00B8DE);
    }
    
    .destacado-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .destacado-card h3 {
        color: #485CC7;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .destacado-card h2 {
        color: #00B8DE;
        font-size: 2.2rem;
        margin: 0.5rem 0;
        font-weight: 700;
    }
    
    /* Card principal de Insecap */
    .insecap-card { 
        background: linear-gradient(135deg, #5a6de0 0%, #33c1ec 100%); /* Colores un poco más claros */
        padding: 2rem;
        border-radius: 20px;
        color: #ffffff;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(72, 92, 199, 0.3); /* Menos sombra para suavizar */
        position: relative;
        overflow: hidden;
        font-weight: 500;
    }
        
    .insecap-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .insecap-card h3 {
        font-size: 1.6rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .insecap-card h2 {
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Métricas mejoradas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-top: 4px solid #00B8DE;
        margin-bottom: 1rem;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #485CC7;
        margin: 0.5rem 0;
    }
    
    .metric-card .metric-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Predicción card */
    .prediction-card {
        background: linear-gradient(135deg, #f8fbff 0%, #e3f2fd 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #00B8DE;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0, 184, 222, 0.1);
    }
    
    .prediction-card h4 {
        color: #485CC7;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .prediction-card ul {
        list-style: none;
        padding: 0;
    }
    
    .prediction-card li {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #00B8DE;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }
    
    /* Tabla mejorada */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    /* Botones mejorados */
    .stButton > button {
        background: linear-gradient(135deg, #485CC7 0%, #00B8DE 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(72, 92, 199, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(72, 92, 199, 0.4);
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fbff 0%, #e8f2ff 100%);
    }
    
    /* Inputs mejorados */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00B8DE;
        box-shadow: 0 0 0 3px rgba(0, 184, 222, 0.1);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #00B8DE;
        box-shadow: 0 0 0 3px rgba(0, 184, 222, 0.1);
    }
    
    /* Expander mejorado */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #485CC7 0%, #00B8DE 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background: white;
        border-radius: 0 0 10px 10px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    /* Divider personalizado */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, #485CC7, #00B8DE);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Alertas mejoradas */
    .stAlert {
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .insecap-card h2 { font-size: 2.5rem; }
        .destacado-card h2 { font-size: 1.8rem; }
    }
    </style>
""", unsafe_allow_html=True)

# Logo en el sidebar mejorado
with st.sidebar:
    st.image("images/Insecap_Logo-01.png", width=200)
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar de navegación mejorado
st.sidebar.markdown("### 🧭 Navegación")
seccion = st.sidebar.selectbox("Selecciona una sección:", [
    "🏢 Clientes/Empresas",
    "👥 Líderes Comerciales",
    "🏆 Destacados"
], label_visibility="collapsed")

# Título institucional
st.markdown("<h1 class='header'>Insecap - Tiempos de Pago</h1>", unsafe_allow_html=True)


# Descripción del problema mejorada
with st.expander("🧾 Descripción del problema y objetivos"):
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image("images/CapinInicial.png", width=140)
    
    with col2:
        st.markdown("""
        ### 📋 Descripción del problema
        
        **Situación actual:** Insecap no cuenta con una forma clara de conocer cuánto tardan sus clientes en pagar, 
        lo cual dificulta anticiparse a retrasos y tomar decisiones oportunas.
        
        **Solución propuesta:** Esta herramienta permite visualizar y estimar los tiempos de pago, 
        entregando una visión clara del comportamiento financiero de cada cliente.
        
        **Beneficios:**
        - 📊 Análisis detallado por cliente
        - 🔮 Predicciones de pago
        - 📈 Seguimiento de líderes comerciales
        - 🏆 Identificación de clientes destacados
        """)

# --- Sección Clientes/Empresas ---
if seccion == "🏢 Clientes/Empresas":
    st.markdown("<h2 class='section-title'>🏢 Análisis de Clientes</h2>", unsafe_allow_html=True)

    # Resumen general mejorado
    try:
        url_general = f"http://127.0.0.1:8000/comercializaciones/tiempo_pago_promedio"
        response_general = requests.get(url_general)
        if response_general.status_code == 200:
            data_general = response_general.json()
            promedio_general = data_general['promedio_dias_para_pago']
            
            st.markdown(f"""
            <div class="insecap-card fade-in">
                <h3>📊 Promedio General de Pago</h3>
                <h2>{promedio_general:.1f} días</h2>
                <p>Tiempo promedio de pago de todos los clientes</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="insecap-card fade-in">
            <h3>📊 Promedio General de Pago</h3>
            <h2>No disponible</h2>
            <p>Tiempo promedio de pago de todos los clientes</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # Búsqueda de cliente mejorada
    st.markdown("### 🔍 Búsqueda de Cliente")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        nombre_cliente = st.text_input("Ingresa el nombre del cliente:", placeholder="Ej: FCAB, KOMATSU CHILE S.A, PYC...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_btn = st.button("🔍 Buscar", use_container_width=True)

    if nombre_cliente and (buscar_btn or nombre_cliente):
        try:
            # --- Obtener datos de cliente ---
            url_info_cliente = f"http://127.0.0.1:8000/clientes/tiempo_pago_promedio/{nombre_cliente}"
            url_etapas_cliente = f"http://127.0.0.1:8000/clientes/tiempos_etapa/{nombre_cliente}"
            response_info_cliente = requests.get(url_info_cliente)
            response_etapas_cliente = requests.get(url_etapas_cliente)

            if response_info_cliente.status_code == 200 and response_etapas_cliente.status_code == 200:
                data_info_cliente = response_info_cliente.json()
                data_etapas_cliente = response_etapas_cliente.json()

                # Perfil del cliente mejorado
                st.markdown(f"<h3 class='section-title'>👤 Perfil del Cliente: {data_info_cliente['nombre_cliente']}</h3>", unsafe_allow_html=True)

                # Métricas en cards mejoradas
                col1, col2, col3, col4 = st.columns(4)
                
                metrics = [
                    ("⏱️", "Días Pago Promedio", f"{data_info_cliente['promedio_dias_para_pago']:.1f} días"),
                    ("💰", "Total Pagado", f"${data_info_cliente['valor_total_pagado']:,.0f}"),
                    ("📊", "Promedio Factura", f"${data_info_cliente['valor_promedio_factura']:,.0f}"),
                    ("📈", "Total Ventas", f"{data_info_cliente['total_facturas_cliente']:,.0f}")
                ]
                
                for idx, (col, (icon, label, value)) in enumerate(zip([col1, col2, col3, col4], metrics)):
                    with col:
                        st.markdown(f"""
                        <div class="metric-card fade-in">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                            <div class="metric-value">{value}</div>
                            <div class="metric-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # Tabla de tiempos por etapa mejorada
                st.markdown("### ⏱️ Tiempos Promedio por Etapa")
                
                df_etapas = pd.DataFrame({
                    "🔄 Etapa": ["Proceso → Término", "Término → Factura", "Factura → Pago"],
                    "📅 Días Promedio": [
                        f"{data_etapas_cliente['promedio_dias_proceso_a_termino']:.1f}",
                        f"{data_etapas_cliente['promedio_dias_termino_a_factura']:.1f}",
                        f"{data_etapas_cliente['promedio_dias_factura_a_pago']:.1f}"
                    ]                })
                
                st.dataframe(df_etapas, use_container_width=True, hide_index=True)

                # Predicción mejorada
                st.markdown("### 🔮 Predicción de Pago")
                
                with st.container():
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    cliente_id = data_info_cliente["cliente_id"]
                    with col1:
                        valor_venta = st.number_input("Valor de venta ($):", min_value=1000, step=1000, value=100000)
                    
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        predict_btn = st.button("Predecir", use_container_width=True)     
                    with col3:
                        var_espacio = 0;               

                    if predict_btn:
                        try:
                            url_pred = f"http://127.0.0.1:8000/clientes/predict_cliente?cliente_id={cliente_id}&valor_venta={valor_venta}"
                            pred_response = requests.get(url_pred)

                            if pred_response.status_code == 200:
                                pred_data = pred_response.json()['data']
                                dias = pred_data['dias_estimados_pago']
                                fecha_estimada = datetime.today() + timedelta(days=int(dias))
                                
                                st.markdown(f"""
                                <div class="insecap-card fade-in">
                                    <h3>Predicción de Pago para {nombre_cliente}</h3>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; text-align: left; margin-top: 1rem;">
                                        <div>
                                            <p><strong>💰 Valor de venta:</strong> ${valor_venta:,.0f}</p>
                                            <p><strong>📅 Días estimados:</strong> {dias} días</p>
                                            <p><strong>🗓️ Fecha estimada:</strong> {fecha_estimada.strftime('%d/%m/%Y')}</p>
                                            <p><strong>📊 Rango de pago:</strong> {pred_data['dias_pago_min']} - {pred_data['dias_pago_max']} días</p>
                                            <p><strong>💡 Recomendación:</strong> {'✅ Aprobar con condiciones estándar' if dias <= 30 else '🕒 Requiere seguimiento especial' if dias <= 60 else '⚠️ Considerar garantías adicionales'}</p>
                                        </div>
                                        <div>
                                            <p><strong>✅ % Pago promedio:</strong> {pred_data['porcentaje_pago_promedio']*100:.1f}%</p>
                                            <p><strong>💵 Total vendido:</strong> ${pred_data['total_vendido']:,}</p>
                                            <p><strong>💸 Total pagado:</strong> ${pred_data['total_pagado']:,}</p>
                                            <p><strong>🏷️ Perfil:</strong> {pred_data['perfil']}</p>
                                            <p><strong>{'🟢 Riesgo: Bajo' if dias <= 30 else '🟡 Riesgo: Medio' if dias <= 60 else '🔴 Riesgo: Alto'}</strong></p>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("❌ Error al obtener la predicción del servidor.")
                        except Exception as e:
                            st.error(f"❌ Error de conexión: {str(e)}")
            else:
                st.warning("⚠️ No se pudo obtener información del cliente. Verifica el nombre ingresado.")
        except Exception as e:
            st.error(f"❌ Error de conexión con el servidor: {str(e)}")


# --- Sección: Líderes Comerciales ---
elif seccion == "👥 Líderes Comerciales":
    st.markdown("<h2 class='section-title'>👥 Análisis de Líderes Comerciales</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        correo_lider = st.text_input("Buscar vendedor/líder comercial:", placeholder="Ej: krojas@insecap.cl, projas@insecap.cl ...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_lider_btn = st.button("🔍 Buscar Líder", use_container_width=True)

    if correo_lider and (buscar_lider_btn or correo_lider):
        try:
            url_lideres_comerciales = f"http://127.0.0.1:8000/clientes/tiempos_etapa_lider/{correo_lider}"
            response_lideres_comerciales = requests.get(url_lideres_comerciales)
            if response_lideres_comerciales.status_code == 200:
                data_lideres_comerciales = response_lideres_comerciales.json()

                st.markdown(f"<h3 class='section-title'>👤 Líder Comercial: {correo_lider}</h3>", unsafe_allow_html=True)

                st.markdown(f"""
                    <div class="insecap-card fade-in">
                        <h4>📊 Total de comercializaciones</h4>
                        <h3>{data_lideres_comerciales["total_comercializaciones_lider"]:.1f} días</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Datos simulados mejorados
                tiempos_lider = [data_lideres_comerciales["promedio_dias_proceso_a_termino"], 
                                 data_lideres_comerciales["promedio_dias_termino_a_factura"],
                                 data_lideres_comerciales["promedio_dias_factura_a_pago"]]
                etapas = ['En Proceso → Terminado', 'Terminado → Facturado', 'Facturado → Pagado']

                # Gráfico mejorado
                st.markdown("### 📊 Tiempos Promedio por Etapa")
                
                fig, ax = plt.subplots(figsize=(12, 6))
                bars = ax.bar(etapas, tiempos_lider, color=['#485CC7', '#00B8DE', '#20B2AA'])
                
                # Personalizar el gráfico
                ax.set_ylabel("Días", fontsize=12, fontweight='bold')
                ax.set_title("Tiempos Promedio por Etapa del Vendedor", fontsize=14, fontweight='bold', pad=20)
                ax.set_ylim(0, max(tiempos_lider) * 1.2)
                
                # Agregar valores en las barras
                for bar, value in zip(bars, tiempos_lider):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{value} días', ha='center', va='bottom', fontweight='bold')
                
                # Estilizar
                ax.grid(axis='y', alpha=0.3)
                ax.set_facecolor('#f8f9fa')
                plt.xticks(rotation=15, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig)
            else: 
                st.warning("⚠️ No se pudo obtener información de los lideres comerciales. El servidor respondió con un estado no exitoso.")
        except:
            st.error("❌ No se pudo obtener información de los lideres comerciales desde el servidor. Verifica la conexión o intenta más tarde.")


# --- Sección: Destacados ---
elif seccion == "🏆 Destacados":
    st.markdown("<h3 class='section-title'>🏆 Empresas Destacadas</h3>", unsafe_allow_html=True)
    
    try:
        url_destacados = f"http://127.0.0.1:8000/comercializaciones/destacados"
        response_destacados = requests.get(url_destacados)
        if response_destacados.status_code == 200:
            data_destacados = response_destacados.json()
            data_clientes_dest = data_destacados["top_clientes"]
            data_lideres_dest = data_destacados["top_lideres"]
           
            # Mostrar top 3 con medallas
            cols = st.columns(3)
            medallas = ["🥇", "🥈", "🥉"]

            for idx in range(min(3, len(data_clientes_dest))):
                cliente = data_clientes_dest[idx]
                with cols[idx]:
                    st.markdown(f"""
                    <div class="destacado-card">
                        <h3>{medallas[idx]} {cliente['nombre_cliente']}</h3>
                        <h2>{cliente['promedio_dias_pago']} días</h2>
                        <p>Promedio de pago</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Tabla completa expandible
            with st.expander("📊 Ver Top Clientes"):
                top_10_data_cliente = []
                for i, cliente in enumerate(data_clientes_dest):
                    top_10_data_cliente.append({
                        "Posición": i + 1,
                        "Nombre": cliente['nombre_cliente'],
                        "Días Promedio": f"{cliente['promedio_dias_pago']} días",
                        "Facturas Pagadas": cliente['facturas_pagadas']
                    })

                df_top_10_cliente = pd.DataFrame(top_10_data_cliente)
                st.dataframe(df_top_10_cliente, use_container_width=True)

            # Líderes comerciales destacados (simulado)
            st.markdown("<h3 class='section-title'>🌟 Líderes Comerciales Destacados</h3>", unsafe_allow_html=True)

            # Mostrar top 3 con medallas
            cols = st.columns(3)
            medallas = ["🥇", "🥈", "🥉"]

            for idx in range(min(3, len(data_lideres_dest))):
                lider = data_lideres_dest[idx]
                with cols[idx]:
                    st.markdown(f"""
                    <div class="destacado-card">
                        <h3>{medallas[idx]} {lider['lider_comercial']}</h3>
                        <h2>{lider['promedio_dias_pago']} días</h2>
                        <p>Promedio de pago</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Tabla completa expandible
            with st.expander("📊 Ver Top Lideres comerciales"):
                top_10_data_lider = []
                for i, lider in enumerate(data_lideres_dest):
                    top_10_data_lider.append({
                        "Posición": i + 1,
                        "Correo": lider['lider_comercial'],
                        "Días Promedio": f"{lider['promedio_dias_pago']} días",
                        "Facturas pagadas": lider['facturas_pagadas']
                    })

                df_top_10_lider = pd.DataFrame(top_10_data_lider)
                st.dataframe(df_top_10_lider, use_container_width=True)
        else:
            st.warning("⚠️ No se pudo obtener información destacada. El servidor respondió con un estado no exitoso.")
    except:
        st.error("❌ No se pudo obtener información destacada desde el servidor. Verifica la conexión o intenta más tarde.")

