import pandas as pd

def clear_code( df ):
    """
        Essa função tem a responsabilidade:
        
        1 - Remoção dos dados NaN
        2 - Mudança do tipo da coluna de dados
        3 - Remoção dos espaços das variaveis de texto
        4 - Formatação da coluna de data
        5 - Limpeza da coluna de tempo
        
        Input : DataFrame
        Output: DataFrame
        
    """
    
    # removendo espaços das strings
    df.loc[:,'ID'] = df.loc[:,'ID'].str.strip()
    df.loc[:,'Road_traffic_density'] = df.loc[:,'Road_traffic_density'].str.strip()
    df.loc[:,'Type_of_order'] = df.loc[:,'Type_of_order'].str.strip()
    df.loc[:,'Type_of_vehicle'] = df.loc[:,'Type_of_vehicle'].str.strip()
    df.loc[:,'City'] = df.loc[:,'City'].str.strip() 
    df.loc[:,'Festival'] = df.loc[:,'Festival'].str.strip() 


    #Exclui as linhas NaN
    linhas_vazias = df['Delivery_person_Age'] != 'NaN '
    df = df.loc[ linhas_vazias, :]
    linhas_vazias = df['multiple_deliveries'] != 'NaN '
    df = df.loc[ linhas_vazias, :]

    df = df.loc[ df['City'] != 'NaN', :]
    df = df.loc[ df['Festival'] != 'NaN ', :]
    df = df.loc[ df['Road_traffic_density'] != 'NaN', :]
    df = df.loc[ df['Weatherconditions'] != 'NaN', : ]


    # Limpando espaços brancos na string
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )

    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )

    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

    df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )

    df = df.reset_index( drop=True )

    # Transformando min em int

    df['Time_taken(min)'] = df['Time_taken(min)'].apply(  lambda x: x.split('(min) ')[1] )
    df['Time_taken(min)'] = df['Time_taken(min)'].astype( int )
    
    return df