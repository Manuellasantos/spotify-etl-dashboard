import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Dashboard Spotify',
    page_icon='🎀',
    layout='wide'
)

st.markdown("""
<style>

.main {
    background-color: #fff0f6;
}

h1, h2, h3 {
    color: #ff4fa3;
    font-family: Arial;
}

section[data-testid="stSidebar"] {
    background-color: #ffc0db;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    border: 2px solid #ff8dc7;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.title('🎀 Dashboard Spotify')
st.markdown('### ✨ Análise de músicas populares do Spotify')

# =====================================================
# EXTRACT (EXTRAÇÃO)
# =====================================================

arquivo = 'high_popularity_spotify_data.csv'

spotify = pd.read_csv(arquivo)

# =====================================================
# TRANSFORM (TRANSFORMAÇÃO)
# =====================================================

# Remove linhas duplicadas
spotify = spotify.drop_duplicates()

# Remove valores nulos
spotify = spotify.dropna()

# Renomeia colunas
spotify = spotify.rename(columns={
    'track_name': 'musica',
    'track_artist': 'artista',
    'track_popularity': 'popularidade',
    'playlist_genre': 'genero',
    'duration_ms': 'duracao_ms',
    'danceability': 'musica_dancante'
})

# Cria coluna de duração em minutos
spotify['duracao_minutos'] = spotify['duracao_ms'] / 60000

# Arredonda valores
spotify['duracao_minutos'] = spotify['duracao_minutos'].round(2)

# Filtra músicas populares
spotify_final = spotify[spotify['popularidade'] >= 80]

# =====================================================
# LOAD (SALVAR CSV)
# =====================================================

spotify_final.to_csv('spotify_tratado.csv', index=False)

st.sidebar.title('🎀 Menu')

pagina = st.sidebar.radio(
    'Navegação',
    [
        '🏠 Visão Geral',
        '🎤 Artistas',
        '🎧 Gêneros',
        '⚡ Energia',
        '📋 Tabela'
    ]
)

# =====================================================
# FILTROS
# =====================================================

st.sidebar.markdown('## 🎛️ Filtros')

generos_disponiveis = spotify_final['genero'].unique()

genero_escolhido = st.sidebar.multiselect(
    'Escolha os gêneros',
    generos_disponiveis,
    default=generos_disponiveis
)

spotify_filtrado = spotify_final[
    spotify_final['genero'].isin(genero_escolhido)
]

# =====================================================
# VISÃO GERAL
# =====================================================

if pagina == '🏠 Visão Geral':

    st.subheader('💖 Informações Gerais')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            '🎵 Quantidade de músicas',
            len(spotify_filtrado)
        )

    with col2:
        st.metric(
            '⭐ Popularidade média',
            round(
                spotify_filtrado['popularidade'].mean(),
                2
            )
        )

    with col3:
        st.metric(
            '🎧 Quantidade de gêneros',
            spotify_filtrado['genero'].nunique()
        )

    st.markdown('---')

    st.subheader('🌸 Top 10 Artistas')

    top_artistas = (
        spotify_filtrado['artista']
        .value_counts()
        .head(10)
    )

    grafico_artistas = px.bar(
        x=top_artistas.index,
        y=top_artistas.values,
        color=top_artistas.values,
        color_continuous_scale='RdPu',
        title='🎤 Top 10 Artistas'
    )

    st.plotly_chart(grafico_artistas, use_container_width=True)

# =====================================================
# ARTISTAS
# =====================================================

elif pagina == '🎤 Artistas':

    st.subheader('🎤 Artistas Mais Frequentes')

    top_artistas = (
        spotify_filtrado['artista']
        .value_counts()
        .head(15)
    )

    grafico = px.bar(
        x=top_artistas.values,
        y=top_artistas.index,
        orientation='h',
        color=top_artistas.values,
        color_continuous_scale='RdPu',
        title='🎵 Ranking de Artistas'
    )

    st.plotly_chart(grafico, use_container_width=True)

# =====================================================
# GÊNEROS
# =====================================================

elif pagina == '🎧 Gêneros':

    st.subheader('🎧 Distribuição dos Gêneros')

    generos = (
        spotify_filtrado['genero']
        .value_counts()
    )

    grafico_generos = px.pie(
        values=generos.values,
        names=generos.index,
        hole=0.5,
        title='🍩 Distribuição dos Gêneros'
    )

    st.plotly_chart(grafico_generos, use_container_width=True)

# =====================================================
# ENERGIA
# =====================================================

elif pagina == '⚡ Energia':

    st.subheader('⚡ Música Dançante x Energia')

    grafico_scatter = px.scatter(
        spotify_filtrado,
        x='musica_dancante',
        y='energy',
        color='genero',
        size='popularidade',
        hover_data=['musica', 'artista'],
        title='⚡ Música Dançante x Energia'
    )

    st.plotly_chart(grafico_scatter, use_container_width=True)

# =====================================================
# TABELA
# =====================================================

elif pagina == '📋 Tabela':

    st.subheader('📋 Dados Tratados')

    st.dataframe(spotify_filtrado)


st.markdown('---')

st.markdown(
    '<center>💖 Dashboard feito com Python + Streamlit 💖</center>',
    unsafe_allow_html=True
)