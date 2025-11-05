"""
Página de Alertas - Configuración y visualización de alertas
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
sys.path.append('..')

from utils.api_client import APIClient

st.set_page_config(page_title="Alertas", page_icon="🔔", layout="wide")

# Inicializar cliente API
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("🔔 Sistema de Alertas")
st.markdown("### Configuración y monitoreo de alertas del sistema")

# Obtener estadísticas de alertas
try:
    alert_stats = st.session_state.api_client.get_alert_stats()
except Exception:
    alert_stats = {
        "total": 45,
        "active": 5,
        "resolved": 40,
        "by_severity": {"critical": 2, "high": 8, "medium": 15, "low": 20},
        "by_type": {"high_consumption": 20, "anomaly": 15, "prediction_error": 10}
    }

# Estadísticas generales
st.markdown("### 📊 Estadísticas de Alertas")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Alertas", alert_stats.get("total", 0))

with col2:
    st.metric("Alertas Activas", alert_stats.get("active", 0), delta="Requiere atención", delta_color="inverse")

with col3:
    st.metric("Alertas Resueltas", alert_stats.get("resolved", 0))

with col4:
    resolution_rate = (alert_stats.get("resolved", 0) / alert_stats.get("total", 1)) * 100
    st.metric("Tasa de Resolución", f"{resolution_rate:.1f}%")

st.markdown("---")

# Alertas activas
st.markdown("### 🚨 Alertas Activas")

# Datos de ejemplo
active_alerts = [
    {
        "id": 1,
        "timestamp": datetime.now() - timedelta(hours=1),
        "tipo": "high_consumption",
        "mensaje": "Consumo excede umbral en Piso 2",
        "severity": "high",
        "area": "Piso 2",
        "threshold_exceeded": 150.5
    },
    {
        "id": 2,
        "timestamp": datetime.now() - timedelta(hours=3),
        "tipo": "anomaly",
        "mensaje": "Patrón anómalo detectado en horario nocturno",
        "severity": "critical",
        "area": "General",
        "threshold_exceeded": 200.0
    },
    {
        "id": 3,
        "timestamp": datetime.now() - timedelta(hours=5),
        "tipo": "prediction_error",
        "mensaje": "Error de predicción superior al 30%",
        "severity": "medium",
        "area": "Estacionamiento",
        "threshold_exceeded": 85.2
    },
    {
        "id": 4,
        "timestamp": datetime.now() - timedelta(hours=12),
        "tipo": "high_consumption",
        "mensaje": "Consumo inusual en climatización",
        "severity": "high",
        "area": "Piso 3",
        "threshold_exceeded": 120.0
    },
    {
        "id": 5,
        "timestamp": datetime.now() - timedelta(hours=18),
        "tipo": "anomaly",
        "mensaje": "Incremento súbito de consumo",
        "severity": "medium",
        "area": "Piso 1",
        "threshold_exceeded": 95.5
    }
]

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    filter_severity = st.multiselect(
        "Severidad",
        ["critical", "high", "medium", "low"],
        default=["critical", "high", "medium"]
    )

with col2:
    filter_type = st.multiselect(
        "Tipo de Alerta",
        ["high_consumption", "anomaly", "prediction_error"],
        default=["high_consumption", "anomaly", "prediction_error"]
    )

with col3:
    filter_area = st.multiselect(
        "Área",
        ["General", "Piso 1", "Piso 2", "Piso 3", "Estacionamiento"],
        default=["General", "Piso 1", "Piso 2", "Piso 3", "Estacionamiento"]
    )

# Mostrar alertas
for alert in active_alerts:
    if alert["severity"] in filter_severity and alert["tipo"] in filter_type and alert["area"] in filter_area:
        # Mapeo de severidad a colores
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        
        severity_text = {
            "critical": "CRÍTICA",
            "high": "ALTA",
            "medium": "MEDIA",
            "low": "BAJA"
        }
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(
                    f"{severity_emoji.get(alert['severity'], '🔵')} "
                    f"**{alert['tipo'].upper().replace('_', ' ')}** - "
                    f"Severidad: {severity_text.get(alert['severity'], 'DESCONOCIDA')}"
                )
                st.write(alert['mensaje'])
                st.caption(
                    f"📍 {alert['area']} | "
                    f"⏰ {alert['timestamp'].strftime('%Y-%m-%d %H:%M')} | "
                    f"📈 Excede umbral en {alert['threshold_exceeded']:.1f} kWh"
                )
            
            with col2:
                if st.button("✅ Resolver", key=f"resolve_{alert['id']}"):
                    st.success(f"Alerta #{alert['id']} marcada como resuelta")
            
            with col3:
                if st.button("📋 Detalles", key=f"details_{alert['id']}"):
                    st.info(f"Mostrando detalles de alerta #{alert['id']}")
            
            st.markdown("---")

st.markdown("---")

# Configuración de alertas
st.markdown("### ⚙️ Configuración de Umbrales")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Umbrales de Consumo")
    
    high_consumption_threshold = st.number_input(
        "Umbral de consumo alto (kWh)",
        value=1000,
        step=50,
        help="Alerta cuando el consumo supere este valor"
    )
    
    anomaly_factor = st.slider(
        "Factor de anomalía",
        1.0, 3.0, 2.0, 0.1,
        help="Alerta cuando el consumo sea X veces mayor que la media"
    )
    
    prediction_error_threshold = st.slider(
        "Umbral de error de predicción (%)",
        10, 50, 30,
        help="Alerta cuando el error de predicción supere este porcentaje"
    )

with col2:
    st.markdown("#### Notificaciones")
    
    enable_email = st.checkbox("Activar notificaciones por email", value=True)
    
    if enable_email:
        notification_email = st.text_input(
            "Email para notificaciones",
            value="admin@megaplaza.com"
        )
    
    enable_webhook = st.checkbox("Activar webhook", value=False)
    
    if enable_webhook:
        webhook_url = st.text_input(
            "URL del webhook",
            placeholder="https://hooks.example.com/alerts"
        )
    
    notification_frequency = st.selectbox(
        "Frecuencia de resumen",
        ["Inmediato", "Cada hora", "Cada 6 horas", "Diario"]
    )

if st.button("💾 Guardar Configuración", type="primary"):
    st.success("✅ Configuración guardada exitosamente")
    st.balloons()

st.markdown("---")

# Historial de alertas
st.markdown("### 📜 Historial de Alertas")

# Datos de historial
historical_alerts = pd.DataFrame({
    'Fecha': pd.date_range(end=datetime.now(), periods=10, freq='D'),
    'Total': [8, 5, 12, 7, 9, 6, 11, 4, 10, 8],
    'Críticas': [1, 0, 2, 1, 1, 0, 2, 0, 1, 1],
    'Altas': [3, 2, 4, 2, 3, 2, 4, 1, 3, 3],
    'Medias': [4, 3, 6, 4, 5, 4, 5, 3, 6, 4]
})

historical_alerts['Fecha'] = historical_alerts['Fecha'].dt.strftime('%Y-%m-%d')

st.dataframe(historical_alerts, use_container_width=True, hide_index=True)

# Gráfico de tendencia
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=historical_alerts['Fecha'],
    y=historical_alerts['Total'],
    mode='lines+markers',
    name='Total de Alertas',
    line=dict(color='#1f77b4', width=2)
))

fig.update_layout(
    title='Tendencia de Alertas (Últimos 10 días)',
    xaxis_title='Fecha',
    yaxis_title='Número de Alertas',
    height=400,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Estadísticas por tipo y severidad
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Distribución por Severidad")
    
    severity_data = alert_stats.get("by_severity", {})
    severity_df = pd.DataFrame({
        'Severidad': list(severity_data.keys()),
        'Cantidad': list(severity_data.values())
    })
    
    import plotly.express as px
    fig_severity = px.pie(
        severity_df,
        values='Cantidad',
        names='Severidad',
        color='Severidad',
        color_discrete_map={
            'critical': '#FF0000',
            'high': '#FF6B00',
            'medium': '#FFD700',
            'low': '#00FF00'
        }
    )
    fig_severity.update_layout(height=300, template='plotly_white')
    st.plotly_chart(fig_severity, use_container_width=True)

with col2:
    st.markdown("#### Distribución por Tipo")
    
    type_data = alert_stats.get("by_type", {})
    type_df = pd.DataFrame({
        'Tipo': list(type_data.keys()),
        'Cantidad': list(type_data.values())
    })
    
    fig_type = px.bar(
        type_df,
        x='Cantidad',
        y='Tipo',
        orientation='h',
        color='Cantidad',
        color_continuous_scale='Blues'
    )
    fig_type.update_layout(height=300, template='plotly_white', showlegend=False)
    st.plotly_chart(fig_type, use_container_width=True)
