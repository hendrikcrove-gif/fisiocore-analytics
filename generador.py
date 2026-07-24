import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Fisiocore Analytics",
    page_icon="🏥",
    layout="wide"
)

# ==========================================
# CONFIGURACIÓN DE LA CLÍNICA
# ==========================================
NOMBRE_CLINICA = "Fisiocore - Clínica de Fisioterapia"

st.title(f"📊 {NOMBRE_CLINICA}")
st.markdown("Panel de control y análisis de pacientes en tiempo real.")

# Función para cargar los datos limpios desde el archivo CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("base_datos_clinica.csv")
    return df

# Carga segura de datos
try:
    df = cargar_datos()

    # Métricas principales (KPIs) - Edad promedio redondeada como entero
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Pacientes", len(df))
    
    if 'Edad' in df.columns:
        edad_promedio = int(df['Edad'].mean())
        col2.metric("Edad Promedio", f"{edad_promedio} años")
    
    if 'Costo_Sesion' in df.columns:
        col3.metric("Ingreso Promedio por Sesión", f"${df['Costo_Sesion'].mean():.2f}")

    st.markdown("---")

    # Filtro interactivo si existe la columna 'Lesion'
    if 'Lesion' in df.columns:
        lesiones_disponibles = ["Todas"] + list(df['Lesion'].dropna().unique())
        lesion_seleccionada = st.selectbox("Filtrar por tipo de lesión:", lesiones_disponibles)
        
        if lesion_seleccionada != "Todas":
            df_filtrado = df[df['Lesion'] == lesion_seleccionada]
        else:
            df_filtrado = df
    else:
        df_filtrado = df

    # Sección de Gráficos
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Distribución por Lesión")
        if 'Lesion' in df.columns:
            fig_pie = px.pie(df, names='Lesion', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Lesion' en los datos.")

    with col_g2:
        st.subheader("Sesiones por Lesión y Estado")
        if 'Lesion' in df.columns and 'Sesiones_Realizadas' in df.columns:
            col_color = 'Estado' if 'Estado' in df.columns else None
            fig_bar = px.bar(df_filtrado, x='Lesion', y='Sesiones_Realizadas', color=col_color, barmode='group')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Faltan columnas de sesiones para graficar.")

    # Tabla interactiva con los datos finales
    st.subheader("Registro Detallado")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error("⚠️ No se pudo cargar el archivo 'base_datos_clinica.csv'. Asegúrate de subir tu archivo CSV con ese nombre exacto a GitHub.")
    st.info(f"Detalle técnico del error: {e}")
