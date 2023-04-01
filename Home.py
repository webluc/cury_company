import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = "",
    layout='wide'
)

imagepath = 'pages/' 
image = Image.open( imagepath + 'logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '### Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write( '# Cury Company Growth Dashboard' )

st.markdown( 
    """
    Growth Dashboard foi construido para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    
    ### Como utilizar esse Growth Dashboard
    -- Visão Empresa
        - Visão Gerencial : Metricas gerais de comportamento.
        - Visão Tática    : Indicadores semanais de crescimento.
        - Visão Geografica: Insights de geolocalização.
    -- Visão Entregadores:
        - Acompanhamento dos Indicadores semanais de crescimento.
    -- Visão Restaurante:
        - Indicadores semanais  de crescimento  dos restaurantes .
    ### ASK for Help:
        - Time Comunidade DS
            @ Luciano Lucena
    """ )