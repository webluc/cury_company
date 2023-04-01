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

st.set_page_config( page_title='Visão Empresa', layout='wide' )

# Load Datasets
df_raw = pd.read_csv('datasets/train.csv')
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

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática' , 'Visão Geografica'] )

with tab1:
    
    with st.container():
        st.markdown( '### Order by Day' )
        # Colunas
        cols = ["ID",'Order_Date']

        # Selecao  de Linhas 
        df_aux = df1.loc[:,cols].groupby( 'Order_Date').count().reset_index()

        # desenhar o grafico
        fig = px.bar( df_aux, x='Order_Date', y='ID')


        st.plotly_chart( fig, use_container_width = True )
    
    with st.container():
         
        col1, col2 = st.columns( 2 )
        
        with col1:
            st.markdown( '### Traffic Order share' )
            df_aux = df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()  
            
            fig = px.pie( df_aux, values='entregas_perc', names='Road_traffic_density')
            
            st.plotly_chart( fig, use_container_width=True)
            
        with col2:
            st.markdown( ' ### Traffic Order City ' )
            df_aux = df1.loc[ :, ['ID','City','Road_traffic_density']].groupby( ['City','Road_traffic_density']).count().reset_index()
            
            fig = px.scatter( df_aux, 'City', "Road_traffic_density", size = 'ID', color='City')
            
            st.plotly_chart( fig, use_container_width=True )

with tab2:
    with st.container():
        st.markdown( '### Order by Week ' )

        # transforma data em semanas
        df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U ')

        # Selecao de linhas 
        df_aux = df1.loc[:, ['ID','week_of_year']].groupby( 'week_of_year').count().reset_index()

        #Desenho do grafico
        fig =px.line( df_aux, 'week_of_year', 'ID')

        st.plotly_chart( fig, use_container_width=True )
        
    with st.container():
        st.markdown( '### Order shared by Week ' )
        df_aux01 = df1.loc[:, ['ID','week_of_year']].groupby( 'week_of_year').count().reset_index()
        df_aux02 = df1.loc[:, ['Delivery_person_ID','week_of_year']].groupby( 'week_of_year').nunique().reset_index()

        df_aux = pd.merge( df_aux01, df_aux02, how='inner' )

        df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

        fig = px.line( df_aux, x='week_of_year', y='order_by_delivery')
        
        st.plotly_chart( fig, use_container_width=True )

with tab3:
    with st.container():
    
        st.markdown( ' ### Country Maps' )
    
        df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby( ['City','Road_traffic_density']).median().reset_index()

        map = folium.Map()

        for index, location_info in df_aux.iterrows():
            folium.Marker( [ location_info['Delivery_location_latitude' ],
                   location_info['Delivery_location_longitude']],
                  popup=location_info[['City','Road_traffic_density']] ).add_to( map )

        folium_static( map )

