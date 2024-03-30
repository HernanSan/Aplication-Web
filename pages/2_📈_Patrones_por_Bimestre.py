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

st.set_page_config(page_title= "Clustering académico",
    page_icon="📈",
    layout= "wide", 
    initial_sidebar_state='expanded'
)

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

st.title(":blue[SmartEdu Clustering]")
st.subheader('Dasboard para identificación de patrones de desempeño académico de estudiantes')
data = pd.read_csv('datos.csv')
dataframe = pd.read_csv("datos.csv")

st.sidebar.header(':mag: :blue[Filtros Dinamicos]')

with st.sidebar:
    st.divider()
    # Crear un filtro interactivo para seleccionar país y ciudad
    selected_sexo = st.selectbox(":blue[**Seleccione el género:**] ", ["All"] + list(dataframe["Sexo"].unique()))
    if selected_sexo != "All":
        filtered_data = dataframe[dataframe["Sexo"] == selected_sexo]
    else:
        filtered_data = dataframe

    selected_estatus_curso = st.selectbox(":blue[**Seleccione estado del curso:**]", ["All"] + list(filtered_data["Estatus del Curso"].unique()))
    if selected_estatus_curso != "All":
        filtered_data = filtered_data[filtered_data["Estatus del Curso"] == selected_estatus_curso]

    selected_periodo = st.selectbox(":blue[**Seleccione el periodo de Admision:**]", ["All"] + list(filtered_data["Periodo Admision"].unique()))
    if selected_periodo != "All":
        filtered_data = filtered_data[filtered_data["Periodo Admision"] == selected_periodo]
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

# Lista de todas las columnas que el usuario puede seleccionar
materias_disponiblesBim1 = ['Metodología de la invest y tec(Bim1)',
                        'Computación y sociedad(Bim1)', 'Fundamentos de tecnologias(Bim1)',
                        'Algoritmos y resolución de pro(Bim1)',
                        'Humanismo universidad y cultu(Bim1)', 'Fundamentos matematicos(Bim1)'
                        ]

materias_disponiblesBim2 = ['Metodología de la invest y tec(Bim2)',
                        'Computación y sociedad(Bim2)', 'Fundamentos de tecnologias(Bim2)',
                        'Algoritmos y resolución de pro(Bim2)',
                        'Humanismo universidad y cultu(Bim2)', 'Fundamentos matematicos(Bim2)'
                        ]

materias_disponibles_aaBim1 =  ['Metodología de la invest y tec(aaBim1)',
                        'Computacion y sociedad(aaBim1)', 'Fundamentos de tecnologias(aaBim1)',
                        'Algoritmos y resolución de pro(aaBim1)',
                        'Humanismo universidad y cultu(aaBim1)', 'Fundamentos matematicos(aaBim1)'
                        ]

materias_disponibles_aaBim2 =  ['Metodología de la invest y tec(aaBim2)',
                        'Computación y sociedad(aaBim2)', 'Fundamentos de tecnologias(aaBim2)',
                        'Algoritmos y resolución de pro(aaBim2)',
                        'Humanismo universidad y cultu(aaBim2)', 'Fundamentos matematicos(aaBim2)'
                        ]

st.write('------------------------------------------')
st.write(':blue[**Representacion de la cantidad total y grupos de estudintes segun su desempeño académico**]')
# Crear la variable "conteos"
conteos = filtered_data["Cluster"].value_counts()

# Obtener el conteo total de estudiantes
total_estudiantes = len(filtered_data)

# Crear un try-except
try:
    # Mostrar los conteos
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(":black[**Total de Estudiantes**]", total_estudiantes, "Total Estudiantes", delta_color="off")
    col2.metric(":orange[**Desempeño Bueno**]", conteos[0], "Estudiantes")
    col3.metric(":green[**Desempeño Regular**]", conteos[1], "Estudiantes", delta_color="off")
    col4.metric(":red[**Desempeño Critico**]", conteos[3], "-Estudiantes")
    col5.metric(":blue[**Incierto**]", conteos[2], "-Estudiantes sin calificaciones",  delta_color="off")
except IndexError:
    # No hacer nada
    pass

st.write('------------------------------------------')
st.write(':blue[**Analisis de las calificaciones de las meterias del 1° y 2° Bimestre**]')
# Widget principal para elegir el bimestre
bimestre_elegido = st.radio("Selecciona el bimestre:", ["Primer Bimestre", "Segundo Bimestre"])
st.write('------------------------------------------')
             
# Dividir el espacio en dos columnas
col1, col2 = st.columns(2, gap="small")
# Establecer estilo CSS para alinear a la izquierda

with col1:
# Widgets para elegir las materias según el bimestre seleccionado

    if bimestre_elegido == "Primer Bimestre":
        materia_x = st.selectbox("Selecciona la materia para el eje X:", materias_disponiblesBim1, key="materia_x")
        materia_y = st.selectbox("Selecciona la materia para el eje Y:", materias_disponiblesBim1, key="materia_y")

    elif bimestre_elegido == "Segundo Bimestre":
        materia_x = st.selectbox("Selecciona la materia para el eje X:", materias_disponiblesBim2, key="materia_x")
        materia_y = st.selectbox("Selecciona la materia para el eje Y:", materias_disponiblesBim2, key="materia_y")
    else:
        st.error("Error inesperado")

    st.write(':blue[**Explicación del análisis representado en la siguiente gráfica:**]')
    st.write('La siguiente gráfica representa la relación entre las calificaciones de las materias de los estudiantes de acuerdo al grupo de desempeño académico que pertenece.')
