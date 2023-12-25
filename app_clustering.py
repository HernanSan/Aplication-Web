 # import packages import
import markdown
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title= "Clustering academico",
    page_icon="🤖",
    layout= "wide", 
    initial_sidebar_state='expanded'
)

st.sidebar.image("https://actoressostenibles.com/wp-content/uploads/2019/08/Logos-15-17-03.png")
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
    st.download_button(
    label="Descargar .csv",
    data=filtered_data.to_csv(),
    file_name="Información de estudiantes.csv",
    mime="text/csv",
)

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
    col3.metric(":red[**Desempeño Critico**]", conteos[2], "-Estudiantes")
    col4.metric(":blue[**Incierto**]", conteos[3], "-Estudiantes sin calificaciones",  delta_color="off")
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

st.write('------------------------------------------')
st.write('Dashboard creado por: Hernán Sánchez')

