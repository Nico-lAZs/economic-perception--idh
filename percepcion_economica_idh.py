import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="PERCEPCION ECONOMICA Y IDH", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Business Economic Perception--IDH🏥📚🌱")

# Cargando los archivos

with st.expander("datasets loading"):

    
    percepcion_economica = st.file_uploader(":file_folder: Subir archivo de percepción económica", type=["csv", "txt", "xlsx", "xls"])
    idh = st.file_uploader(":file_folder: Subir archivo de IDH", type=["csv", "txt", "xlsx", "xls"], key="idh_uploader")

    if percepcion_economica is not None:
        filename_percepcion = percepcion_economica.name
        df_percepcion = pd.read_csv(percepcion_economica) if filename_percepcion.endswith(".csv") else pd.read_excel(percepcion_economica)
    else:
        df_percepcion = None

    if idh is not None:
        filename_idh = idh.name
        df_idh = pd.read_csv(idh,index_col=0) if filename_idh.endswith(".csv") else pd.read_excel(idh)
        
        
    else:
        df_idh = None

if df_percepcion is not None and df_idh is not None:
    # Filtros
    measures = st.sidebar.multiselect("Escoge la medida economica 💼💵", df_percepcion['Measure'].unique())
    economic_activity = st.sidebar.multiselect("Escoge la actividad economica🏛️💻", df_percepcion['Economic activity'].unique())
    country = st.sidebar.multiselect("Escoge el pais🌍", df_percepcion['Reference area'].unique())
    Frequency= st.sidebar.multiselect(" Escoge la frecuencia de observacion 🕛",df_percepcion['Frequency of observation'].unique())
    IDH=st.sidebar.multiselect("Escoga el pais del data set (idh)🏥📚🌱",df_idh['Reference area'].unique())

    # Aplicar los filtros a los datos
    df2_percepcion = df_percepcion.copy()
    df_idh2=df_idh.copy()

    if measures:
        df2_percepcion = df2_percepcion[df2_percepcion['Measure'].isin(measures)]

    if economic_activity:
        df2_percepcion = df2_percepcion[df2_percepcion['Economic activity'].isin(economic_activity)]

    if country:
        df2_percepcion = df2_percepcion[df2_percepcion['Reference area'].isin(country)]
        
    if Frequency:
        df2_percepcion=df2_percepcion[df2_percepcion['Frequency of observation'].isin(Frequency)]    
        
    if  IDH:
        df_idh2=df_idh2[df_idh2['Reference area'].isin(IDH)]   
        
        
        
#-------------------------------------------------------------------------------------------------------------------------
## Vision general de la percepcion economica atravez de los años.      

