 # import packages import
import markdown
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo
from fpdf import FPDF
import base64
import os
import io
from PIL import Image

st.set_page_config(page_title= "Clustering academico",
    page_icon="📈",
    layout= "wide", 
    initial_sidebar_state='expanded'
)

file = open("marca UTPL 2018-01.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((200, 75))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 45px;
                background-position: 40px 50px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title(":blue[Trabajo de Integración Curricular]")
st.subheader(':male-detective: _Identificación de patrones en base a información académica de estudiantes aplicando algoritmos de Aprendizaje Automático._ ')
data = pd.read_csv('data_completa.csv')
dataframe = pd.read_csv("data_completa.csv")

st.sidebar.header(':mag: :blue[Filtros Dinamicos]')

with st.sidebar:
    st.divider()
    # Crear un filtro interactivo para seleccionar país y ciudad
    selected_country = st.selectbox(":blue[**Seleccione sexo:**] ", ["All"] + list(dataframe["sexo"].unique()))
    if selected_country != "All":
        filtered_data = dataframe[dataframe["sexo"] == selected_country]
    else:
        filtered_data = dataframe

    selected_city = st.selectbox(":blue[**Seleccione estado del curso:**]", ["All"] + list(filtered_data["estatus_cursos"].unique()))
    if selected_city != "All":
        filtered_data = filtered_data[filtered_data["estatus_cursos"] == selected_city]

    selected_vegan_option = st.selectbox(":blue[**Seleccione el ciclo academico:**]", ["All"] + list(filtered_data["ciclo_academico"].unique()))
    if selected_vegan_option != "All":
        filtered_data = filtered_data[filtered_data["ciclo_academico"] == selected_vegan_option]
    st.write(":blue[**Descarge la información:**]")
    
    # Dividir el espacio en dos columnas
    col1, col2 = st.columns(2, gap="small")
    # Establecer estilo CSS para alinear a la izquierda
    with col1:
        st.download_button(
            label="Descargar .csv",
            data=filtered_data.to_csv(),
            file_name="Información de estudiantes.csv",
            mime="text/csv",
        )
    with col2:
        export_as_pdf = st.button("Generar PDF")
    


fig = px.scatter(filtered_data, x="Componente_1", y="Componente_2", color="cluster", 
                color_continuous_scale='Inferno', template="simple_white",
                hover_data={'porcentaje_de_beca': True, 'porcentaje_des_matricula': True, 'monto_descuento_automatico': True},
                labels={"porcentaje_de_beca": "Porcentaje de beca",  
                    "porcentaje_des_matricula": "Porcentaje de descuento de la matricula", 
                    "monto_descuento_automatico": "Monto de descuento automatico", 
                    "cluster": "Desempeño academico"},
                title= "Gráfica de todos los estudiantes en los Grupos generados por el Modelo")


fig4 = px.scatter(filtered_data, x="bim1_nota_fundamentos_de_tecnologias", 
                y="bim1_nota_humanismo,_universidad_y_cultu",
                color="cluster",
                template="simple_white",
                labels={"bim1_nota_fundamentos_de_tecnologias": "Fundamentos de la Tecnología",  
                    "bim1_nota_humanismo,_universidad_y_cultu": "Humanismo universidad y cultura", 
                    "cluster": "Desempeño academico"},
                title= "Relación entra las calificaciónes de 1° Bimestre de las materias de Fundamentos de la <br> Tecnología y Humanismo ")

fig1 = px.scatter(filtered_data, x="acdb1_nota_fundamentos_matematicos", 
                y="porcentaje_des_matricula",
                color="cluster",
                labels={"acdb1_nota_fundamentos_matematicos": "Fundamentos matematicos",  
                        "porcentaje_des_matricula": "Porcentaje de descuento de la matricula", 
                        "cluster": "Desempeño academico"},
                template="simple_white",
                title='Relacion entre las calificaciones del apeb1 Bimestre de la materia de Fundamentos <br> Matematicos y el Porcentaje de descuento de la matricula ')

fig2 = px.scatter(filtered_data, x="bim1_nota_computacion_y_sociedad", 
                y="porcentaje_de_beca",
                color="cluster",
                labels={"bim1_nota_computacion_y_sociedad": "Computación y sociedad",  
                        "porcentaje_de_beca": "Porcentaje de beca", 
                        "cluster": "Desempeño academico"},
                template="simple_white",
                title='Relacion entre las calificaciones del 1° Bimestre de la materia de Computacón y <br> sociedady el Porcentaje de beca ')

# Crear la variable "conteos"
conteos = filtered_data["cluster"].value_counts()

st.write('------------------------------------------')

# Crear un try-except
try:
    # Mostrar los conteos
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(":orange[**Desempeño Bueno**]", conteos[0], "Estudiantes")
    col2.metric(":green[**Desempeño Regular**]", conteos[1], "Estudiantes", delta_color="off")
    col3.metric(":red[**Desempeño Critico**]", conteos[3], "-Estudiantes")
    col4.metric(":blue[**Incierto**]", conteos[2], "-Estudiantes sin calificaciones",  delta_color="off")
    
except IndexError:
    # No hacer nada
    pass

st.write('------------------------------------------')

# Dividir el espacio en dos columnas
col1, col2 = st.columns(2, gap="small")
# Establecer estilo CSS para alinear a la izquierda

with col1:
    #st.subheader("Top 10 de los restaurantes mejor valorados")
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)

