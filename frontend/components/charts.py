"""
Componentes de gráficos para el dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict


def plot_consumption_vs_prediction(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de consumo real vs predicho
    
    Args:
        df: DataFrame con columnas 'timestamp', 'real', 'predicted'
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['real'],
        mode='lines',
        name='Consumo Real',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['predicted'],
        mode='lines',
        name='Consumo Predicho',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Consumo Real vs Predicho',
        xaxis_title='Fecha y Hora',
        yaxis_title='Consumo (kWh)',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_consumption_by_hour(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de consumo promedio por hora del día
    
    Args:
        df: DataFrame con columna 'hora' y 'consumo'
    """
    hourly_avg = df.groupby('hora')['consumo'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=hourly_avg['hora'],
        y=hourly_avg['consumo'],
        marker=dict(
            color=hourly_avg['consumo'],
            colorscale='Viridis'
        )
    ))
    
    fig.update_layout(
        title='Consumo Promedio por Hora del Día',
        xaxis_title='Hora del Día',
        yaxis_title='Consumo Promedio (kWh)',
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def plot_consumption_by_day(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de consumo por día de la semana
    
    Args:
        df: DataFrame con columna 'dia_semana' y 'consumo'
    """
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    daily_avg = df.groupby('dia_semana')['consumo'].mean().reset_index()
    daily_avg['dia_nombre'] = daily_avg['dia_semana'].apply(lambda x: days[x] if x < 7 else 'N/A')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily_avg['dia_nombre'],
        y=daily_avg['consumo'],
        marker=dict(color='skyblue')
    ))
    
    fig.update_layout(
        title='Consumo Promedio por Día de la Semana',
        xaxis_title='Día de la Semana',
        yaxis_title='Consumo Promedio (kWh)',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_consumption_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histograma de distribución del consumo
    
    Args:
        df: DataFrame con columna 'consumo'
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['consumo'],
        nbinsx=50,
        marker=dict(color='lightblue', line=dict(color='black', width=1))
    ))
    
    fig.update_layout(
        title='Distribución del Consumo Energético',
        xaxis_title='Consumo (kWh)',
        yaxis_title='Frecuencia',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_cluster_distribution(cluster_data: Dict) -> go.Figure:
    """
    Gráfico de distribución de clusters
    
    Args:
        cluster_data: Diccionario con información de clusters
    """
    fig = go.Figure()
    
    clusters = list(cluster_data.keys())
    counts = list(cluster_data.values())
    
    fig.add_trace(go.Pie(
        labels=clusters,
        values=counts,
        hole=0.4,
        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ))
    
    fig.update_layout(
        title='Distribución de Clusters de Consumo',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_temperature_vs_consumption(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot de temperatura vs consumo
    
    Args:
        df: DataFrame con columnas 'temperatura' y 'consumo'
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['temperatura'],
        y=df['consumo'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['consumo'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Consumo (kWh)')
        )
    ))
    
    fig.update_layout(
        title='Relación entre Temperatura y Consumo',
        xaxis_title='Temperatura (°C)',
        yaxis_title='Consumo (kWh)',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_time_series(df: pd.DataFrame, column: str = 'consumo') -> go.Figure:
    """
    Gráfico de serie temporal
    
    Args:
        df: DataFrame con columnas 'timestamp' y el valor a graficar
        column: Nombre de la columna a graficar
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df[column],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#1f77b4', width=1)
    ))
    
    fig.update_layout(
        title=f'Serie Temporal de {column.capitalize()}',
        xaxis_title='Fecha y Hora',
        yaxis_title=f'{column.capitalize()} (kWh)',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    return fig


def plot_gauge(value: float, max_value: float, title: str) -> go.Figure:
    """
    Gráfico de medidor (gauge)
    
    Args:
        value: Valor actual
        max_value: Valor máximo
        title: Título del medidor
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value * 0.7},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                {'range': [max_value * 0.5, max_value * 0.75], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300, template='plotly_white')
    
    return fig