# 1. percepcion economica en general
    
    intervalos = ['-138.1 - 115.0', '-115.0 - 91.8', '-91.8 - 68.7', '-68.7 - 45.6', '-45.6 - 22.4', '-22.4 - 0.7', '0.7 - 23.8', '23.8 - 47.0', '47.0 - 70.1', '70.1 - 93.2', '93.2 - 116.4', '116.4 - 139.5', '139.5 - 162.6']
    bins = [-138.1, -115.0, -91.8, -68.7, -45.6, -22.4, 0.7, 23.8, 47.0, 70.1, 93.2, 116.4, 139.5, 162.6]
    
    
    intervalos_frecuencias = np.histogram(df2_percepcion['OBS_VALUE'], bins=bins)
    frecuencias = intervalos_frecuencias[0]

    
    opinions_managers = pd.DataFrame({
        'intervalos_opinions': intervalos,
        'Frecuencia absoluta': frecuencias
    })

    
    opinions_managers['Frecuencia relativa'] = opinions_managers['Frecuencia absoluta'] / opinions_managers['Frecuencia absoluta'].sum()
    opinions_managers['Frecuencia relativa'] = opinions_managers['Frecuencia relativa'].round(4)

    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=opinions_managers['intervalos_opinions'],
        y=opinions_managers['Frecuencia absoluta'],
        name='Frecuencia Absoluta',
        marker_color='blue',
        opacity=0.4,
        text=opinions_managers['Frecuencia absoluta'],
        textposition='outside',
        visible='legendonly'
    ), secondary_y=False)

    fig.add_trace(go.Bar(
        x=opinions_managers['intervalos_opinions'],
        y=opinions_managers['Frecuencia relativa'],
        name='Frecuencia Relativa (%)',
        marker_color='red',
        opacity=0.4,
        text=opinions_managers['Frecuencia relativa'],
        textposition='outside'
    ), secondary_y=True)
    
    fig.update_yaxes(
    range=[0, opinions_managers['Frecuencia relativa'].max() + 0.05],
    secondary_y=True
)
    

    
    fig.update_layout(
    title='Percepción Económica General 1950-2024',
    barmode='relative',
    margin=dict(t=60),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=12),  
    ),
    yaxis=dict(
        tickfont=dict(size=12),  
    ),
    legend=dict(
        font=dict(size=14)  
    ),
    font=dict(
        size=16  
    )
)   
    st.write("\n\n") # lineas de salto
    st.write("\n\n")
    st.header("📉 Visión general de la percepción económica a través de los años 📈")
    st.write("\n\n")
    st.write("\n\n")
    st.plotly_chart(fig)
    
    
    
    # 2. promedio opiniones por pais
    avg_country_ = df2_percepcion.groupby('Reference area')['OBS_VALUE'].agg(['mean', 'max', 'min']).reset_index()
    
    def categorize_opinion(value):
        if value < -45.6:
            return'Muy negativo'
        elif -45.6<= value < -22.4:
            return'Negativo'
        elif -22.4 <= value < 0.7:
            return 'Neutral'
        elif 0.7 <= value < 23.8:
            return 'levemente Positivo'
        elif 23.8 <= value <47.0:
            return 'positivo'
        else :
            return 'Muy Positivo'
    avg_country_['opinion_category']=avg_country_['mean'].apply(categorize_opinion)   
        
    # graficamos el promedio por pais en opinion en cuanto el panorama economico
    fig2=px.scatter(avg_country_,x='Reference area',y='mean',color='opinion_category',
                            color_discrete_map={'Muy negativo':'Red','Negativo':'Orange','Neutral':'Gray',
                                               'levemente Positivo':'Yellow','positivo':'lightblue','Muy Positivo':'Skyblue'}
                            ,title='promedio opiniones y max,min  por pais')
# Añadir el gráfico de los valores 'max'
    fig2.add_scatter(x=avg_country_['Reference area'], 
                    y=avg_country_['max'], 
                    mode='markers', 
                    name='Max', 
                    marker=dict(color='blue'))

# Añadir el gráfico de los valores 'min'
    fig2.add_scatter(x=avg_country_['Reference area'], 
                    y=avg_country_['min'], 
                    mode='markers', 
                    name='Min', 
                    marker=dict(color='red'))

    fig2.update_yaxes(title='')
    fig2.update_xaxes(title='')
    
    st.plotly_chart(fig2)
    
    
    #3. haciendo grafico de linea par aver por año la percepcion economica general 
    expanded_time=df2_percepcion['TIME_PERIOD'].str.split('-',expand=True)

    expanded_time=expanded_time[[0]]
    business_new=pd.concat([df2_percepcion,expanded_time],axis=1)
    #limpiando el nuevo data frame
    business_new.rename(columns={0:'Years'},inplace=True)

    # pasando a entero
    business_new['Years']=business_new['Years'].astype(int)
    groupby_business_tendency=business_new.groupby('Years') ['OBS_VALUE'].mean().reset_index() 
    fig10 = px.line(
    groupby_business_tendency,
    x='Years',
    y='OBS_VALUE',
    title='series de tiempo por año analisis ',
    labels={
        'Years': 'Años',
        'OBS_VALUE': 'valores'
    },
     color_discrete_sequence=["Lightpink"]  
)


    fig10.update_traces(
        mode="lines+markers",
        marker=dict(size=6, color="skyblue", line=dict(width=3, color="white"))
)
    fig10.update_layout(
        xaxis=dict(
            showgrid=False  # Quitar cuadrícula en el eje X
        ),
        yaxis=dict(
            showgrid=False  # Quitar cuadrícula en el eje Y
        )
)

    
    st.plotly_chart(fig10)
    