# Mostrar la gráfica 2 en la columna 2
with col2:
    #st.subheader("Top 10 de los restaurantes mejor valorados")
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# Crear una lista con las variables disponibles
variables_y = ["bim1_nota_algoritmos_y_resolucion_de_pro",
               "bim1_nota_fundamentos_de_tecnologias",
               "bim1_nota_computacion_y_sociedad",
               "bim1_nota_metodologia_de_la_invest_y_tec",
               "bim1_nota_humanismo,_universidad_y_cultu",
               "bim1_nota_fundamentos_matematicos"]

# Crear una lista con los nombres de las variables
nombres_variables = ["Notas de algoritmos y resolución de problemas", "Notas de fundamentos de tecnologías", "Notas de computación y sociedad", "Notas de metodología de la investigación y tecnología"]

# Crear el selector
variable_y = st.selectbox("Seleccione la materia en específico:", variables_y)

# Crear la gráfica
fig3 = px.bar(filtered_data, x="cluster", y=variable_y, color="cluster", title="Estado de los estudiantes por grupo")

# Mostrar la gráfica
st.plotly_chart(fig3, use_container_width=True)



def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if export_as_pdf:
    # Crear un objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Añadir una página
    pdf.add_page()

    # Configurar el título del PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte del Dashboard de Clustering Académico", ln=True, align="C")
    
    
    # Guardar los conteos en el PDF
    pdf.ln(2)  # Ajusta este valor según sea necesario para el espaciado deseado
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, f"Desempeño Bueno: {conteos[0]} Estudiantes")
    pdf.multi_cell(0, 10, f"Desempeño Regular: {conteos[1]} Estudiantes")
    pdf.multi_cell(0, 10, f"Desempeño Critico: {conteos[3]} Estudiantes")
    pdf.multi_cell(0, 10, f"Incierto: {conteos[2]} Estudiantes sin calificaciones")
    
# Descargar cada gráfica y añadirla al PDF
    for i, fig in enumerate([fig, fig1, fig4, fig2, fig3]):
        # Guardar la figura como una imagen temporal
        img_path = f"temp_img_{i}.png"
        fig.write_image(img_path)

        # Añadir la imagen al PDF
        # Colocar dos gráficas una al lado de la otra
        if i % 2 == 0:
            pdf.image(img_path, x=10, y=pdf.get_y(), w=90)
        else:
            pdf.image(img_path, x=100, y=pdf.get_y(), w=90)
            pdf.ln(70)  # Hacer el salto de línea después de dos gráficas

        # Eliminar la imagen temporal después de usarla
        os.remove(img_path)

    # Convertir el PDF a bytes
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    # Crear el enlace de descarga
    st.download_button(
        label="Descargar PDF",
        data=pdf_bytes,
        file_name="dashboard_clustering_academico.pdf",
        key="download_pdf"
    )
    
st.write('------------------------------------------')
st.write('Dashboard creado por: Hernán Sánchez')