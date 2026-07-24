import streamlit as st
import pandas as pd
import plotly.express as px
from faker import Faker
import random

# Configuración de la página
st.set_page_config(page_title="Fisiocore Analytics", page_icon="📈", layout="wide")

st.title("📊 Fisiocore Analytics - Panel Clínico")
st.write("Monitoreo de pacientes, sesiones de fisioterapia y estadísticas en tiempo real.")

# Generador de datos simulados con Faker
@st.cache_data
def generar_datos():
    fake = Faker('es_ES')
    nombres_lesiones = ['Esguince de tobillo', 'Lumbalgia', 'Tendinitis rotuliana', 'Cervicalgia', 'Pubalgia', 'Fascitis plantar']
    estados = ['En tratamiento', 'Alta médica', 'Evaluación inicial']
    
    registros = []
    for i in range(1, 101):
        registros.append({
            'ID_Paciente': f"PAC-{1000 + i}",
            'Nombre': fake.name(),
            'Edad': random.randint(18, 70),
            'Lesion': random.choice(nombres_lesiones),
            'Sesiones_Realizadas': random.randint(1, 15),
            'Estado': random.choice(estados),
            'Costo_Sesion': round(random.uniform(25.0, 60.0), 2)
        })
    return pd.DataFrame(registros)

# Cargar los datos
df = generar_datos()

# Métricas superiores (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Total Pacientes", len(df))
col2.metric("Edad Promedio", f"{df['Edad'].mean():.1f} años")
col3.metric("Ingreso Promedio por Sesión", f"${df['Costo_Sesion'].mean():.2f}")

st.markdown("---")

# Filtros laterales o en pantalla
lesion_seleccionada = st.selectbox("Filtrar por tipo de lesión:", ["Todas"] + list(df['Lesion'].unique()))
if lesion_seleccionada != "Todas":
    df_filtrado = df[df['Lesion'] == lesion_seleccionada]
else:
    df_filtrado = df

# Gráficos con Plotly
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Distribución por Lesiones")
    fig_lesiones = px.pie(df, names='Lesion', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig_lesiones, use_container_width=True)

with col_g2:
    st.subheader("Sesiones Realizadas por Lesión")
    fig_sesiones = px.bar(df_filtrado, x='Lesion', y='Sesiones_Realizadas', color='Estado', barmode='group')
    st.plotly_chart(fig_sesiones, use_container_width=True)

# Tabla interactiva
st.subheader("Registro Detallado de Pacientes")
st.dataframe(df_filtrado, use_container_width=True)
