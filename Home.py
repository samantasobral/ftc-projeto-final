#Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import folium
import re
import inflection
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image

#-----------------------------------------------
# FUNÇÕES 
#-----------------------------------------------
def clean_code(df):
    def rename_columns(dataframe):
        df = dataframe.copy()
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df

    df['Cuisines'] = df['Cuisines'].astype( str )
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    
    df = rename_columns(df)
    
    # Excluir as linhas sem votos
    linhas_vazias = df['votes'] != 0
    df = df.loc[linhas_vazias, :]

    #eliminando valores nulos de cuisine:
    linhas_vazias = df['cuisines'] != 'nan'
    df = df.loc[linhas_vazias, :]
    
    #colocando os nomes dos países
    df['country_code'] = df['country_code'].replace({
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",})


    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
        }

    def color_name(color_code):
        
        return COLORS[color_code]

    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))
    
    df = df.dropna()
    
    df = df.drop_duplicates()
    
    return df


def mapa(df1):
    cols = ['restaurant_name', 'average_cost_for_two', 'currency', 'aggregate_rating', 'color_name', 'latitude', 'longitude']
    data_plot = df1.loc[:, cols]

    map = folium.Map()

    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['latitude'], location_info['longitude']], popup = location_info['restaurant_name'], icon=folium.Icon(color=location_info['color_name'])).add_to(map)

        folium_static(map, width = 1024 , height= 600)
    return None

#------------------------------------Início da estrutura lógica do código ---------------------------
#-----------------------
#importando o arquivo
#---------------------
df = pd.read_csv('dataset\zomato.csv')

#-----------------------
#limpando os dados
#-----------------------
df1 = clean_code(df)
    

#VISÃO PAÍS
 
#================================
#layout no streamlit - barra lateral
#================================

image = Image.open('image.png')
st.sidebar.image(image, width=60)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtros')

country = st.sidebar.multiselect(
    'Escolha os países',
    ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'], 
    default= ['India', 'Brazil', 'England', 'United States of America'])
st.sidebar.markdown("""---""")


#filtro de país:
linhas_selecionadas = df1['country_code'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]


#================================
#layout no streamlit
#================================

with st.container():
    st.markdown('# Fome zero!')
    st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
    st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        rest = len(df1.loc[:,'restaurant_id'].unique())
        col1.metric('Restaurantes', rest)
        
    with col2:
        paises = len(df1.loc[:,'country_code'].unique())
        col2.metric('Países', paises)
        
    with col3:
        cidades = len(df1.loc[:, 'city'].unique())
        col3.metric('Cidades', cidades)
        
    with col4:
        avaliacoes = df1.loc[:,'votes'].sum()
        col4.metric('Avaliações', avaliacoes)
    
    with col5:
        culinarias = len(df1.loc[:, 'cuisines'].unique())
        col5.metric('Tipos de culinárias', culinarias)
        
with st.container():

    mapa(df1)