# percepcion economica mapa de calor
    business_new_group = business_new.pivot_table(index='Reference area', columns='Years', values='OBS_VALUE')
    heat=px.imshow(business_new_group,labels={'x':'Years','y':'Reference area','color':'OBS_VALUE'},
                     color_continuous_scale='Viridis')
    heat.update_layout(title='mapa de calor percepcion economica por pais atravez de los años',
                        width=800,  
    height=800   )


    st.plotly_chart(heat)
    
    # ubicacion geografica de los paises 
    coordinates = {
        'Australia': (-25.2744, 133.7751),
        'Austria': (47.5162, 14.5501),
        'Belgium': (50.8503, 4.3517),
        'Canada': (56.1304, -106.3468),
        'Colombia': (4.5709, -74.2973),
        'Czechia': (49.8175, 15.4720),
        'Denmark': (56.2639, 9.5018),
        'Estonia': (58.5953, 25.0136),
        'Finland': (61.9241, 25.7482),
        'France': (46.6034, 1.8883),
        'Germany': (51.1657, 10.4515),
        'Greece': (39.0742, 21.8243),
        'Hungary': (47.1625, 19.5033),
        'Ireland': (53.4129, -8.2439),
        'Israel': (31.0461, 34.8516),
        'Italy': (41.8719, 12.5674),
        'Japan': (36.2048, 138.2529),
        'Korea': (35.9078, 127.7669),
        'Latvia': (56.8796, 24.6032),
        'Lithuania': (55.1694, 23.8813),
        'Luxembourg': (49.6117, 6.13),
        'Mexico': (23.6345, -102.5528),
        'Netherlands': (52.3794, 4.9009),
        'New Zealand': (-40.9006, 174.8860),
        'Norway': (60.4720, 8.4689),
        'Poland': (51.9194, 19.1451),
        'Portugal': (39.3999, -8.2245),
        'Slovak Republic': (48.6690, 19.6990),
        'Slovenia': (46.1511, 14.9955),
        'Spain': (40.4637, -3.7492),
        'Sweden': (60.1282, 18.6435),
        'Switzerland': (46.8182, 8.2275),
        'Türkiye': (38.9637, 35.2433),
        'United Kingdom': (55.3781, -3.4360),
        'United States': (37.0902, -95.7129)
    }

# Añadir las coordenadas al DataFrame
    avg_country_['latitude'] = avg_country_['Reference area'].map(lambda x: coordinates[x][0])
    avg_country_['longitude'] = avg_country_['Reference area'].map(lambda x: coordinates[x][1])

    figx = px.scatter_geo(avg_country_,
                     lat='latitude',
                     lon='longitude',
                     hover_name='Reference area',
                     color='opinion_category',
                     color_discrete_map={'Muy negativo':'Red','Negativo':'Orange','Neutral':'Gray',
                                               'levemente Positivo':'Yellow','positivo':'lightblue','Muy Positivo':'Skyblue'},# Esto coloreará por categoría de opinión
                     title="Distribución geográfica de la opinión por país")
    figx.update_geos(
        projection_type="orthographic",
        bgcolor="black" #mapa circular

        )
    figx.update_layout(
        width=700,  
        height=700,)

    # Mostrar el gráfico
    st.plotly_chart(figx)    

    
