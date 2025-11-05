"""
Página de Configuración - Gestión y configuración del sistema
"""
import streamlit as st
from datetime import datetime
import sys
sys.path.append('..')

from utils.api_client import APIClient

st.set_page_config(page_title="Configuración", page_icon="⚙️", layout="wide")

# Inicializar cliente API
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("⚙️ Configuración del Sistema")
st.markdown("### Gestión y configuración avanzada")

# Tabs para organizar configuración
tab1, tab2, tab3, tab4 = st.tabs([
    "🔧 General",
    "👥 Usuarios",
    "🤖 Modelos ML",
    "📊 Reportes"
])

# Tab 1: Configuración General
with tab1:
    st.markdown("### Configuración General")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Parámetros del Sistema")
        
        data_refresh_rate = st.selectbox(
            "Frecuencia de actualización de datos",
            ["Tiempo real", "1 minuto", "5 minutos", "15 minutos", "30 minutos"],
            index=2
        )
        
        timezone = st.selectbox(
            "Zona horaria",
            ["America/Lima", "UTC", "America/New_York"],
            index=0
        )
        
        language = st.selectbox(
            "Idioma",
            ["Español", "English"],
            index=0
        )
        
        theme = st.selectbox(
            "Tema visual",
            ["Claro", "Oscuro", "Auto"],
            index=0
        )
    
    with col2:
        st.markdown("#### Almacenamiento de Datos")
        
        retention_days = st.number_input(
            "Días de retención de datos",
            value=365,
            step=30,
            help="Datos más antiguos serán archivados"
        )
        
        backup_enabled = st.checkbox("Respaldo automático", value=True)
        
        if backup_enabled:
            backup_frequency = st.selectbox(
                "Frecuencia de respaldo",
                ["Diario", "Semanal", "Mensual"],
                index=0
            )
            
            backup_time = st.time_input(
                "Hora de respaldo",
                value=datetime.strptime("02:00", "%H:%M").time()
            )
        
        archive_old_data = st.checkbox("Archivar datos antiguos", value=True)
    
    if st.button("💾 Guardar Configuración General", type="primary"):
        st.success("✅ Configuración general guardada")

