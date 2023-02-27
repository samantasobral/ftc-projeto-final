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

def rest_pais(df1):
    df_aux = df1.loc[:, ['country_code', 'restaurant_id']].groupby('country_code').count().reset_index()
    df_aux = df_aux.sort_values('restaurant_id', ascending=False)
    fig = px.bar(df_aux, x='country_code', y='restaurant_id', labels = {'country_code': 'Países', 'restaurant_id': 'Quantidade de restaurantes'}, title = 'Quantidade de restaurantes registrados por país', text_auto=True)
    return fig

def cidade_pais(df1):
    df_aux = df1.loc[:, ['country_code', 'city']].groupby('country_code').nunique().reset_index()
    df_aux = df_aux.sort_values('city', ascending=False)
    fig = px.bar(df_aux, x='country_code', y='city', labels={'country_code': 'Países', 'city': 'Quantidade de cidades'}, title = 'Quantidade de cidades registradas por país', text_auto = True)
    return fig

def av_pais(df1):
    df_aux = df1.loc[:, ['country_code', 'votes']].groupby('country_code').mean()
    df_aux = df_aux.reset_index()
    df_aux = df_aux.sort_values('votes', ascending = False)
    fig = px.bar(df_aux, x='country_code', y='votes', labels = {'country_code': 'Países', 'votes': 'Quantidade de avaliações'}, title = 'Média de avaliações por país', text_auto=True)
    return fig

def preco_pais(df1):
    df_aux = df1.loc[:, ['country_code', 'average_cost_for_two']].groupby('country_code').mean()
    df_aux = df_aux.reset_index()
    df_aux = df_aux.sort_values('average_cost_for_two', ascending = False)
    fig = px.bar(df_aux, x = 'country_code', y='average_cost_for_two', labels = {'country_code': 'Países', 'average_cost_for_two': 'Preço de prato para dois'}, title='Média de preço de prato para dois por país', text_auto = True)
    return fig

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
    st.header('Visão País')
    fig = rest_pais(df1)
    st.plotly_chart(fig, use_container_width = True)
    
with st.container():
    fig = cidade_pais(df1)
    st.plotly_chart(fig, use_container_width = True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        fig = av_pais(df1)
        st.plotly_chart(fig, use_container_width = True)
        
    with col2:
        fig = preco_pais(df1)
        st.plotly_chart(fig, use_container_width = True)
        