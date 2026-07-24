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

# Función para cargar y limpiar los datos desde el archivo CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("base_datos_clinica.csv")
    
    # Formatear teléfonos a "xxxx-xxxx" si existe la columna
    for col in ['Telefono', 'Tel', 'Celular', 'telefono', 'tel']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\D', '', regex=True)
            df[col] = df[col].apply(lambda x: f"{x[:4]}-{x[4:]}" if len(x) == 8 else x)
            
    return df

try:
    df = cargar_datos()

    # Nombres exactos de tus columnas según tu archivo
    col_edad = 'Edad' if 'Edad' in df.columns else None
    col_lesion = 'Diagnostico' if 'Diagnostico' in df.columns else None
    col_costo = 'Costo_Sesion' if 'Costo_Sesion' in df.columns else None
    col_estado = 'Estado_Cita' if 'Estado_Cita' in df.columns else None

    # Métricas principales (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Pacientes", len(df))
    
    if col_edad:
        edad_promedio = int(df[col_edad].mean())
        col2.metric("Edad Promedio", f"{edad_promedio} años")
    else:
        col2.metric("Edad Promedio", "N/D")
    
    if col_costo:
        col3.metric("Ingreso Promedio", f"${df[col_costo].mean():.2f}")
    else:
        col3.metric("Ingreso Promedio", "N/D")

    st.markdown("---")

    # Filtro interactivo por Diagnóstico
    df_filtrado = df
    if col_lesion:
        opciones = ["Todas"] + list(df[col_lesion].dropna().unique())
        seleccion = st.selectbox("Filtrar por Diagnóstico:", opciones)
        
        if seleccion != "Todas":
            df_filtrado = df[df[col_lesion] == seleccion]

    # Sección de Gráficos
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Distribución por Diagnóstico")
        if col_lesion:
            fig_pie = px.pie(df, names=col_lesion, hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Diagnostico'.")

    with col_g2:
        st.subheader("Citas por Diagnóstico y Estado")
        if col_lesion and col_costo:
            fig_bar = px.bar(df_filtrado, x=col_lesion, y=col_costo, color=col_estado if col_estado else None, barmode='group')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Faltan columnas para generar el gráfico de barras.")

    # Tabla interactiva con los datos limpios
    st.subheader("Registro Detallado de Pacientes")
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error("⚠️ No se pudo cargar el archivo 'base_datos_clinica.csv'. Asegúrate de subir tu archivo CSV con ese nombre exacto a GitHub.")
    st.info(f"Detalle técnico del error: {e}")