# Tab 2: Gestión de Usuarios
with tab2:
    st.markdown("### Gestión de Usuarios")
    
    # Lista de usuarios mock
    import pandas as pd
    
    users_df = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Email': [
            'admin@megaplaza.com',
            'operador@megaplaza.com',
            'analista@megaplaza.com',
            'supervisor@megaplaza.com'
        ],
        'Rol': ['Admin', 'Operador', 'Analista', 'Supervisor'],
        'Estado': ['Activo', 'Activo', 'Activo', 'Inactivo'],
        'Último Acceso': [
            '2024-01-15 14:30',
            '2024-01-15 13:45',
            '2024-01-15 09:20',
            '2024-01-10 16:15'
        ]
    })
    
    st.dataframe(users_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("#### Agregar Nuevo Usuario")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_email = st.text_input("Email")
    
    with col2:
        new_role = st.selectbox("Rol", ["Admin", "Operador", "Analista", "Supervisor"])
    
    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer
        if st.button("➕ Agregar Usuario"):
            st.success(f"✅ Usuario {new_email} agregado con rol {new_role}")
    
    st.markdown("---")
    
    st.markdown("#### Permisos por Rol")
    
    permissions_df = pd.DataFrame({
        'Permiso': [
            'Ver Dashboard',
            'Ver Análisis',
            'Configurar Alertas',
            'Gestionar Modelos ML',
            'Gestionar Usuarios',
            'Ver Reportes',
            'Exportar Datos'
        ],
        'Admin': ['✅', '✅', '✅', '✅', '✅', '✅', '✅'],
        'Supervisor': ['✅', '✅', '✅', '✅', '❌', '✅', '✅'],
        'Analista': ['✅', '✅', '✅', '❌', '❌', '✅', '✅'],
        'Operador': ['✅', '✅', '❌', '❌', '❌', '❌', '❌']
    })
    
    st.dataframe(permissions_df, use_container_width=True, hide_index=True)

# Tab 3: Modelos ML
with tab3:
    st.markdown("### Gestión de Modelos de Machine Learning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Estado de Modelos")
        
        st.info(
            "**Modelo de Predicción**\n\n"
            "- Tipo: XGBoost Regressor\n"
            "- Versión: v1.0\n"
            "- Última actualización: 2024-01-10\n"
            "- Estado: ✅ Activo\n"
            "- Precisión (R²): 0.8756"
        )
        
        if st.button("🔄 Re-entrenar Modelo de Predicción"):
            with st.spinner("Re-entrenando modelo..."):
                import time
                time.sleep(2)
            st.success("✅ Modelo re-entrenado exitosamente")
        
        st.markdown("---")
        
        st.success(
            "**Modelo de Clustering**\n\n"
            "- Tipo: K-Means\n"
            "- Versión: v1.0\n"
            "- Última actualización: 2024-01-10\n"
            "- Estado: ✅ Activo\n"
            "- Clusters: 3"
        )
        
        if st.button("🔄 Re-entrenar Modelo de Clustering"):
            with st.spinner("Re-entrenando modelo..."):
                import time
                time.sleep(2)
            st.success("✅ Modelo re-entrenado exitosamente")
    
    with col2:
        st.markdown("#### Configuración de Entrenamiento")
        
        st.write("**Predicción**")
        
        train_size = st.slider("Tamaño del conjunto de entrenamiento (%)", 60, 90, 80)
        
        n_estimators = st.number_input("Número de estimadores", value=100, step=10)
        
        max_depth = st.slider("Profundidad máxima", 3, 15, 6)
        
        learning_rate = st.select_slider(
            "Tasa de aprendizaje",
            options=[0.01, 0.05, 0.1, 0.15, 0.2],
            value=0.1
        )
        
        st.markdown("---")
        
        st.write("**Clustering**")
        
        n_clusters = st.slider("Número de clusters", 2, 10, 3)
        
        clustering_features = st.multiselect(
            "Features para clustering",
            [
                "consumo_energia",
                "temperatura_aire",
                "hora_del_dia",
                "dia_de_la_semana",
                "pies_cuadrados"
            ],
            default=[
                "consumo_energia",
                "temperatura_aire",
                "hora_del_dia",
                "dia_de_la_semana"
            ]
        )
        
        if st.button("💾 Guardar Configuración ML"):
            st.success("✅ Configuración de modelos guardada")
    
    st.markdown("---")
    
    st.markdown("#### Historial de Entrenamientos")
    
    training_history = pd.DataFrame({
        'Fecha': [
            '2024-01-15 10:30',
            '2024-01-10 02:15',
            '2024-01-05 02:15',
            '2024-01-01 02:15'
        ],
        'Modelo': [
            'Predicción',
            'Predicción',
            'Clustering',
            'Predicción'
        ],
        'Versión': ['v1.1', 'v1.0', 'v1.0', 'v0.9'],
        'R² Score': [0.8756, 0.8712, '-', 0.8650],
        'Estado': ['Activo', 'Archivado', 'Activo', 'Archivado']
    })
    
    st.dataframe(training_history, use_container_width=True, hide_index=True)

# Tab 4: Reportes
with tab4:
    st.markdown("### Generación de Reportes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Configuración del Reporte")
        
        report_type = st.selectbox(
            "Tipo de reporte",
            [
                "Consumo Diario",
                "Consumo Semanal",
                "Consumo Mensual",
                "Alertas",
                "Predicciones vs Real",
                "Análisis de Eficiencia",
                "Reporte Completo"
            ]
        )
        
        report_format = st.selectbox(
            "Formato",
            ["PDF", "Excel", "CSV", "HTML"]
        )
        
        include_charts = st.checkbox("Incluir gráficos", value=True)
        
        include_recommendations = st.checkbox("Incluir recomendaciones", value=True)
        
        date_range = st.date_input(
            "Rango de fechas",
            value=(datetime.now() - pd.Timedelta(days=30), datetime.now())
        )
    
    with col2:
        st.markdown("#### Reportes Programados")
        
        schedule_enabled = st.checkbox("Activar reportes automáticos", value=False)
        
        if schedule_enabled:
            schedule_frequency = st.selectbox(
                "Frecuencia",
                ["Diario", "Semanal", "Mensual"],
                index=2
            )
            
            schedule_day = st.selectbox(
                "Día de envío",
                ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
                index=0
            )
            
            schedule_time = st.time_input(
                "Hora de envío",
                value=datetime.strptime("08:00", "%H:%M").time()
            )
            
            recipients = st.text_area(
                "Destinatarios (emails separados por coma)",
                value="admin@megaplaza.com, supervisor@megaplaza.com"
            )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generar Reporte", type="primary"):
            with st.spinner("Generando reporte..."):
                import time
                time.sleep(2)
            st.success(f"✅ Reporte {report_type} generado en formato {report_format}")
            st.download_button(
                label="⬇️ Descargar Reporte",
                data="Contenido del reporte simulado",
                file_name=f"reporte_{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{report_format.lower()}",
                mime="application/octet-stream"
            )
    
    with col2:
        if schedule_enabled and st.button("💾 Guardar Programación"):
            st.success("✅ Reporte programado guardado")
    
    with col3:
        if st.button("📧 Vista Previa"):
            st.info("Vista previa del reporte disponible")
    
    st.markdown("---")
    
    st.markdown("#### Historial de Reportes")
    
    reports_history = pd.DataFrame({
        'Fecha Generación': [
            '2024-01-15 08:00',
            '2024-01-14 08:00',
            '2024-01-13 08:00'
        ],
        'Tipo': ['Consumo Mensual', 'Consumo Diario', 'Alertas'],
        'Formato': ['PDF', 'Excel', 'PDF'],
        'Estado': ['Enviado', 'Enviado', 'Enviado'],
        'Destinatarios': [2, 2, 3]
    })
    
    st.dataframe(reports_history, use_container_width=True, hide_index=True)

st.markdown("---")

# Información del sistema
st.markdown("### ℹ️ Información del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "**Versión**\n\n"
        "Sistema: v1.0.0\n\n"
        "API: v1.0.0\n\n"
        "Frontend: v1.0.0"
    )

with col2:
    st.success(
        "**Estado**\n\n"
        "API: ✅ Online\n\n"
        "Base de Datos: ✅ Online\n\n"
        "Redis: ✅ Online"
    )

with col3:
    st.warning(
        "**Mantenimiento**\n\n"
        "Próximo: 2024-02-01\n\n"
        "Último: 2024-01-01\n\n"
        "Frecuencia: Mensual"
    )
