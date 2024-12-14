import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Setup path and imports
root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import * 

def display_key_metrics(conexion_ordenada, precio_producto):
    """Display key performance metrics in two columns."""
    col1, col2 = st.columns(2)
    
    # Top selling product
    col1.metric(
        "Producto Más Vendido", 
        conexion_ordenada.iloc[0]["ProductName"], 
        f"{conexion_ordenada.iloc[0]['Cantidad']} Unidades"
    )
    
    # Average product price
    precio_promedio = precio_producto["Precio_de_producto"].mean()
    col2.metric("Precio Promedio de Producto", f"$ {precio_promedio:.2f}")

def create_sidebar_filters(conexion_ordenada, precio_combinado):
    """Create sidebar filters for product selection and price ranges."""
    # Product selection filter
    producto_seleccionado = st.sidebar.selectbox(
        "Selecciona un producto para los gráficos:",
        ["Todos los productos"] + conexion_ordenada["ProductName"].tolist()
    )
    
    # Product price range filter
    rango_precio_producto = st.sidebar.slider(
        'Selecciona el rango de precio de producto:',
        min_value=float(precio_combinado['Precio_de_producto'].min()),
        max_value=float(precio_combinado['Precio_de_producto'].max()),
        value=(
            float(precio_combinado['Precio_de_producto'].min()), 
            float(precio_combinado['Precio_de_producto'].max())
        )
    )
    
    # Order price range filter
    rango_precio_orden = st.sidebar.slider(
        'Selecciona el rango de precio de orden:',
        min_value=float(precio_combinado['Precio_Orden'].min()),
        max_value=float(precio_combinado['Precio_Orden'].max()),
        value=(
            float(precio_combinado['Precio_Orden'].min()), 
            float(precio_combinado['Precio_Orden'].max())
        )
    )
    
    return producto_seleccionado, rango_precio_producto, rango_precio_orden

def filter_data(conexion_ordenada, precio_combinado, producto_seleccionado, rango_precio_producto, rango_precio_orden):
    """Filter data based on product selection and price ranges."""
    # Filter by product if not "All products"
    if producto_seleccionado != "Todos los productos":
        conexion_ordenada = conexion_ordenada[conexion_ordenada["ProductName"] == producto_seleccionado]
    
    # Create masks for price ranges
    mask_precio_producto = (
        (precio_combinado['Precio_de_producto'] >= rango_precio_producto[0]) & 
        (precio_combinado['Precio_de_producto'] <= rango_precio_producto[1])
    )
    mask_precio_orden = (
        (precio_combinado['Precio_Orden'] >= rango_precio_orden[0]) & 
        (precio_combinado['Precio_Orden'] <= rango_precio_orden[1])
    )
    
    # Apply filters
    precio_combinado_filtrado = precio_combinado[mask_precio_producto & mask_precio_orden]
    
    return conexion_ordenada, precio_combinado_filtrado

def create_top_products_chart(conexion_ordenada):
    """Create bar chart of top 10 products sold."""
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

def create_price_relationship_chart(precio_combinado_filtrado):
    """Create scatter plot showing relationship between product and order prices."""
    fig2 = px.scatter(
        precio_combinado_filtrado, 
        x='Precio_de_producto', 
        y='Precio_Orden', 
        title='Relación entre precios de productos y órdenes de compra',
        labels={'Precio_de_producto': 'Precio de Producto', 'Precio_Orden': 'Precio de Orden'}
    )
    fig2.update_layout(
        xaxis_title='Precio de Producto',
        yaxis_title='Precio de Orden'
    )
    st.plotly_chart(fig2)

def create_shipping_region_chart(agrupado):
    """Create bar chart of accumulated count by shipping region."""
    filtrar_region = st.selectbox('Selecciona la Región de Envío para Filtrar', ['Todos'] + list(agrupado['ShipRegion'].unique()))
    
    if filtrar_region != 'Todos':
        mask_region = agrupado['ShipRegion'] == filtrar_region
        agrupado = agrupado[mask_region]
    
    grafico3 = px.bar(
        agrupado, 
        x='ShipRegion', 
        y='conteo_acomulado', 
        title=f'Cantidad Acumulada por Región de Envío (Filtrado: {filtrar_region})',
        labels={'ShipRegion': 'Región de Envío', 'conteo_acomulado': 'Cantidad Acumulada'}
    )
    st.plotly_chart(grafico3)

def main():
    """Main function to orchestrate the Streamlit app."""
    # Display key metrics
    display_key_metrics(conexion_ordenada, precio_producto)
    
    # Create sidebar filters
    producto_seleccionado, rango_precio_producto, rango_precio_orden = create_sidebar_filters(conexion_ordenada, precio_combinado)
    
    # Filter data
    conexion_ordenada_filtered, precio_combinado_filtrado = filter_data(
        conexion_ordenada, 
        precio_combinado, 
        producto_seleccionado, 
        rango_precio_producto, 
        rango_precio_orden
    )
    
    # Create visualizations
    create_top_products_chart(conexion_ordenada_filtered)
    create_price_relationship_chart(precio_combinado_filtrado)
    create_shipping_region_chart(agrupado)

if __name__ == "__main__":
    main()
    