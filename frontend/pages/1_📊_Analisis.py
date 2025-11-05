"""
Página de Análisis - Visualizaciones estadísticas del consumo
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
sys.path.append('..')

from utils.api_client import APIClient
from components.charts import (
    plot_consumption_by_hour,
    plot_consumption_by_day,
    plot_consumption_distribution,
    plot_temperature_vs_consumption
)

st.set_page_config(page_title="Análisis", page_icon="📊", layout="wide")

# Inicializar cliente API
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("📊 Análisis Estadístico del Consumo")
st.markdown("### Visualizaciones y métricas detalladas")

# Generar datos de ejemplo
np.random.seed(42)
hours_data = pd.DataFrame({
    'hora': range(24),
    'consumo': np.random.normal(750, 100, 24) + np.sin(np.arange(24) * 2 * np.pi / 24) * 150
})

days_data = pd.DataFrame({
    'dia_semana': range(7),
    'consumo': [780, 820, 810, 790, 800, 650, 600]
})

consumption_data = pd.DataFrame({
    'consumo': np.random.normal(750, 150, 1000)
})

temp_data = pd.DataFrame({
    'temperatura': np.random.normal(22, 5, 500),
    'consumo': np.random.normal(750, 120, 500) + np.random.normal(22, 5, 500) * 15
})

# Estadísticas generales
st.markdown("### 📈 Estadísticas Generales")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Media", f"{consumption_data['consumo'].mean():.1f} kWh")

with col2:
    st.metric("Mediana", f"{consumption_data['consumo'].median():.1f} kWh")

with col3:
    st.metric("Desv. Est.", f"{consumption_data['consumo'].std():.1f} kWh")

with col4:
    st.metric("Mínimo", f"{consumption_data['consumo'].min():.1f} kWh")

with col5:
    st.metric("Máximo", f"{consumption_data['consumo'].max():.1f} kWh")

st.markdown("---")

# Gráficos de análisis temporal
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⏰ Consumo por Hora del Día")
    fig_hour = plot_consumption_by_hour(hours_data)
    st.plotly_chart(fig_hour, use_container_width=True)
    
    st.info(
        "**Insight**: El consumo alcanza su pico entre las 18:00 y 21:00 horas, "
        "coincidiendo con el horario de mayor afluencia de visitantes."
    )

with col2:
    st.markdown("### 📅 Consumo por Día de la Semana")
    fig_day = plot_consumption_by_day(days_data)
    st.plotly_chart(fig_day, use_container_width=True)
    
    st.info(
        "**Insight**: Los fines de semana muestran un consumo menor debido a "
        "la reducción de operaciones administrativas."
    )

st.markdown("---")

# Distribución y relaciones
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Distribución del Consumo")
    fig_dist = plot_consumption_distribution(consumption_data)
    st.plotly_chart(fig_dist, use_container_width=True)
    
    st.success(
        "**Observación**: La distribución es aproximadamente normal, "
        "lo que facilita la aplicación de modelos predictivos."
    )

with col2:
    st.markdown("### 🌡️ Temperatura vs Consumo")
    fig_temp = plot_temperature_vs_consumption(temp_data)
    st.plotly_chart(fig_temp, use_container_width=True)
    
    st.warning(
        "**Correlación**: Existe una correlación positiva entre temperatura "
        "y consumo, principalmente por el uso de sistemas de climatización."
    )

st.markdown("---")

# Tabla de datos
st.markdown("### 📋 Tabla de Datos Detallada")

# Crear tabla de ejemplo
detailed_data = pd.DataFrame({
    'Fecha': pd.date_range(end=datetime.now(), periods=10, freq='D'),
    'Consumo Promedio (kWh)': np.random.normal(750, 50, 10),
    'Temperatura (°C)': np.random.normal(22, 3, 10),
    'Humedad (%)': np.random.normal(65, 10, 10),
    'Costo ($)': np.random.normal(750 * 0.12, 50 * 0.12, 10)
})

detailed_data['Fecha'] = detailed_data['Fecha'].dt.strftime('%Y-%m-%d')

# Formatear valores numéricos
detailed_data['Consumo Promedio (kWh)'] = detailed_data['Consumo Promedio (kWh)'].round(1)
detailed_data['Temperatura (°C)'] = detailed_data['Temperatura (°C)'].round(1)
detailed_data['Humedad (%)'] = detailed_data['Humedad (%)'].round(1)
detailed_data['Costo ($)'] = detailed_data['Costo ($)'].round(2)

st.dataframe(detailed_data, use_container_width=True, hide_index=True)

# Descarga de datos
csv = detailed_data.to_csv(index=False)
st.download_button(
    label="📥 Descargar datos CSV",
    data=csv,
    file_name=f"consumo_energia_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

st.markdown("---")

# Análisis de tendencias
st.markdown("### 📈 Análisis de Tendencias")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Tendencia Semanal",
        "-3.2%",
        delta="-3.2%",
        delta_color="normal"
    )
    st.caption("Comparado con la semana anterior")

with col2:
    st.metric(
        "Tendencia Mensual",
        "+5.8%",
        delta="+5.8%",
        delta_color="inverse"
    )
    st.caption("Comparado con el mes anterior")

with col3:
    st.metric(
        "Eficiencia",
        "87.5%",
        delta="+2.1%"
    )
    st.caption("Mejora en la eficiencia energética")
