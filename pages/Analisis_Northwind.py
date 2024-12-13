import sys
from pathlib import Path
import plotly.express as px
import streamlit as st

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import * 

<<<<<<< HEAD
# primer grafico 



#segundo grafico
# Contenedor para los sliders
with st.container():
    # Crear columnas para los sliders
    col1, col2 = st.columns(2)

    # Slider para el rango de Precio de Producto en la primera columna
    with col1:
        rango_precio_producto = st.slider(
            'Rango de Precio de Producto',
            min_value=float(precio_combinado['Precio_de_producto'].min()),
            max_value=float(precio_combinado['Precio_de_producto'].max()),
            value=(float(precio_combinado['Precio_de_producto'].min()), 
                   float(precio_combinado['Precio_de_producto'].max()))
        )

    # Slider para el rango de Precio de Orden en la segunda columna
    with col2:
        rango_precio_orden = st.slider(
            'Rango de Precio de Orden',
            min_value=float(precio_combinado['Precio_Orden'].min()),
            max_value=float(precio_combinado['Precio_Orden'].max()),
            value=(float(precio_combinado['Precio_Orden'].min()), 
                   float(precio_combinado['Precio_Orden'].max()))
        )

# Crear las máscaras para filtrar los datos según los valores seleccionados en los sliders
=======
# Mostrar las tarjetas con información clave
col1, col2 = st.columns(2)

# Tarjeta 1: Producto más vendido
col1.metric("Producto Más Vendido", conexion_ordenada.iloc[0]["ProductName"], f"{conexion_ordenada.iloc[0]['Cantidad']} Unidades")

# Tarjeta 2: Precio promedio de producto
precio_promedio = precio_producto["Precio_de_producto"].mean()
col2.metric("Precio Promedio de Producto", f"$ {precio_promedio:.2f}")



# Filtro  1
producto_seleccionado = st.sidebar.selectbox(
    "Selecciona un producto para los gráficos:",
    ["Todos los productos"] + conexion_ordenada["ProductName"].tolist()
)

# Filtro dos
rango_precio_producto = st.sidebar.slider(
    'Selecciona el rango de precio de producto:',
    min_value=float(precio_combinado['Precio_de_producto'].min()),
    max_value=float(precio_combinado['Precio_de_producto'].max()),
    value=(float(precio_combinado['Precio_de_producto'].min()), 
           float(precio_combinado['Precio_de_producto'].max()))
)

# Filtro 3
rango_precio_orden = st.sidebar.slider(
    'Selecciona el rango de precio de orden:',
    min_value=float(precio_combinado['Precio_Orden'].min()),
    max_value=float(precio_combinado['Precio_Orden'].max()),
    value=(float(precio_combinado['Precio_Orden'].min()), 
           float(precio_combinado['Precio_Orden'].max()))
)

# Filtrar los datos según el producto seleccionado y los rangos de precios
if producto_seleccionado != "Todos los productos":
    conexion_ordenada = conexion_ordenada[conexion_ordenada["ProductName"] == producto_seleccionado]

# Crear las máscaras para los rangos de precio
>>>>>>> 965f198ccad5a059079c939faf1862b615bdbd2b
mask_precio_producto = (precio_combinado['Precio_de_producto'] >= rango_precio_producto[0]) & \
                        (precio_combinado['Precio_de_producto'] <= rango_precio_producto[1])

mask_precio_orden = (precio_combinado['Precio_Orden'] >= rango_precio_orden[0]) & \
                    (precio_combinado['Precio_Orden'] <= rango_precio_orden[1])

# Filtrar los datos con las máscaras
precio_combinado_filtrado = precio_combinado[mask_precio_producto & mask_precio_orden]

<<<<<<< HEAD
# Crear el gráfico de dispersión con los datos filtrados
fig = px.scatter(
=======
# Primer gráfico: Productos más vendidos
grafico1 = px.bar(
    conexion_ordenada,
    x="ProductName",
    y="Cantidad",
    title="Top 10 Productos Más Vendidos",
    labels={"ProductName": "Producto", "Cantidad": "Cantidad Vendida"},
    color="Cantidad",
    color_continuous_scale="Blues"
)

st.plotly_chart(grafico1)

# Segundo gráfico: Relación entre precios de productos y órdenes de compra (con los filtros aplicados)
fig2 = px.scatter(
>>>>>>> 965f198ccad5a059079c939faf1862b615bdbd2b
    precio_combinado_filtrado, 
    x='Precio_de_producto', 
    y='Precio_Orden', 
    title='Relación entre precios de productos y órdenes de compra',
    labels={'Precio_de_producto': 'Precio de Producto', 'Precio_Orden': 'Precio de Orden'}
)

<<<<<<< HEAD
# Ajustar los títulos de los ejes
fig.update_layout(
=======
# Ajustar los títulos 
fig2.update_layout(
>>>>>>> 965f198ccad5a059079c939faf1862b615bdbd2b
    xaxis_title='Precio de Producto',
    yaxis_title='Precio de Orden'
)

<<<<<<< HEAD
# Mostrar el gráfico
st.plotly_chart(fig, key='grafico_precio_combinado')



# tercer grafico 

# Contenedor para los widgets y el gráfico
with st.container():
    # Widget para decidir si filtrar por región
    filtrar_region = st.selectbox('Selecciona la Región de Envío para Filtrar', ['Todos'] + list(agrupado['ShipRegion'].unique()))

    # Si el usuario selecciona 'Todos', no filtramos. Si selecciona una región, aplicamos el filtro.
    if filtrar_region != 'Todos':
        mask_region = agrupado['ShipRegion'] == filtrar_region
        agrupado = agrupado[mask_region]
    
    # Crear el gráfico
    fig = px.bar(agrupado, 
=======
st.plotly_chart(fig2)

# Tercer gráfico
with st.container():
    filtrar_region = st.selectbox('Selecciona la Región de Envío para Filtrar', ['Todos'] + list(agrupado['ShipRegion'].unique()))

    if filtrar_region != 'Todos':
        mask_region = agrupado['ShipRegion'] == filtrar_region
        agrupado = agrupado[mask_region]

    grafico3 = px.bar(agrupado, 
>>>>>>> 965f198ccad5a059079c939faf1862b615bdbd2b
                 x='ShipRegion', 
                 y='conteo_acomulado', 
                 title=f'Cantidad Acumulada por Región de Envío (Filtrado: {filtrar_region})',
                 labels={'ShipRegion': 'Región de Envío', 'conteo_acomulado': 'Cantidad Acumulada'})

<<<<<<< HEAD
    # Mostrar el gráfico en el contenedor
    st.plotly_chart(fig)
=======
    st.plotly_chart(grafico3)
>>>>>>> 965f198ccad5a059079c939faf1862b615bdbd2b