#-------------------------------------------------------------------------------------------------------------------------
# Vision  general IDH 

    st.header('Vision General Desarollo Humano IDH 🌐')
    idh_melted=df_idh2.melt(id_vars='Reference area', var_name='Año', value_name='OBS_VALUE')
    group_reference=idh_melted.groupby('Reference area') ['OBS_VALUE'].mean().reset_index()
    df_idh2
    figz= px.box(
        group_reference,
        x='OBS_VALUE',  # Datos para el eje X
        points='all',    # Mostrar todos los puntos
        title='Desarrollo humano a través de los años (IDH)',
        hover_data={'OBS_VALUE': True, 'Reference area': True},  # Mostrar país y valor al pasar el ratón
        color_discrete_sequence=['lightpink']  # Cambiar a un color específico (puedes poner el color que desees)
)

    figz.update_yaxes(title='promedio paises')

    st.plotly_chart(figz)
    #---------------------------------------------------------------------------------------------------------------
    #Distribucion en "%" segun actitivad economica

    st.header('Distribucion en "%" segun actividad economica💰💳🪙💸')
    figzz=px.box(
        df2_percepcion,
        x='Economic activity',
        y='OBS_VALUE',
        color='Economic activity'
        
    )
    figzz.update_yaxes(title='')
    st.plotly_chart(figzz)

    #---------------------------------------------------------------------------------------------------------------
    #Tendencia central idh y percepcion economica
    st.header('Tendencia central idh y percepcion economica🔍🔢🧑‍🔬')
    #A. Calculamos primero el promedio del desarollo idh y del indice de percepcion economica


    df_idh2['promedio idh']=df_idh2.iloc[:,1:].mean(axis=1)
    df_promedios=pd.DataFrame({'country':df_idh2['Reference area'],'promedio idh':df_idh2['promedio idh'],
                            'promedio opinion managers':avg_country_['mean']})

    #B. Desviacion estandar
    
    countries=df_promedios['country']
    mean_idh = 0.85
    std_idh = 0.05


    fig6 = go.Figure()

    fig6.add_trace(go.Scatter(
        x=countries,
        y=[mean_idh] * len(countries),  
        mode='lines', 
        name='Media del IDH (0.85)',
        line=dict(color='red')
    ))


    fig6.add_trace(go.Scatter(
        x=list(countries)+list(countries[::-1]),
        y=[mean_idh + std_idh] * len(countries) + [mean_idh - std_idh] * len(countries),
        fill='toself', 
        fillcolor='lightblue',
        opacity=0.5,
        line=dict(color='skyblue'),
        name='Rango de ±0.05 "variabilidad"'
    ))

    fig6.add_trace(go.Scatter(
        x=countries,
        y=df_promedios['promedio idh'],
        mode='markers', 
        name='Puntajes de IDH por país',
        marker=dict(color='red', size=8)
    ))


    fig6.update_layout(
        title=" variabilidad idh por pais",
        xaxis_title="País",
        yaxis_title="IDH puntaje ",
        yaxis=dict(range=[0.6, 1.0])
    )
    st.plotly_chart(fig6)


    mean_managers = 4.3
    std_managers = 12.5

    fig7=go.Figure()

    # graficando la linea de la media 4.3

    fig7.add_trace(go.Scatter(
        x=countries,
        y=[mean_managers]*len(countries),
        mode='lines',
        name='economic perception mean 4.3',
        line=dict(color='red')
    ))

    # agregar banda ± 12.5

    fig7.add_trace(go.Scatter(
        x=list(countries)+list(countries[::-1]),
        y=[mean_managers+std_managers]*len(countries)+[mean_managers-std_managers]*len(countries),
        fill='toself',
        fillcolor='lightblue',
        opacity=0.5,
        line=dict(color='Skyblue'),
        name='rango de variabilidad ± 12.5'
            
    ))   

    fig7.add_trace(go.Scatter(
        x=countries,
        y=df_promedios['promedio opinion managers'],
        name='percepcion economica por pais',
        mode='markers',
        marker=dict(color='red',size=8),
        
    ))

    fig7.update_layout(
        title='Variabilidad de la Percepcion economica por pais',
        yaxis=dict(range=[-20,75])
    )

    st.plotly_chart(fig7)


    # C. paises con mas gerentes con percepcion negativa/positiva

    countries_pesimist_managers=df2_percepcion[df2_percepcion['OBS_VALUE']<-22.4] 
    pesimist_countries=countries_pesimist_managers.groupby('Reference area') ['OBS_VALUE'].count().reset_index()

    positivist_countries_managers=df2_percepcion[df2_percepcion['OBS_VALUE']>0.7] 
    positivist_countries=positivist_countries_managers.groupby('Reference area') ['OBS_VALUE'].count().reset_index() 

    fpes=px.histogram(pesimist_countries,x='Reference area',y='OBS_VALUE',title='total gerentes percepcion negativa por pais')
    fpes.update_traces(marker=dict(line=dict(color='white',width=1.5)))
    fpes.update_layout(
        title=dict(
            font=dict(size=20),
        x=0.5),
        xaxis_title='pais',
        yaxis_title='total gerentes'
        
    )
    st.plotly_chart(fpes)

    
    fnov=px.histogram(positivist_countries,x='Reference area',y='OBS_VALUE',title='total gerentes percepcion positiva por pais')
    fnov.update_traces(marker=dict(line=dict(color='white',width=0.5)))
    fnov.update_layout(
        title=dict(font=dict(size=20),
                x=0.5),
        xaxis_title='pais',
        yaxis_title='total gerentes'
        
    )
    st.plotly_chart(fnov)

    # D. cuanto ha crecido de manera porcentual cada pais en su desarollo humano 


    df_idh2 = df_idh2.set_index('Reference area')


    idh_cambio_porcentual = df_idh2.pct_change(axis=1, fill_method=None) * 100


    idh_cambio_porcentual['avg_growth_percent'] = idh_cambio_porcentual.mean(axis=1)

    avg_growth = idh_cambio_porcentual['avg_growth_percent'].reset_index()
    avg_growth.sort_values(by='avg_growth_percent',ascending=True,inplace=True)
    top_5_=avg_growth.head()
    notop_5=avg_growth.tail()
    df_graph=pd.concat([top_5_,notop_5])
    df_graph.sort_values(by='avg_growth_percent',ascending=True,inplace=True)
    colors=['red','red','red','red','red','lightgreen','lightgreen','lightgreen','lightgreen','lightgreen']
    df_graph['color'] = colors

    figx=px.pie(df_graph,values='avg_growth_percent',names='Reference area',hole=0.3,title='Crecimiento porcentual mayor/menor pais 1990--2024',color=colors,
                color_discrete_map={'red': 'red', 'lightgreen': 'lightgreen'})

    st.plotly_chart(figx)

    #-----------------------------------------------------------------------------------------------------------------
    #Que relacion tuvo la percepcion economica  con un verdadero desarrollo humano (IDH)
    st.header('Que relacion tuvo la percepcion economica  con un verdadero desarrollo humano (IDH)🧪🔬🌀')

    correlacion=df_promedios['promedio idh'].corr(df_promedios['promedio opinion managers'])
    print('Correlacion entre el desarollo humano por pais y la percepcion economica: ',correlacion)

    from sklearn.linear_model import LinearRegression

    X=df_promedios[['promedio opinion managers']] 
    Y=df_promedios['promedio idh'] 

    regresion=LinearRegression().fit(X,Y)



    Y_pred=regresion.predict(X)


    print("r2 score: ",regresion.score(X,Y))

    # Regresion lineal

    fig33=px.scatter(df_promedios,x='promedio opinion managers',y='promedio idh',title=' predicción del IDH en función de la percepción económica')

    fig33.add_scatter(x=df_promedios['promedio opinion managers'],y=Y_pred,mode="lines",line=dict(color='Red')) # creando linea de regresion

    st.plotly_chart(fig33)


    # R2


    fig4 = go.Figure(go.Bar(
        x=['Porcentage de relacion'],
        y=[6.1],
        text=['R² = 6.1 % '],
        textposition='outside',
        marker=dict(color='royalblue')
    ))

    fig4.update_layout(
        title="Fuerza de  Relación entre IDH y Percepción Económica",
        yaxis_title="R²",
        xaxis_title="",
        yaxis_range=[0, 100]  # Escala de 0 a 100 %
    )

    st.plotly_chart(fig4)

    # Correlacion

    correlation_data = {
        'indices': ['IDH', 'Percepción Económica'],
        'IDH': [1, -0.247],
        'Percepción Económica': [-0.247, 1]
    }
    df_corr = pd.DataFrame(correlation_data).set_index('indices')


    fig5 = px.imshow(
        df_corr, 
        text_auto=True, 
        color_continuous_scale='Viridis', 
        title="Mapa de Calor de la Correlación entre IDH y Percepción Económica"
    )
    st.plotly_chart(fig5)
