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

def top_cuisines(df1, asc):
    fig = df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending = asc).reset_index().head(top_n)
    fig = px.bar(fig, x='cuisines', y='aggregate_rating', labels = {'cuisines': 'Culinárias', 'aggregate_rating': 'Média das avaliações'}, text_auto=True)
    return fig


#------------------------------------Início da estrutura lógica do código ---------------------------
#-----------------------
#importando o arquivo
#---------------------
df = pd.read_csv('dataset/zomato.csv')

#-----------------------
#limpando os dados
#-----------------------
df1 = clean_code(df)
    

#VISÃO CULINÁRIAS
 
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

top_n = st.sidebar.slider("Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10)
st.sidebar.markdown("""---""")

#filtro de restaurantes:
linhas_selecionadas = df1['country_code'].isin(country)

cuisines = st.sidebar.multiselect(
    'Escolha os tipos de culinárias',
        ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'], 
    default= ['Italian', 'American', 'Arabian', 'Brazilian'])
st.sidebar.markdown("""---""")

#filtro de culinárias:
linhas_selecionadas = df1['cuisines'].isin(cuisines)
df1 = df1.loc[linhas_selecionadas, :]


#================================
#layout no streamlit
#================================

with st.container():
    st.header('Visão: Culinárias')
    st.subheader('Top restaurantes')
    df2 = df1.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True]).head(top_n)
    st.dataframe(df2)

with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('Melhores tipos de culinárias')
        fig = top_cuisines(df1, asc= False)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('Piores tipos de culinárias')
        fig = top_cuisines(df1, asc= True)
        st.plotly_chart(fig, use_container_width=True)
    
    
    
