# Library
import pandas               as pd
import numpy                as np
import streamlit            as st
import plotly.express       as px
import plotly.graph_objects as go
import folium
import re

st.set_page_config( page_title='Visão Restaurantes', layout='wide' )

from PIL import Image
from streamlit_folium import folium_static
from haversine import haversine
from library.utils import clear_code 
 

# Load Datasets
df_raw = pd.read_csv('datasets/train.csv')


#Fazendo uma copia do Dataframe lido
df = df_raw.copy()

#Limpeza e transformação dos dados.
df1 = clear_code( df )

# ----------------------------------------
# streamlit Barra Lateral
# ----------------------------------------

st.header( 'Marktplace - Visão Restaurante' )

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
        st.subheader(' Overal Metrics' )
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )

        with col1:
             col1.metric( 'Entregadores Unicos', value=df1.loc[:,'Delivery_person_ID'].nunique() )
        
        with col2:
            cols = ('ID','Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude')

            df1['distance_re'] = ( df1.loc[:, cols]
                                      .apply( lambda x: haversine(( x['Restaurant_latitude'],x['Restaurant_longitude']),
                                                                  ( x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1  ) )

            col2.metric( 'Média restaurante / local de entrega', value= np.round( df1.loc[:,'distance_re'].mean(), 2))
            
        with col3: 
            cols = ['Time_taken(min)', 'Festival']

            df_aux = df1.loc[:, cols].groupby('Festival').agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()

            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'] )

            col3.metric( 'Média no Festival' , df_aux )
            
        with col4:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = df1.loc[:, cols].groupby('Festival').agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'] )

            col4.metric( 'STD no Festival' , df_aux )
        
        with col5:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = df1.loc[:, cols].groupby('Festival').agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'] )

            col5.metric( 'Média sem Festival' , df_aux )
            
        with col6:
            cols = ['Time_taken(min)', 'Festival']

            df_aux = df1.loc[:, cols].groupby('Festival').agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'std_time'] )

            col6.metric( 'STD sem Festival' , df_aux )
            
    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns( 2 )
        
        with col1:
            
            
            st.subheader( 'Tempo Médio de entrega por cidade' )


            df_aux = df1.loc[:, ['City','Time_taken(min)'] ].groupby('City').agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()

            fig = go.Figure() 

            fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'] , error_y=dict( type='data', array=df_aux['std_time'] )) )
            fig.update_layout( barmode='group' )

            st.plotly_chart( fig, use_container_width=True )
            
        with col2:
            
            st.subheader( 'Tempo Médio de entrega por pedido' )
            cols = ['City','Time_taken(min)', 'Type_of_order']

            df_aux = df1.loc[:, cols].groupby(['City','Type_of_order']).agg( {'Time_taken(min)' : ['mean','std']})

            df_aux.columns = ['avg_time','std_time']

            df_aux = df_aux.reset_index()

            st.dataframe( df_aux )
            
        
    with st.container():
        st.markdown("""---""")
        st.subheader( 'Distribuição de Tempo' )
        
                
        col1, col2 = st.columns( 2 )
        
        with col1:
            
            
            with st.container():
                
        
                cols = ('Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude')

                df1['distance_re'] = df1.loc[:, cols].apply( lambda x: haversine(( x['Restaurant_latitude'],x['Restaurant_longitude']),
                                                                     ( x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1  )

                avg_distance = df1.loc[:,['City','distance_re']].groupby( 'City' ).mean().reset_index()

                fig = go.Figure( data=[ go.Pie( labels = avg_distance['City'], values=avg_distance['distance_re'], pull=[0.05, 0.05, 0.05] ) ] )

                st.plotly_chart( fig, use_container_width=True )
            
 
        with col2:
            with st.container():
                df_aux = df1.loc[:, ['City','Time_taken(min)', 'Road_traffic_density'] ].groupby(['City','Road_traffic_density']).agg( {'Time_taken(min)' : ['mean','std']})

                df_aux.columns = ['avg_time','std_time']

                df_aux = df_aux.reset_index()
            
                fig = px.sunburst( df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average( df_aux['std_time'] ) )
            
                st.plotly_chart( fig, use_container_width=True )