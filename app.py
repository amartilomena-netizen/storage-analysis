import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Storage Analysis", layout="wide")

st.title("📊 Storage Analysis – HDD vs SSD vs Cinta vs Nube")
st.markdown("Este dashboard compara tecnologías de almacenamiento en criterios de **costo, velocidad, fiabilidad y escalabilidad**.")

# ---------------------------
# Datos base
# ---------------------------
data = {
    "Tecnología": ["HDD", "SSD", "Cinta", "Nube"],
    "Lectura_MBps": [150, 500, 100, 200],
    "Escritura_MBps": [130, 480, 90, 180],
    "Capacidad_TB": [10, 4, 50, 9999],  # 9999 como proxy de "ilimitado"
    "Costo_USD_GB": [0.03, 0.10, 0.01, 0.02],
    "Fiabilidad_MTBF": [1_500_000, 2_000_000, 5_000_000, 0],
    "Consumo_W": [8, 4, 1, 0],
    "Seguridad": [3, 4, 3, 5],
    "Escalabilidad": [4, 3, 2, 5]
}

df = pd.DataFrame(data)
st.subheader("📋 Tabla comparativa")
st.dataframe(df, use_container_width=True)

# ---------------------------
# Gráfico: Velocidades
# ---------------------------
st.subheader("⚡ Velocidades de Lectura y Escritura (MB/s)")
fig, ax = plt.subplots()
df.plot(x="Tecnología", y=["Lectura_MBps", "Escritura_MBps"], kind="bar", ax=ax)
ax.set_ylabel("MB/s")
st.pyplot(fig)

# ---------------------------
# Gráfico: Costo por GB
# ---------------------------
st.subheader("💲 Costo por GB (USD)")
fig2, ax2 = plt.subplots()
df.plot(x="Tecnología", y="Costo_USD_GB", kind="bar", ax=ax2)
ax2.set_ylabel("USD por GB")
st.pyplot(fig2)

# ---------------------------
# Radar chart cualitativo (Fiabilidad, Seguridad, Escalabilidad)
# ---------------------------
import numpy as np

st.subheader("🕸️ Comparación Cualitativa (1–5)")

labels = ["Fiabilidad", "Seguridad", "Escalabilidad"]
num_vars = len(labels)

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # cerrar círculo

fig3, ax3 = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

for i, row in df.iterrows():
    values = [
        3 if row["Fiabilidad_MTBF"] < 2_000_000 else
        4 if row["Fiabilidad_MTBF"] < 5_000_000 else 5,
        row["Seguridad"],
        row["Escalabilidad"]
    ]
    values += values[:1]
    ax3.plot(angles, values, label=row["Tecnología"])
    ax3.fill(angles, values, alpha=0.1)

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(labels)
ax3.set_yticks([1, 2, 3, 4, 5])
ax3.set_ylim(0, 5)
ax3.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
st.pyplot(fig3)

st.markdown("📌 Nota: Los valores son **de referencia** y pueden variar según fabricante/proveedor. Este análisis es orientativo.")
