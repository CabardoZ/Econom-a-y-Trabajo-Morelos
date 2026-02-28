# -*- coding: utf-8 -*-
"""ECONOMÍA LABORAL EN MORELOS - Dashboard Rediseñado"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

############################  DATOS  ############################

df_general = {
    'Población ocupada': '98.54%',
    'Población económicamente activa': '57.20%',
    'Ingreso promedio mensual': '$11,178',
    'Hombres': '50.40%',
    'Mujeres': '49.60%',
    'Formalidad': '35.33%',
    'Informalidad': '64.67%'
}

df_pea = pd.DataFrame({
    'AÑO': [2020, 2021, 2022, 2023, 2024],
    'PEA 1T': [851025, 806650, 833317, 877664, 887869],
    'PEA2T': [None, 833429, 823846, 870630, 873166],
    'PEA3T': [809827, 836743, 849133, 863509, 888038],
    'PEA4T': [834927, 830832, 859002, 893467, None]
})

df_pea_genero = pd.DataFrame({
    'SEXO': ['HOMBRES']*5 + ['MUJERES']*5,
    'AÑO': [2020, 2021, 2022, 2023, 2024]*2,
    'PEA 1T': [504204, 479895, 496848, 496594, 508443, 346821, 326755, 336469, 381070, 379426],
    'PEA2T': [None, 506067, 484895, 500152, 503398, None, 327362, 338951, 370478, 369768],
    'PEA3T': [482151, 506233, 497248, 501141, 520229, 327746, 330510, 351885, 362368, 367809],
    'PEA4T': [491615, 493277, 493522, 510900, None, 343312, 337105, 365480, 382557, None]
})

df_sectores = pd.DataFrame({
    'AÑO': [2024,2024,2024,2023,2023,2023,2023,2022,2022,2022,2022,2021,2021,2021,2021,2020,2020,2020],
    'TRIMESTRE': ['TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','PRIMERO'],
    'SECTOR PRIMARIO': [90982,80983,71554,82266,80065,82735,67887,88592,87814,78637,70682,82290,86915,65499,64988,88940,93767,102354],
    'SECTOR SECUNDARIO': [191093,196104,204094,189997,198556,191298,201486,190286,196250,193548,205400,188991,190801,200247,186096,182756,181113,177366],
    'SECTOR TERCIARIO': [604157,593600,610249,620053,582868,594372,607584,576982,563612,549901,555945,556387,555397,564229,552743,561442,533491,568876],
    'NO ESPECIFICADO': [1806,2479,1972,1141,2020,2225,707,3142,1457,1760,1290,2714,3630,3454,2823,1789,1526,2429]
})

df_sectores_estratos = pd.DataFrame({
    'AÑO': [2024,2023,2022,2021,2020],
    'Bajo': [126471,114792,105000,120000,98000],
    'Medio bajo': [572341,616963,570000,590000,530000],
    'Medio alto': [149929,124938,130000,135000,105000],
    'Alto': [39297,36764,38000,35000,31000]
})

df_salarios = pd.DataFrame({
    'AÑO': [2024,2024,2024,2023,2023,2023,2023,2022,2022,2022,2022,2021,2021,2021,2021,2020,2020,2020],
    'TRIMESTRE': ['TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','PRIMERO'],
    'HASTA UN SALARIO MÍNIMO': [285658,282057,277379,235450,228928,257244,263082,216184,224916,202315,246677,151558,169134,155513,168180,179233,150688,168600],
    'MÁS DE 1 HASTA 2 SALARIOS MÍNIMOS': [189877,172746,183198,220411,204999,221775,213609,208327,187440,182709,187384,218705,245202,223527,236709,210054,205891,238363],
    'MÁS DE 2 HASTA 3 SALARIOS MÍNIMOS': [26398,18748,19286,35087,23378,30932,31866,52973,46740,43539,38377,57035,64703,62594,60085,68902,62804,65856],
    'MÁS DE 3 HASTA 5 SALARIOS MÍNIMOS': [4385,2182,3774,7895,5242,6216,6341,10236,7757,8069,6485,19107,15108,11029,15545,16885,15613,17516],
    'MÁS DE 5 SALARIOS MÍNIMOS': [1272,2307,1675,1166,2621,2333,34888,2821,4045,2782,3684,5375,3817,5448,3436,6609,3233,3870],
    'NO RECIBE INGRESOS': [36350,34028,37146,36091,30487,35259,30301,31542,34388,25574,25878,32899,33189,26844,23652,36192,40809,30816]
})

df_edad = pd.DataFrame({
    'AÑO': [2024,2024,2024,2023,2023,2023,2023,2022,2022,2022,2022,2021,2021,2021,2021,2020,2020,2020],
    'PERIODO': ['TERCER','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','SEGUNDO','PRIMERO','CUARTO','TERCERO','PRIMERO'],
    '15-19 AÑOS': [40694,37563,40637,36378,36596,37543,37689,38944,35821,36215,38361,35002,37012,36111,35521,34012,35217,34589],
    '20-29 AÑOS': [171914,171012,164992,179010,168187,170985,174218,174836,169812,176226,175625,165417,167859,170174,165348,160099,161172,158761],
    '30-39 AÑOS': [208215,205574,205789,203014,212817,211008,215103,220320,221004,214209,214225,210421,217214,217956,215052,207654,210358,213498],
    '40-49 AÑOS': [187106,187802,197083,194549,192623,190311,185900,189623,198435,185112,190214,183226,185411,188101,187363,178947,176126,180759],
    '50-59 AÑOS': [168135,167961,171418,168551,151543,155633,159417,154253,146814,151051,150370,142853,137826,138747,142614,140423,138965,136481],
    '60 AÑOS Y MÁS': [111482,103028,107663,111841,101558,103112,100887,95213,90117,88793,90201,80373,78594,79047,81012,74792,72533,69804]
})

df_edad_avg = df_edad.groupby('AÑO').agg({
    '15-19 AÑOS':'mean','20-29 AÑOS':'mean','30-39 AÑOS':'mean',
    '40-49 AÑOS':'mean','50-59 AÑOS':'mean','60 AÑOS Y MÁS':'mean'
}).reset_index()

df_profesiones = pd.DataFrame({
    'AÑO': [2024,2024,2024,2023,2023,2023,2022,2022,2022,2021,2021,2021,2020,2020,2020],
    'PROFESIONISTAS, TÉCNICOS Y TRABAJADORES DEL ARTE HOMBRES': [45721,47863,50783,51742,56035,55080,53513,49010,42385,43161,37957,39973,46502,38662,39785],
    'PROFESIONISTAS, TÉCNICOS Y TRABAJADORES DEL ARTE MUJERES': [42861,40122,45128,45699,44911,44386,42035,37391,35808,35935,36200,29166,33075,31407,34780],
    'TRABAJADORES DE LA EDUCACIÓN HOMBRES': [11690,10992,11219,10261,10202,12298,14004,13324,11941,10462,10281,11152,12630,13653,12315],
    'TRABAJADORES DE LA EDUCACIÓN MUJERES': [223862,23888,25475,21616,19805,19699,17940,20833,19566,20682,20648,22994,20732,22693,26106],
    'FUNCIONARIOS Y DIRECTIVOS DE LOS SECTORES PÚBLICO, PRIVADO Y SOCIAL HOMBRES': [4787,6260,6424,6537,5582,8455,6717,5428,6230,3969,3450,6829,8895,6904,6040],
    'FUNCIONARIOS Y DIRECTIVOS DE LOS SECTORES PÚBLICO, PRIVADO Y SOCIAL MUJERES': [2850,3155,2800,6229,4918,5202,7102,5825,3054,3487,4796,3309,4683,2860,2378],
    'TRABAJADORES EN ACTIVIDADES AGRÍCOLAS, GANADERAS, SILVÍCOLAS, DE CAZA Y DE PESCA HOMBRES': [73184,71680,60190,70930,66745,71702,57045,74957,77220,71423,63604,73260,80433,61984,61150],
    'TRABAJADORES EN ACTIVIDADES AGRÍCOLAS, GANADERAS, SILVÍCOLAS, DE CAZA Y DE PESCA MUJERES': [14468,7716,10193,8815,11536,11300,9451,11561,10317,6292,6733,8955,6658,5541,4070],
    'TRABAJADORES INDUSTRIALES, ARTESANOS Y AYUDANTES HOMBRES': [168768,170580,178290,165335,168052,164244,172199,160964,171344,166246,183480,166763,168588,183136,163920],
    'TRABAJADORES INDUSTRIALES, ARTESANOS Y AYUDANTES MUJERES': [50409,46077,51214,50439,46573,39683,48200,44525,50127,44957,45529,51181,41345,41456,41396],
    'CONDUCTORES Y AYUDANTES DE CONDUCTORES DE MAQUINARÍA  MÓVIL Y MEDIOS DE TRANSPORTE HOMBRES': [39173,37427,37391,39485,35948,37703,40638,38203,40917,43599,43737,42647,40136,38459,35157],
    'CONDUCTORES Y AYUDANTES DE CONDUCTORES DE MAQUINARÍA  MÓVIL Y MEDIOS DE TRANSPORTE MUJERES': [676,542,906,0,569,130,455,124,650,112,701,0,320,320,0],
    'OFICINISTAS HOMBRES': [21366,21793,19971,22423,23523,22476,21289,24484,21265,21060,22066,18272,21797,26507,24844],
    'OFICINISTAS MUJERES': [26321,29367,28406,27284,28643,30379,33796,27717,30831,31614,28366,27876,30598,31475,34583],
    'COMERCIANTES HOMBRES': [880443,74893,74949,72517,74644,68384,67607,67146,62075,66103,68920,72327,68901,68239,65786],
    'COMERCIANTES MUJERES': [99927,109368,102955,104979,103489,107949,107730,102316,93888,89739,84275,91364,90415,97219,93782],
    'TRABAJADORES EN SERVICIO PERSONALES HOMBRES': [69349,57081,63420,65882,55710,53541,57281,55104,58408,53939,57692,56268,54363,63458,67497],
    'TRABAJADORES EN SERVICIO PERSONALES MUJERES': [105465,108769,110660,115906,101103,110625,111888,113883,106037,104912,108109,101943,101380,93266,88727],
    'TRABAJADORES EN SERVICIOS DE PROTECCIÓN Y VIGILANCIA Y FUERZAS ARMADAS HOMBRES': [5748,4829,5806,5788,4579,6269,6301,4902,5463,4933,5553,5512,3867,4805,3151],
    'TRABAJADORES EN SERVICIOS DE PROTECCIÓN Y VIGILANCIA Y FUERZAS ARMADAS MUJERES': [537,764,1488,1590,700,1030,2361,1305,1607,1010,1112,317,1304,744,933],
})

columns_hombres = [col for col in df_profesiones.columns if 'HOMBRES' in col]
columns_mujeres = [col for col in df_profesiones.columns if 'MUJERES' in col]

profesiones_list = []
for año in df_profesiones['AÑO'].unique():
    for col_h, col_m in zip(columns_hombres, columns_mujeres):
        profesion = col_h.split(' HOMBRES')[0]
        suma_h = df_profesiones[df_profesiones['AÑO'] == año][col_h].sum()
        suma_m = df_profesiones[df_profesiones['AÑO'] == año][col_m].sum()
        profesiones_list.append({'AÑO': año, 'PROFESION': profesion, 'SEXO': 'HOMBRES', 'SUMA': suma_h})
        profesiones_list.append({'AÑO': año, 'PROFESION': profesion, 'SEXO': 'MUJERES', 'SUMA': suma_m})

df_profesiones_suma = pd.DataFrame(profesiones_list)

color_map_prof = {
    'PROFESIONISTAS, TÉCNICOS Y TRABAJADORES DEL ARTE': '#0D5ED9',
    'TRABAJADORES DE LA EDUCACIÓN': '#1b0bca',
    'FUNCIONARIOS Y DIRECTIVOS DE LOS SECTORES PÚBLICO, PRIVADO Y SOCIAL': '#0D4DD9',
    'TRABAJADORES EN ACTIVIDADES AGRÍCOLAS, GANADERAS, SILVÍCOLAS, DE CAZA Y DE PESCA': '#1105eb',
    'TRABAJADORES INDUSTRIALES, ARTESANOS Y AYUDANTES': '#0D74D9',
    'CONDUCTORES Y AYUDANTES DE CONDUCTORES DE MAQUINARÍA  MÓVIL Y MEDIOS DE TRANSPORTE': '#00009c',
    'OFICINISTAS': '#209BDB',
    'COMERCIANTES': '#0DB0D9',
    'TRABAJADORES EN SERVICIO PERSONALES': '#0e0781',
    'TRABAJADORES EN SERVICIOS DE PROTECCIÓN Y VIGILANCIA Y FUERZAS ARMADAS': '#000071'
}

############################  GRÁFICOS  ############################

GRAPH_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor='rgba(10,14,30,0)',
    plot_bgcolor='rgba(10,14,30,0)',
    font=dict(family='DM Sans, sans-serif', color='#a8b8d8'),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
    xaxis=dict(gridcolor='rgba(100,120,180,0.1)', zeroline=False),
    yaxis=dict(gridcolor='rgba(100,120,180,0.1)', zeroline=False),
)

def create_general_graph():
    fig = go.Figure()
    quarters = [('PEA 1T','#4A90E2'),('PEA2T','#0CF5EF'),('PEA3T','#2563EB'),('PEA4T','#60A5FA')]
    for q, c in quarters:
        visible = True if q == 'PEA 1T' else 'legendonly'
        fig.add_trace(go.Scatter(
            x=df_pea['AÑO'], y=pd.to_numeric(df_pea[q], errors='coerce'),
            mode='lines+markers', name=q,
            line=dict(color=c, width=2.5),
            marker=dict(size=7),
            visible=visible,
            fill='tozeroy' if q == 'PEA 1T' else 'none',
            fillcolor='rgba(74,144,226,0.07)'
        ))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="Población Económicamente Activa por Trimestre", font=dict(size=13, color='#e2e8f0')),
        xaxis=dict(tickvals=[2020,2021,2022,2023,2024], gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False)
    )
    return fig

def create_sex_graph():
    df_h = df_pea_genero[df_pea_genero['SEXO'] == 'HOMBRES']
    df_m = df_pea_genero[df_pea_genero['SEXO'] == 'MUJERES']
    fig = go.Figure()
    for trimestre, df_g, base_color, fill_c in [
        ('PEA 1T', df_h, '#4A90E2', 'rgba(74,144,226,0.12)'),
        ('PEA 1T', df_m, '#F5A623', 'rgba(245,166,35,0.12)')
    ]:
        label = 'Hombres' if base_color == '#4A90E2' else 'Mujeres'
        fig.add_trace(go.Scatter(
            x=df_g['AÑO'], y=pd.to_numeric(df_g[trimestre], errors='coerce'),
            mode='lines+markers', name=label,
            line=dict(color=base_color, width=2.5),
            marker=dict(size=7),
            fill='tozeroy', fillcolor=fill_c
        ))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="PEA por Sexo (Primer Trimestre)", font=dict(size=13, color='#e2e8f0')),
        xaxis=dict(tickvals=[2020,2021,2022,2023,2024], gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False)
    )
    return fig

def create_sector_graph():
    df_g = df_sectores.groupby('AÑO')[['SECTOR PRIMARIO','SECTOR SECUNDARIO','SECTOR TERCIARIO','NO ESPECIFICADO']].mean().reset_index()
    colors = ['#0CD2F5','#2563EB','#0CF5E5','#4A90E2']
    fig = go.Figure()
    for col, c in zip(['SECTOR PRIMARIO','SECTOR SECUNDARIO','SECTOR TERCIARIO','NO ESPECIFICADO'], colors):
        fig.add_trace(go.Bar(x=df_g['AÑO'], y=df_g[col], name=col.title(), marker_color=c))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="Distribución por Sectores Económicos (Promedio por Año)", font=dict(size=13, color='#e2e8f0')),
        barmode='stack',
        xaxis=dict(tickvals=[2020,2021,2022,2023,2024], gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False)
    )
    return fig

def create_socioeconomic_graph():
    colors = [('#180bc1','rgba(24,11,193,0.3)'),('#0CE5F5','rgba(12,229,245,0.2)'),
              ('#0C52F5','rgba(12,82,245,0.15)'),('#60A5FA','rgba(96,165,250,0.1)')]
    fig = go.Figure()
    for (col, (lc, fc)) in zip(['Bajo','Medio bajo','Medio alto','Alto'], colors):
        fig.add_trace(go.Scatter(
            x=df_sectores_estratos['AÑO'], y=df_sectores_estratos[col],
            name=col, mode='lines+markers', fill='tozeroy',
            line=dict(color=lc, width=2), fillcolor=fc, marker=dict(size=6)
        ))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="Estratificación Socioeconómica por Año", font=dict(size=13, color='#e2e8f0')),
        xaxis=dict(tickvals=[2020,2021,2022,2023,2024], gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False)
    )
    return fig

def create_salarios_graph():
    df_avg = df_salarios.groupby('AÑO').mean(numeric_only=True).reset_index()
    cols = ['HASTA UN SALARIO MÍNIMO','MÁS DE 1 HASTA 2 SALARIOS MÍNIMOS',
            'MÁS DE 2 HASTA 3 SALARIOS MÍNIMOS','MÁS DE 3 HASTA 5 SALARIOS MÍNIMOS',
            'MÁS DE 5 SALARIOS MÍNIMOS','NO RECIBE INGRESOS']
    colors = ['#0C67F5','#0CF5EF','#3357FF','#0601fe','#0C9FF5','#3333FF']
    labels = ['≤1 S.M.','1-2 S.M.','2-3 S.M.','3-5 S.M.','>5 S.M.','Sin ingreso']
    fig = go.Figure()
    for col, c, lbl in zip(cols, colors, labels):
        fig.add_trace(go.Bar(y=df_avg['AÑO'], x=df_avg[col], name=lbl, orientation='h', marker_color=c))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="Distribución de Rangos Salariales por Año", font=dict(size=13, color='#e2e8f0')),
        barmode='stack',
        xaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(gridcolor='rgba(100,120,180,0.1)', zeroline=False, type='category')
    )
    return fig

def create_edad_graph():
    age_groups = ['15-19 AÑOS','20-29 AÑOS','30-39 AÑOS','40-49 AÑOS','50-59 AÑOS','60 AÑOS Y MÁS']
    colors = ['#0C9BF5','#0C52F5','#4A90E2','#0CA7F5','#0CF5EF','#0C14F5']
    labels = ['15-19','20-29','30-39','40-49','50-59','60+']
    fig = go.Figure()
    for ag, c, lbl in zip(age_groups, colors, labels):
        fig.add_trace(go.Bar(y=df_edad_avg['AÑO'], x=df_edad_avg[ag], name=lbl, orientation='h', marker_color=c))
    fig.update_layout(**GRAPH_LAYOUT,
        title=dict(text="Distribución de la PEA por Grupos de Edad", font=dict(size=13, color='#e2e8f0')),
        barmode='stack',
        xaxis=dict(tickformat=',', gridcolor='rgba(100,120,180,0.1)', zeroline=False),
        yaxis=dict(gridcolor='rgba(100,120,180,0.1)', zeroline=False, type='category')
    )
    return fig

def create_treemap(df, title):
    fig = px.treemap(df, path=['PROFESION','AÑO','SEXO'], values='SUMA',
                     color='PROFESION', color_discrete_map=color_map_prof, title=title)
    fig.update_layout(
        paper_bgcolor='rgba(10,14,30,0)', plot_bgcolor='rgba(10,14,30,0)',
        font=dict(color='white', family='DM Sans, sans-serif'),
        margin=dict(l=10, r=10, t=40, b=10),
        title=dict(font=dict(size=13, color='#e2e8f0'))
    )
    fig.update_traces(textfont=dict(size=11))
    return fig

############################  ESTILOS  ############################

CARD_STYLE = {
    'background': 'linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(20,30,60,0.9) 100%)',
    'border': '1px solid rgba(74,144,226,0.2)',
    'borderRadius': '12px',
    'padding': '20px',
    'height': '100%',
}

METRIC_CARD = {
    'background': 'linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(20,30,60,0.9) 100%)',
    'border': '1px solid rgba(74,144,226,0.25)',
    'borderRadius': '10px',
    'padding': '18px 16px',
    'textAlign': 'center',
    'transition': 'transform 0.2s ease',
}

def metric_card(label, value, accent='#4A90E2', icon=''):
    return html.Div([
        html.Div(icon, style={'fontSize': '22px', 'marginBottom': '6px'}),
        html.Div(value, style={
            'fontSize': '26px', 'fontWeight': '700', 'color': accent,
            'fontFamily': 'DM Sans, sans-serif', 'letterSpacing': '-0.5px'
        }),
        html.Div(label, style={
            'fontSize': '11px', 'color': '#64748b', 'marginTop': '4px',
            'fontFamily': 'DM Sans, sans-serif', 'textTransform': 'uppercase', 'letterSpacing': '0.08em'
        })
    ], style=METRIC_CARD)

def section_divider(title, subtitle=None):
    return html.Div([
        html.Div(style={'height': '1px', 'background': 'linear-gradient(90deg, rgba(74,144,226,0.6) 0%, rgba(74,144,226,0) 100%)', 'marginBottom': '16px'}),
        html.Div(title, style={'fontSize': '13px', 'fontWeight': '700', 'color': '#4A90E2', 'textTransform': 'uppercase', 'letterSpacing': '0.12em', 'fontFamily': 'DM Sans, sans-serif'}),
        html.Div(subtitle or '', style={'fontSize': '12px', 'color': '#475569', 'marginTop': '3px', 'fontFamily': 'DM Sans, sans-serif'}),
    ], style={'marginTop': '32px', 'marginBottom': '16px'})

############################  APP  ############################

CUSTOM_CSS = """
    body {
        background: #060b18 !important;
        background-image: radial-gradient(ellipse at 20% 20%, rgba(37,99,235,0.06) 0%, transparent 50%),
                          radial-gradient(ellipse at 80% 80%, rgba(12,229,245,0.04) 0%, transparent 50%);
        min-height: 100vh;
    }
    .dash-graph .modebar { background: transparent !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #060b18; }
    ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
    .Select-control { background-color: #0f172a !important; border-color: rgba(74,144,226,0.3) !important; }
    .Select-menu-outer { background-color: #0f172a !important; }
    .Select-option { color: #a8b8d8 !important; }
    .Select-value-label { color: #e2e8f0 !important; }
"""

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap'
    ]
)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Economía y Trabajo Morelos</title>
        {%favicon%}
        {%css%}
        <style>''' + CUSTOM_CSS + '''</style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dbc.Container([

        # ── HEADER ──────────────────────────────────────────────────────────
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("MORELOS", style={
                            'fontSize': '11px', 'fontWeight': '700', 'color': '#4A90E2',
                            'letterSpacing': '0.2em', 'fontFamily': 'DM Sans, sans-serif',
                            'textTransform': 'uppercase'
                        }),
                        html.H1("Economía y Trabajo", style={
                            'fontSize': 'clamp(28px,4vw,52px)', 'fontWeight': '700',
                            'color': '#f1f5f9', 'fontFamily': 'DM Serif Display, serif',
                            'lineHeight': '1.1', 'margin': '6px 0 8px'
                        }),
                        html.P("Radiografía del mercado laboral morelense · 2020 – 2024", style={
                            'color': '#64748b', 'fontSize': '14px', 'fontFamily': 'DM Sans, sans-serif',
                            'margin': 0
                        })
                    ])
                ], width=8),
                dbc.Col([
                    html.Div([
                        html.Div("2020–2024", style={
                            'fontSize': '40px', 'fontWeight': '700', 'color': 'rgba(74,144,226,0.15)',
                            'fontFamily': 'DM Serif Display, serif', 'textAlign': 'right',
                            'lineHeight': '1'
                        }),
                        html.Div("ENOE · INEGI · IMSS", style={
                            'fontSize': '10px', 'color': '#334155', 'textAlign': 'right',
                            'fontFamily': 'DM Sans, sans-serif', 'letterSpacing': '0.1em'
                        })
                    ])
                ], width=4, className='d-flex align-items-center justify-content-end')
            ], align='center'),
        ], style={
            'borderBottom': '1px solid rgba(74,144,226,0.15)',
            'paddingTop': '36px', 'paddingBottom': '28px', 'marginBottom': '8px'
        }),

        # ── MÉTRICAS CLAVE ───────────────────────────────────────────────────
        section_divider("Indicadores clave 2024", "Snapshot del panorama laboral en Morelos"),

        dbc.Row([
            dbc.Col(metric_card("Población ocupada", df_general['Población ocupada'], '#4A90E2', '👷'), width=6, md=4, lg=True, className='mb-3'),
            dbc.Col(metric_card("PEA", df_general['Población económicamente activa'], '#0CF5EF', '📊'), width=6, md=4, lg=True, className='mb-3'),
            dbc.Col(metric_card("Ingreso mensual", df_general['Ingreso promedio mensual'], '#60A5FA', '💰'), width=6, md=4, lg=True, className='mb-3'),
            dbc.Col(metric_card("Formalidad", df_general['Formalidad'], '#2563EB', '✅'), width=6, md=4, lg=True, className='mb-3'),
            dbc.Col(metric_card("Informalidad", df_general['Informalidad'], '#F59E0B', '⚠️'), width=6, md=4, lg=True, className='mb-3'),
        ], className='g-3'),

        # Barra hombres / mujeres
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("♂ Hombres", style={'color':'#4A90E2','fontWeight':'600','fontSize':'13px','fontFamily':'DM Sans, sans-serif'}),
                        html.Span(f"  {df_general['Hombres']}", style={'color':'#94a3b8','fontSize':'13px','fontFamily':'DM Sans, sans-serif'})
                    ]),
                    html.Div(style={
                        'height':'6px','borderRadius':'3px','marginTop':'6px',
                        'background':f'linear-gradient(90deg, #4A90E2 {df_general["Hombres"]}, rgba(74,144,226,0.1) {df_general["Hombres"]})'
                    })
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.Span("♀ Mujeres", style={'color':'#a78bfa','fontWeight':'600','fontSize':'13px','fontFamily':'DM Sans, sans-serif'}),
                        html.Span(f"  {df_general['Mujeres']}", style={'color':'#94a3b8','fontSize':'13px','fontFamily':'DM Sans, sans-serif'})
                    ]),
                    html.Div(style={
                        'height':'6px','borderRadius':'3px','marginTop':'6px',
                        'background':f'linear-gradient(90deg, #a78bfa {df_general["Mujeres"]}, rgba(167,139,250,0.1) {df_general["Mujeres"]})'
                    })
                ], width=6)
            ])
        ], style={**CARD_STYLE, 'marginTop': '12px'}),

        # ── BLOQUE 1: PEA ────────────────────────────────────────────────────
        section_divider("Evolución de la PEA", "¿Cómo ha cambiado la participación laboral entre 2020 y 2024?"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Label("Desglose:", style={'color':'#64748b','fontSize':'11px','fontFamily':'DM Sans, sans-serif','marginRight':'10px'}),
                        dcc.Dropdown(
                            id="dropdown-chart",
                            options=[
                                {"label": "PEA Total por Trimestre", "value": "GENERAL"},
                                {"label": "PEA por Sexo", "value": "SEXO"}
                            ],
                            value="GENERAL",
                            clearable=False,
                            style={'width':'220px','display':'inline-block','fontSize':'12px'}
                        )
                    ], style={'marginBottom':'12px','display':'flex','alignItems':'center'}),
                    dcc.Graph(id='chart-container', style={'height':'350px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, lg=6, className='mb-3'),

            dbc.Col([
                html.Div([
                    dcc.Graph(figure=create_edad_graph(), style={'height':'350px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, lg=6, className='mb-3'),
        ]),

        # ── BLOQUE 2: SECTORES ───────────────────────────────────────────────
        section_divider("Composición sectorial", "El sector terciario domina la estructura productiva de Morelos"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=create_sector_graph(), style={'height':'380px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, className='mb-3')
        ]),

        # ── BLOQUE 3: INGRESOS & ESTRATOS ───────────────────────────────────
        section_divider("Ingresos y estructura socioeconómica", "¿Cuánto gana y a qué estrato pertenece la población trabajadora?"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=create_socioeconomic_graph(), style={'height':'340px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, lg=5, className='mb-3'),

            dbc.Col([
                html.Div([
                    dcc.Graph(figure=create_salarios_graph(), style={'height':'340px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, lg=7, className='mb-3'),
        ]),

        # ── BLOQUE 4: OCUPACIONES ────────────────────────────────────────────
        section_divider("Ocupaciones por sexo", "¿En qué trabajan hombres y mujeres en Morelos?"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Año:", style={'color':'#64748b','fontSize':'11px','fontFamily':'DM Sans, sans-serif','marginRight':'10px'}),
                    dcc.Dropdown(
                        id="dropdown-año",
                        options=[{"label": str(y), "value": y} for y in sorted(df_profesiones['AÑO'].unique())],
                        value=2024, clearable=False,
                        style={'width':'140px','display':'inline-block','fontSize':'12px'}
                    )
                ], style={'marginBottom':'12px','display':'flex','alignItems':'center'})
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='treemap-profesiones', style={'height':'460px'}, config={'displayModeBar':False})
                ], style=CARD_STYLE)
            ], width=12, className='mb-3')
        ]),

        # ── FOOTER ───────────────────────────────────────────────────────────
        html.Div([
            html.Div(style={'height':'1px','background':'rgba(74,144,226,0.1)','marginBottom':'28px'}),
            dbc.Row([
                dbc.Col([
                    html.P("Fuentes de datos", style={'color':'#4A90E2','fontSize':'11px','fontWeight':'700','textTransform':'uppercase','letterSpacing':'0.1em','fontFamily':'DM Sans, sans-serif','marginBottom':'12px'}),
                    html.Div([
                        html.A("ENOE – INEGI", href="https://www.inegi.org.mx/programas/enoe/", target="_blank",
                               style={'color':'#4A90E2','fontSize':'12px','fontFamily':'DM Sans, sans-serif','marginRight':'20px','textDecoration':'none'}),
                        html.A("Observatorio Laboral SNE", href="https://www.observatoriolaboral.gob.mx/static/estudios-publicaciones/Informe_IMSS.html", target="_blank",
                               style={'color':'#4A90E2','fontSize':'12px','fontFamily':'DM Sans, sans-serif','marginRight':'20px','textDecoration':'none'}),
                        html.A("ILMM – INEGI", href="https://www.inegi.org.mx/programas/ilmm/#datos_abiertos", target="_blank",
                               style={'color':'#4A90E2','fontSize':'12px','fontFamily':'DM Sans, sans-serif','marginRight':'20px','textDecoration':'none'}),
                        html.A("SNIM", href="http://www.snim.rami.gob.mx/", target="_blank",
                               style={'color':'#4A90E2','fontSize':'12px','fontFamily':'DM Sans, sans-serif','textDecoration':'none'}),
                    ])
                ], width=8),
                dbc.Col([
                    html.Div([
                        html.P("Lic. C. Pol. Eduardo Cabrera Gutiérrez", style={'color':'#e2e8f0','fontSize':'12px','fontFamily':'DM Sans, sans-serif','fontWeight':'600','margin':'0','textAlign':'right'}),
                        html.P("cabardo.gutz@gmail.com", style={'color':'#475569','fontSize':'11px','fontFamily':'DM Sans, sans-serif','margin':'2px 0 0','textAlign':'right'}),
                    ])
                ], width=4, className='d-flex align-items-center justify-content-end')
            ]),
            html.Div(style={'height':'32px'})
        ])

    ], fluid=True, style={'maxWidth':'1280px', 'padding':'0 24px'})
], style={'backgroundColor':'#060b18', 'minHeight':'100vh'})

############################  CALLBACKS  ############################

@app.callback(
    [Output('treemap-profesiones','figure'), Output('chart-container','figure')],
    [Input('dropdown-año','value'), Input('dropdown-chart','value')]
)
def update_graphs(selected_año, selected_value):
    filtered = df_profesiones_suma[df_profesiones_suma['AÑO'] == selected_año]
    treemap_fig = create_treemap(filtered, f"Ocupaciones por Profesión y Sexo · {selected_año}")
    chart_fig = create_general_graph() if selected_value == 'GENERAL' else create_sex_graph()
    return treemap_fig, chart_fig

if __name__ == '__main__':
    app.run_server(debug=True)
