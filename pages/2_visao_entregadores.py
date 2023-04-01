# Library
import pandas         as pd
import numpy          as np
import streamlit      as st
import plotly.express as px 
import folium
import re

from PIL import Image
from streamlit_folium import folium_static
from library.utils import clear_code 

st.set_page_config( page_title='Visão Entregadores', layout='wide' )

# Load Datasets
df_raw = pd.read_csv('datasets/train.csv')


#Fazendo uma copia do Dataframe lido
df = df_raw.copy()


#Limpeza e transformação dos dados.
df1 = clear_code( df )


# ----------------------------------------
# streamlit Barra Lateral
# ----------------------------------------

st.header( 'Marktplace - Visão Cliente' )

imagepath = 'pages/' 
image = Image.open( imagepath + 'logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '### Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '### Selecione uma data limite' )

date_slider = st.sidebar.slider(
    'Até que valor ?',
    value=pd.datetime( 2023, 3, 28 ),
    min_value = pd.datetime( 2022, 2, 11 ),
    max_value = pd.datetime( 2022, 4, 6 ),
    format = 'DD-MM-YYYY' )

st.sidebar.markdown( """---""" )
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '#### Powered ComunidadeDS'  )

# ----------------------------------------
# Aplicacao do filtro ao layout
# ----------------------------------------

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[ linhas_selecionadas, : ]

# Filtro de Traffic 
linhas_selecionadas = df['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[ linhas_selecionadas, : ]

# ----------------------------------------
# streamlit Layout - Body 
# ----------------------------------------

tab1, tab2,tab3 = st.tabs( ['Visão Gerencial','.','.'] )

with tab1:
    with st.container():
        
        col1, col2, col3, col4 = st.columns( 4 )

        with col1:
             col1.metric( 'Maior Idade', value=df1.loc[:,'Delivery_person_Age'].max() )
        
        with col2:
            col2.metric( 'Menor Idade', value=df1.loc[:,'Delivery_person_Age'].min() )
        
        with col3:
            col3.metric( 'Melhor condição Veículo', df1.loc[:,'Vehicle_condition'].max() )
            
        with col4:
            col4.metric( 'Pior condição de veículo' , df1.loc[:,'Vehicle_condition'].min() )
            
    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown( 'Tabela Avaliação por Entregadores ' )
            df_aux = ( df1.loc[:,['Delivery_person_ID','Delivery_person_Ratings']]
                          .groupby('Delivery_person_ID')
                          .mean().reset_index() )
            st.dataframe( df_aux )
        with col2:
            with st.container():
                st.markdown( 'Tabela Condições Transito' )
                df_aux = ( df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                              .groupby('Road_traffic_density')
                              .agg({'Delivery_person_Ratings' : ['mean','std']}) )
                df_aux.columns = ['Delivery_means','Delivery_std']

                df_aux = df_aux.reset_index()
                st.dataframe( df_aux )
            with st.container():
                st.markdown( 'Tabela Condições Climaticas ' )
                df_aux = ( df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
                              .groupby('Weatherconditions')
                              .agg({'Delivery_person_Ratings' : ['mean','std']}) )
                df_aux.columns = ['Delivery_means','Delivery_std']

                df_aux = df_aux.reset_index()
                st.dataframe( df_aux )
                
    with st.container():
        st.markdown("""---""")
        col1,  col2 = st.columns( 2 )
        with col1:
            st.markdown( 'Top entregadores mais rapidos ' )
            df_aux = ( df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                          .groupby(['City','Delivery_person_ID'])
                          .min()
                          .sort_values(['City','Time_taken(min)']).reset_index() )
            st.dataframe( df_aux )
            
        with col2:
            st.markdown( 'Top entregadores mais lento ' )
            df_aux = ( df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']]
                          .groupby(['City','Delivery_person_ID']).max()
                          .sort_values(['City','Time_taken(min)'], ascending=False).reset_index() )
            st.dataframe( df_aux )