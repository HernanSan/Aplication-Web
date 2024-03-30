import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo
from PIL import Image
import base64
import pandas as pd
import io

st.set_page_config(
    page_title="Información General",
    page_icon="🤖",
    layout= "wide", 
    initial_sidebar_state='expanded'
)

data = pd.read_csv('datos.csv')

file = open("SmartEdu.jpeg", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((170, 170))  # x, y
resized_img.save(buffer, format="JPEG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 140px;
                background-position: 50px 40px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
st.write("# Bienvenido a SmartEdu Clustering! 👋")

st.markdown(
    """
    Esta plataforma te ofrece una experiencia única para explorar y analizar el rendimiento 
    académico de estudiantes.
    Con dashboards que proporcionan una visión detallada de los patrones y agrupamientos 
    identificados a través de técnicas avanzadas de clustering. Sumérgete en el fascinante
    mundo de los datos académicos y descubre insights valiosos sobre el desempeño estudiantil.
    Acompáñanos en este viaje, donde la información se convierte en conocimiento, y donde cada 
    clic te acerca a una comprensión más profunda de los factores que influyen en el éxito académico.
     
     :blue[**¡Explora, aprende y disfruta de SmartEdu Clustering!**]
"""
)

# Dividir el espacio en dos columnas
col1, col2 = st.columns(2, gap="small")
# Establecer estilo CSS para alinear a la izquierda

with col1:
    st.markdown(
    """
    ### **Algoritmos utilizados**
    En la implementación de SmartEdu Clustering, se utilizó el potente algoritmo de k-means 
    para realizar una segmentación efectiva de los datos académicos. Este algoritmo de clustering
    ha permitido identificar patrones inherentes en el desempeño estudiantil y agrupar a
    los estudiantes en categorías distintivas. 
    
    A continuación, te presentamos una visualización realizada con la ayuda de la tecnica de Análisis de
    Componetes Principales (PCA) gráfica que refleja de manera clara y precisa los grupos identificados por nuestro 
    modelo de k-means.
    
    """    
)

with col2:
    fig = px.scatter(data, x="Componente_1", y="Componente_2", color="Cluster", 
                color_continuous_scale='Inferno', template="simple_white",
                hover_data={'Porcentaje de beca': True, 'Edad': True},
                labels={"Porcentaje de beca": "Porcentaje de beca",
                    "Edad": "Edad", 
                    "cluster": "Desempeño academico"},
                title= "Gráfica de todos los estudiantes con los grupos generados por el Modelo")
    st.plotly_chart(fig, use_container_width=True)
    
st.markdown(
    """
    ### **Ejemplo del uso de la herramienta**
    Como ejemplo demostrativo del uso de la herramienta se presenta la experiencia de explorar y analizar el rendimiento 
    académico de estudiantes de una institucion de educación superior de :blue[**primero**] a :blue[**cuarto**] 
    ciclo en la carrera a distancia de :blue[**Tecnologías de la Información**], durante los periodos académicos :blue[**2019, 2020 y 2021**].
    En la parte izquierda puede observar dos ventanas donde encontrará los Dashboard de los patrones por las 
    Calificaciones de las materias :red[Bimestrales] y las 
    califiaciones por cada :red[Componente de Aprendizaje]. 
    """
)