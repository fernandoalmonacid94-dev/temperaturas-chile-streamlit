import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Temperaturas en Chile - 2023", layout="wide")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("temperaturas_chile_2023.csv")
    return df

df = cargar_datos()

st.title("🌡️ Temperaturas en Chile — Segundo semestre 2023")
st.markdown("Datos de estaciones meteorológicas obtenidos vía API pública de datos.gob.cl")

st.sidebar.header("Filtros")
estaciones = sorted(df["nombre_estacion"].unique())
estaciones_seleccionadas = st.sidebar.multiselect("Estaciones", estaciones, default=estaciones[:5])

meses_disponibles = sorted(df["mes"].unique())
meses_seleccionados = st.sidebar.multiselect("Meses", meses_disponibles, default=meses_disponibles)

df_filtrado = df[df["nombre_estacion"].isin(estaciones_seleccionadas) & df["mes"].isin(meses_seleccionados)]

st.write(f"Mostrando {len(df_filtrado)} registros de {len(estaciones_seleccionadas)} estaciones")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Comparación entre estaciones")
    promedio = df_filtrado.groupby("nombre_estacion")[["temp_min", "temp_max"]].mean().round(1).sort_values("temp_max", ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.barh(promedio.index, promedio["temp_max"], color="tomato")
    ax.set_xlabel("Temperatura máxima promedio (°C)")
    st.pyplot(fig)

with col2:
    st.subheader("Evolución mensual")
    evolucion = df_filtrado.groupby("mes")[["temp_min", "temp_max"]].mean().round(1)
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.plot(evolucion.index, evolucion["temp_max"], marker="o", label="Máxima", color="tomato")
    ax2.plot(evolucion.index, evolucion["temp_min"], marker="o", label="Mínima", color="steelblue")
    ax2.legend()
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("°C")
    st.pyplot(fig2)

st.subheader("Datos filtrados")
st.dataframe(df_filtrado)