# Mostrar la gráfica 2 en la columna 2
with col2:
    # Crear la figura dinámicamente
    fig5 = px.scatter(filtered_data, x=materia_x, y=materia_y,
                    color="Cluster",
                    template="simple_white",
                    labels={materia_x: materia_x.capitalize(),  
                            materia_y: materia_y.capitalize(), 
                            "Cluster": "Desempeño académico"},
                    title=f"Relación entre materias de {materia_x.capitalize()}<br> y {materia_y.capitalize()}")
    st.plotly_chart(fig5, use_container_width=True)

st.write('------------------------------------------')

# Dividir el espacio en dos columnas
col2, col1 = st.columns(2, gap="small")
# Establecer estilo CSS para alinear a la izquierda

with col1:
# Widgets para elegir las materias según el bimestre seleccionado
    if bimestre_elegido == "Primer Bimestre":
        materia_y1 = st.selectbox("Selecciona la materia para el eje X:", materias_disponiblesBim1, key="materia_y1")
    elif bimestre_elegido == "Segundo Bimestre":
        materia_y1 = st.selectbox("Selecciona la materia para el eje X:", materias_disponiblesBim2, key="materia_y1")
    else:
        st.error("Error inesperado")  
    st.write(':blue[**Explicación del análisis representado en la siguiente gráfica:**]')
    st.write('La siguiente gráfica representa la relación entre la calificacion de la materia y el porcentaje de beca de acuerdo al grupo de desempeño al que pertenece.') 

# Mostrar la gráfica 2 en la columna 2
with col2:
    # Crear la figura dinámicamente
    materia_x = "Porcentaje de beca"
    
    # Crear la figura dinámicamente
    fig1 = px.scatter(filtered_data, x=materia_x, y=materia_y1,
                color="Cluster",
                template="simple_white",
                labels={materia_x: "Porcentaje de beca",  
                        materia_y: materia_y.capitalize(), 
                        "cluster": "Desempeño académico"},
                title=f"Relación entre la materia de {materia_y.capitalize()}<br> y el porcentaje de beca.")

    # Mostrar la gráfica
    st.plotly_chart(fig1, use_container_width=True)
st.write('------------------------------------------')

# Dividir el espacio en dos columnas
col1, col2 = st.columns(2, gap="small")
# Establecer estilo CSS para alinear a la izquierda

with col1:
    
# Widgets para elegir las materias según el bimestre seleccionado
    if bimestre_elegido == "Primer Bimestre":
        materia_y = st.selectbox("Selecciona la materia para el eje Y:", materias_disponiblesBim1)
    elif bimestre_elegido == "Segundo Bimestre":
        materia_y = st.selectbox("Selecciona la materia para el eje Y:", materias_disponiblesBim2)
    else:
        st.error("Error inesperado")  
    st.write(':blue[**Explicación del análisis representado en la siguiente gráfica:**]')
    st.write('La siguiente gráfica representa la relación entre la calificacion de la materia y el porcentaje de discapacidad de acuerdo al grupo de desempeño al que pertenece.') 

# Mostrar la gráfica 2 en la columna 2
with col2:
    # Crear la figura dinámicamente
    materia_x = "Porcentaje de discapacidades"
    
    # Crear la figura dinámicamente
    fig2 = px.scatter(filtered_data, x=materia_x, y=materia_y1,
                color="Cluster",
                template="simple_white",
                labels={materia_x: "Porcentaje de Discapacidad",  
                        materia_y: materia_y.capitalize(), 
                        "cluster": "Desempeño académico"},
                title=f"Relación entre las materias de {materia_y.capitalize()}<br> y el porcentaje de dicapacidad")

    # Mostrar la gráfica
    st.plotly_chart(fig2, use_container_width=True)

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if export_as_pdf:
    # Crear un objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Añadir una página
    pdf.add_page()
    
    # Logo
    pdf.image('SmartEdu.jpeg', 15, 8, 33)
        # Arial bold 15
    pdf.set_font('Arial', 'B', 15)
        # Move to the right
    pdf.cell(80)
        # Title
    pdf.cell(60, 30, 'SmartEdu Clustering', 0, 0, 'C')
        # Line break
    pdf.ln(35)

    # Configurar el título del PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte de la Informción del Desempeño Académico de los estudiantes", ln=True, align="C")
    
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(200, 10, f"Número total de estudiantes y cantidad de estudiantes por cada grupo")
    pdf.multi_cell(200, 10, f"segun su desempeño académico")
    
    # Guardar los conteos en el PDF
    pdf.ln(2)  # Ajusta este valor según sea necesario para el espaciado deseado
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, f"Totral: {total_estudiantes} Estudiantes")
    pdf.multi_cell(0, 10, f"Desempeño Bueno: {conteos[0]} Estudiantes")
    pdf.multi_cell(0, 10, f"Desempeño Regular: {conteos[1]} Estudiantes")
    pdf.multi_cell(0, 10, f"Desempeño Critico: {conteos[3]} Estudiantes")
    pdf.multi_cell(0, 10, f"Incierto: {conteos[2]} Estudiantes sin calificaciones")
    
# Descargar cada gráfica y añadirla al PDF
    for i, fig in enumerate([fig1, fig2,fig5]):
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
        file_name="reporte_desempeño_académico.pdf",
        key="download_pdf"
    )
    
st.write('------------------------------------------')
st.write('Dashboard creado por: Hernán Sánchez')