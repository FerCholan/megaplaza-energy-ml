"""
Dashboard Principal - Sistema de Optimización Energética
Mega Plaza Chimbote
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.api_client import APIClient
from components.charts import (
    plot_consumption_vs_prediction,
    plot_time_series,
    plot_gauge
)

# Configuración de la página
st.set_page_config(
    page_title="Mega Plaza Energy - Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar cliente API
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()

# Sidebar
with st.sidebar:
    st.title("⚡ Mega Plaza Energy")
    st.markdown("### Sistema de Optimización Energética")
    st.markdown("---")
    
    # Filtros
    st.markdown("### Filtros")
    date_range = st.date_input(
        "Rango de fechas",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )
    
    area_filter = st.selectbox(
        "Área",
        ["Todas", "Piso 1", "Piso 2", "Piso 3", "Estacionamiento"]
    )
    
    st.markdown("---")
    st.markdown("### Información")
    st.info("Dashboard en tiempo real para monitoreo y predicción de consumo energético")

# Título principal
st.title("📊 Dashboard de Consumo Energético")
st.markdown("### Mega Plaza Chimbote - Monitoreo en Tiempo Real")

# Obtener datos (mock data si la API no está disponible)
try:
    # Intentar obtener datos reales de la API
    stats = st.session_state.api_client.get_consumption_stats(days=7)
    realtime_data = st.session_state.api_client.get_realtime_consumption(hours=24)
    
    if not stats:
        # Datos de ejemplo si la API no está disponible
        stats = {
            "average_kwh": 750.5,
            "min_kwh": 450.2,
            "max_kwh": 1200.8,
            "total_kwh": 126090
        }
except Exception:
    # Datos de ejemplo
    stats = {
        "average_kwh": 750.5,
        "min_kwh": 450.2,
        "max_kwh": 1200.8,
        "total_kwh": 126090
    }
    realtime_data = []

# KPIs principales
st.markdown("### 📈 Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Consumo Actual",
        value=f"{stats.get('average_kwh', 750):.1f} kWh",
        delta="-5.2%"
    )

with col2:
    st.metric(
        label="Predicción (1h)",
        value=f"{stats.get('average_kwh', 750) * 1.05:.1f} kWh",
        delta="+5.0%"
    )

with col3:
    st.metric(
        label="Diferencia",
        value=f"{stats.get('average_kwh', 750) * 0.05:.1f} kWh",
        delta="Normal"
    )

with col4:
    st.metric(
        label="Total Semanal",
        value=f"{stats.get('total_kwh', 126090) / 1000:.1f} MWh",
        delta="-2.3%"
    )

st.markdown("---")

# Gráficos principales
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📉 Consumo Real vs Predicho (Últimas 24h)")
    
    # Generar datos de ejemplo
    hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
    consumption_data = pd.DataFrame({
        'timestamp': hours,
        'real': np.random.normal(750, 100, 24),
        'predicted': np.random.normal(755, 95, 24)
    })
    
    fig_comparison = plot_consumption_vs_prediction(consumption_data)
    st.plotly_chart(fig_comparison, use_container_width=True)

with col_right:
    st.markdown("### 🎯 Objetivo de Eficiencia")
    
    # Medidor de eficiencia
    current_efficiency = 85.5
    fig_gauge = plot_gauge(current_efficiency, 100, "Eficiencia Actual (%)")
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Información adicional
    st.success("✅ Objetivo: 90% de eficiencia")
    st.info(f"📊 Actual: {current_efficiency}%")
    st.warning("⚠️ Falta: {:.1f}%".format(90 - current_efficiency))

st.markdown("---")

# Serie temporal semanal
st.markdown("### 📅 Evolución del Consumo Semanal")

# Generar datos de ejemplo
days = pd.date_range(end=datetime.now(), periods=168, freq='H')
weekly_data = pd.DataFrame({
    'timestamp': days,
    'consumo': np.random.normal(750, 150, 168) + 
               np.sin(np.arange(168) * 2 * np.pi / 24) * 100
})

fig_weekly = plot_time_series(weekly_data, 'consumo')
st.plotly_chart(fig_weekly, use_container_width=True)

st.markdown("---")

# Alertas y Recomendaciones
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔔 Últimas Alertas")
    
    # Obtener alertas (mock data si falla)
    try:
        alerts = st.session_state.api_client.get_active_alerts(limit=5)
        if not alerts:
            alerts = [
                {
                    "tipo": "high_consumption",
                    "mensaje": "Consumo alto detectado en Piso 2",
                    "severity": "high",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "tipo": "anomaly",
                    "mensaje": "Patrón anómalo en horario nocturno",
                    "severity": "medium",
                    "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
                }
            ]
    except Exception:
        alerts = []
    
    if alerts:
        for alert in alerts[:5]:
            severity_color = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }.get(alert.get("severity", "low"), "🔵")
            
            st.warning(
                f"{severity_color} **{alert.get('tipo', 'Alerta').upper()}**\n\n"
                f"{alert.get('mensaje', 'Sin mensaje')}\n\n"
                f"_Hace {(datetime.now() - datetime.fromisoformat(alert.get('timestamp', datetime.now().isoformat()).replace('Z', '+00:00'))).seconds // 3600} horas_"
            )
    else:
        st.info("✅ No hay alertas activas")

with col2:
    st.markdown("### 💡 Recomendaciones")
    
    st.success(
        "**Optimización de Horarios**\n\n"
        "Reducir el consumo en horarios pico (18:00-21:00) "
        "podría generar un ahorro del 15% mensual."
    )
    
    st.info(
        "**Mantenimiento Preventivo**\n\n"
        "Se recomienda revisar los equipos de climatización "
        "del Piso 2 por consumo anómalo detectado."
    )
    
    st.success(
        "**Eficiencia Energética**\n\n"
        "Implementar iluminación LED en áreas comunes "
        "podría reducir el consumo en un 20%."
    )

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Sistema de Optimización Energética - Mega Plaza Chimbote</p>
    <p>Desarrollado con Machine Learning y FastAPI</p>
</div>
""", unsafe_allow_html=True)
