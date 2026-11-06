import html
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# Arquivos
PASTA = Path(__file__).parent
ENTRADA = PASTA / 'high_popularity_spotify_data.csv'
SAIDA = PASTA / 'spotify_tratado.csv'
CSS = PASTA / 'style.css'

# Cores
SUPERFICIE = '#0B1020'
GRADE = '#1A2340'
COBALTO = '#1558C9'
COBALTO_CLARO = '#6FA0FF'
LIMA = '#D4FF24'
TEXTO = '#F2F5FA'
SUAVE = '#8EA0C2'

ESCALA = [[0, COBALTO], [1, LIMA]]
ESCALA_CALOR = [[0, SUPERFICIE], [0.5, COBALTO], [1, LIMA]]
ESCALA_DIVERGENTE = [[0, COBALTO], [0.5, SUPERFICIE], [1, LIMA]]

ATRIBUTOS = {
    'energia': 'Energia', 'dancabilidade': 'Dançabilidade',
    'valencia': 'Positividade', 'acustica': 'Acústica',
    'fala': 'Fala', 'ao_vivo': 'Ao vivo', 'volume': 'Volume (dB)',
    'andamento': 'Andamento (BPM)', 'duracao_min': 'Duração (min)',
    'popularidade': 'Popularidade'
}

PERFIL = ['energia', 'dancabilidade', 'valencia', 'acustica', 'fala', 'ao_vivo']
COLUNAS_TABELA = [
    'musica', 'artista', 'genero', 'popularidade', 'ano',
    'duracao_min', 'energia', 'dancabilidade', 'valencia'
]

# Página
st.set_page_config(page_title='Dashboard Spotify', layout='wide')

if CSS.exists():
    st.markdown(f'<style>{CSS.read_text(encoding="utf-8")}</style>', unsafe_allow_html=True)

# Aparência dos gráficos
eixo = dict(
    gridcolor=GRADE, zerolinecolor=GRADE, linecolor=GRADE,
    title=dict(font=dict(color=SUAVE))
)

pio.templates['neo'] = go.layout.Template(layout=dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=TEXTO, family='Inter, sans-serif', size=13),
    colorway=[LIMA, COBALTO_CLARO, '#8CFF9E', '#B58CFF', '#FFB86B',
              '#FF6B9A', '#5CE1E6', COBALTO],
    xaxis=eixo,
    yaxis=eixo,
    coloraxis=dict(colorscale=ESCALA, colorbar=dict(outlinewidth=0, thickness=12)),
    margin=dict(l=10, r=10, t=10, b=10),
    hoverlabel=dict(
        bgcolor=SUPERFICIE, font=dict(color=TEXTO), bordercolor=COBALTO
    ),
    legend=dict(bgcolor='rgba(0,0,0,0)')
))
pio.templates.default = 'neo'

st.markdown(
    '<div class="hero"><div class="hero-topo"><div><h1>Dashboard Spotify</h1>'
    '<p>Análise das músicas mais populares do Spotify</p></div></div></div>',
    unsafe_allow_html=True
)

# Tratamento dos dados
@st.cache_data
def executar_etl(caminho):
    df = pd.read_csv(caminho)
    df = df.rename(columns={
        'track_id': 'id_faixa', 'track_name': 'musica',
        'track_artist': 'artista', 'track_popularity': 'popularidade',
        'playlist_genre': 'genero', 'playlist_subgenre': 'subgenero',
        'track_album_name': 'album', 'track_album_release_date': 'lancamento',
        'duration_ms': 'duracao_ms', 'energy': 'energia',
        'danceability': 'dancabilidade', 'valence': 'valencia',
        'acousticness': 'acustica', 'speechiness': 'fala',
        'liveness': 'ao_vivo', 'loudness': 'volume', 'tempo': 'andamento',
        'mode': 'modo'
    })
    # Mantém a música com maior popularidade
    df = df.drop_duplicates()
    df = df.sort_values('popularidade', ascending=False).drop_duplicates('id_faixa')
    df = df.dropna(subset=['musica', 'artista', 'popularidade', 'genero', 'duracao_ms'])
    df['ano'] = pd.to_numeric(df['lancamento'].astype(str).str[:4], errors='coerce')
    df['duracao_min'] = (df['duracao_ms'] / 60000).round(2)
    df['modo'] = df['modo'].map({1: 'Maior', 0: 'Menor'})
    df.to_csv(SAIDA, index=False)
    return df.reset_index(drop=True)

def mostrar(fig, altura=380):
    fig.update_layout(height=altura)
    st.plotly_chart(fig, config={'displayModeBar': False})

def insight(titulo, texto):
    st.markdown(
        f'<div class="insight"><span>{html.escape(titulo)}</span>'
        f'{html.escape(texto)}</div>',
        unsafe_allow_html=True
    )

def agrupar(base, coluna):
    return base.groupby(coluna).agg(
        musicas=('musica', 'size'), popularidade=('popularidade', 'mean')
    ).reset_index()

# Carrega os dados
try:
    spotify = executar_etl(ENTRADA)
except FileNotFoundError:
    st.error(f'Arquivo "{ENTRADA.name}" não encontrado. Coloque-o na mesma pasta do app.')
    st.stop()

# Filtros
ano_min = int(spotify['ano'].min())
ano_max = int(spotify['ano'].max())
generos_ordenados = spotify['genero'].value_counts().index.tolist()

with st.sidebar:
    st.markdown('<p class="rotulo">Filtros</p>', unsafe_allow_html=True)
    pop_min = st.slider(
        'Popularidade mínima', int(spotify['popularidade'].min()), 100,
        int(spotify['popularidade'].min())
    )
    anos = st.slider(
        'Ano de lançamento', ano_min, ano_max,
        (max(ano_min, 2010), ano_max)
    )
    generos = st.multiselect('Gêneros', generos_ordenados, default=generos_ordenados)

df = spotify[
    (spotify['popularidade'] >= pop_min)
    & (spotify['genero'].isin(generos))
    & (spotify['ano'].between(*anos) | spotify['ano'].isna())
]

if df.empty:
    st.warning('Nenhuma música encontrada. Ajuste os filtros.')
    st.stop()

# Abas
aba_geral, aba_generos, aba_artistas, aba_evolucao, aba_perfil, aba_dados = st.tabs(
    ['Panorama', 'Gêneros', 'Artistas', 'Evolução', 'Perfil sonoro', 'Dados']
)

# Panorama
with aba_geral:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric('Músicas únicas', f'{len(df):,}'.replace(',', '.'))
    c2.metric('Artistas', f"{df['artista'].nunique():,}".replace(',', '.'))
    c3.metric('Popularidade média', f"{df['popularidade'].mean():.1f}")
    c4.metric('Duração média', f"{df['duracao_min'].mean():.1f} min")
    c5.metric('Lançamento mediano', f"{df['ano'].median():.0f}")
    contagem = df['genero'].value_counts()
    acima_80 = (df['popularidade'] >= 80).mean() * 100
    insight(
        'Resumo',
        f"{' e '.join(contagem.index[:2])} representam "
        f"{contagem.iloc[:2].sum() / len(df) * 100:.0f}% das músicas. "
        f"{acima_80:.0f}% têm popularidade igual ou maior que 80."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader('Gêneros com mais músicas')
        top = contagem.head(10).rename_axis('genero').reset_index(name='musicas')
        top = top.sort_values('musicas')
        fig = px.bar(
            top, x='musicas', y='genero', orientation='h', color='musicas',
            labels={'musicas': 'Músicas', 'genero': ''}
        )
        fig.update_coloraxes(showscale=False)
        mostrar(fig)
    with col_b:
        st.subheader('Distribuição da popularidade')
        fig = px.histogram(
            df, x='popularidade', nbins=33, color_discrete_sequence=[LIMA],
            labels={'popularidade': 'Popularidade'}
        )
        fig.add_vline(
            x=80, line_dash='dot', line_color=COBALTO_CLARO,
            annotation_text='80', annotation_font_color=COBALTO_CLARO
        )
        fig.update_layout(yaxis_title='Músicas', bargap=0.08)
        mostrar(fig)
# Gêneros
with aba_generos:
    minimo_g = st.slider('Mínimo de músicas por gênero', 5, 50, 15, key='min_g')
    por_genero = agrupar(df, 'genero')
    por_genero = por_genero[por_genero['musicas'] >= minimo_g]
    if por_genero.empty:
        st.info('Nenhum gênero atinge esse mínimo. Reduza o valor.')
    else:
        melhor = por_genero.loc[por_genero['popularidade'].idxmax()]
        ordem = por_genero.sort_values('musicas', ascending=False)['genero'].tolist()
        perfil = df[df['genero'].isin(ordem)].groupby('genero')[PERFIL].mean().loc[ordem]
        insight(
            'Destaques',
            f"{melhor['genero']} tem a maior popularidade média "
            f"({melhor['popularidade']:.1f}), com {int(melhor['musicas'])} músicas. "
            f"{perfil['energia'].idxmax()} tem a maior média de energia e "
            f"{perfil['acustica'].idxmax()} a maior média de acústica."
        )
        altura = 120 + 30 * len(por_genero)
        col_a, col_b = st.columns([2, 3])
        with col_a:
            st.subheader('Popularidade média')
            fig = px.scatter(
                por_genero.sort_values('popularidade'),
                x='popularidade', y='genero', size='musicas',
                color='popularidade', size_max=26,
                labels={'popularidade': 'Popularidade média', 'genero': '', 'musicas': 'Músicas'}
            )
            fig.update_coloraxes(showscale=False)
            mostrar(fig, altura)
        with col_b:
            st.subheader('Perfil sonoro por gênero')
            fig = px.imshow(
                perfil.rename(columns=ATRIBUTOS), text_auto='.2f', aspect='auto',
                color_continuous_scale=ESCALA_CALOR, labels={'color': 'Média'}
            )
            fig.update_traces(xgap=3, ygap=3)
            fig.update_xaxes(side='top')
            fig.update_coloraxes(showscale=False)
            mostrar(fig, altura)
# Artistas
with aba_artistas:
    minimo_a = st.slider('Mínimo de músicas por artista', 2, 10, 3, key='min_a')
    por_artista = agrupar(df, 'artista')
    destaque = por_artista[por_artista['musicas'] >= minimo_a].copy()
    if destaque.empty:
        st.info('Nenhum artista atinge esse mínimo. Reduza o valor.')
    else:
        mais_faixas = por_artista.loc[por_artista['musicas'].idxmax()]
        mais_popular = destaque.loc[destaque['popularidade'].idxmax()]
        insight(
            'Artistas em destaque',
            f"{mais_faixas['artista']} tem mais músicas ({int(mais_faixas['musicas'])}). "
            f"Entre os artistas com pelo menos {minimo_a} músicas, "
            f"{mais_popular['artista']} tem a maior popularidade média "
            f"({mais_popular['popularidade']:.1f})."
        )
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.subheader('Quantidade de músicas x popularidade média')
            marcados = (
                set(destaque.nlargest(6, 'popularidade').index)
                | set(destaque.nlargest(4, 'musicas').index)
            )
            destaque['rotulo'] = [
                artista if indice in marcados else ''
                for indice, artista in zip(destaque.index, destaque['artista'])
            ]
            fig = px.scatter(
                destaque, x='musicas', y='popularidade', color='popularidade',
                text='rotulo', hover_name='artista', opacity=0.85,
                labels={'musicas': 'Músicas no ranking', 'popularidade': 'Popularidade média'}
            )
            fig.update_traces(
                textposition='top center', marker=dict(size=11),
                textfont=dict(color=TEXTO, size=11)
            )
            fig.update_coloraxes(showscale=False)
            mostrar(fig, 460)
        with col_b:
            st.subheader('Mais presentes')
            top = por_artista.nlargest(10, 'musicas').sort_values('musicas')
            fig = px.bar(
                top, x='musicas', y='artista', orientation='h', color='popularidade',
                labels={'musicas': 'Músicas', 'artista': '', 'popularidade': 'Pop. média'}
            )
            mostrar(fig, 460)

# Evolução
with aba_evolucao:
    por_ano = (
        df.dropna(subset=['ano']).groupby('ano')
        .agg(
            musicas=('musica', 'size'), duracao=('duracao_min', 'mean'),
            energia=('energia', 'mean'), dancabilidade=('dancabilidade', 'mean'),
            valencia=('valencia', 'mean')
        )
        .reset_index()
    )
    robustos = por_ano[por_ano['musicas'] >= 20]
    if len(robustos) >= 2:
        ini, fim = robustos.iloc[0], robustos.iloc[-1]
        insight(
            'Comparação entre anos',
            f"A duração média foi de {ini['duracao']:.1f} min em {int(ini['ano'])} "
            f"e de {fim['duracao']:.1f} min em {int(fim['ano'])}. "
            f"A dançabilidade foi de {ini['dancabilidade']:.2f} para "
            f"{fim['dancabilidade']:.2f}. O ano de {int(fim['ano'])} representa "
            f"{fim['musicas'] / len(df) * 100:.0f}% das músicas filtradas."
        )
    st.subheader('Músicas por ano de lançamento')
    fig = px.bar(
        por_ano, x='ano', y='musicas', labels={'ano': 'Ano', 'musicas': 'Músicas'},
        color_discrete_sequence=[COBALTO]
    )
    fig.update_layout(bargap=0.15)
    mostrar(fig, 300)
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader('Duração média (minutos)')
        fig = px.line(
            por_ano, x='ano', y='duracao', markers=True,
            labels={'ano': 'Ano', 'duracao': 'Minutos'}
        )
        mostrar(fig)
    with col_b:
        st.subheader('Características médias')
        longo = por_ano.melt(
            'ano', ['energia', 'dancabilidade', 'valencia'],
            var_name='atributo', value_name='media'
        )
        longo['atributo'] = longo['atributo'].map(ATRIBUTOS)
        fig = px.line(
            longo, x='ano', y='media', color='atributo', markers=True,
            labels={'ano': 'Ano', 'media': 'Média (0 a 1)', 'atributo': ''}
        )
        fig.update_layout(legend=dict(orientation='h', y=1.12, x=0))
        mostrar(fig)

# Perfil sonoro
with aba_perfil:
    corr = df[list(ATRIBUTOS)].corr()
    com_pop = corr['popularidade'].drop('popularidade')
    forte_pop = com_pop.abs().idxmax()
    sem_pop = corr.drop('popularidade').drop(columns='popularidade')
    pares = sem_pop.where(np.triu(np.ones(sem_pop.shape, dtype=bool), 1)).stack()
    par = pares.abs().idxmax()
    relacao = 'fraca' if abs(com_pop[forte_pop]) < 0.3 else 'moderada'
    insight(
        'Correlações',
        f"A característica mais relacionada à popularidade é {ATRIBUTOS[forte_pop]} "
        f"(r = {com_pop[forte_pop]:+.2f}). A relação é {relacao}. "
        f"A maior correlação entre características é {ATRIBUTOS[par[0]]} e "
        f"{ATRIBUTOS[par[1]]} (r = {pares.loc[par]:+.2f})."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader('Correlação entre características')
        nomes = [ATRIBUTOS[coluna] for coluna in corr.columns]
        fig = px.imshow(
            corr.values, x=nomes, y=nomes, zmin=-1, zmax=1, text_auto='.2f',
            color_continuous_scale=ESCALA_DIVERGENTE, aspect='auto'
        )
        fig.update_traces(xgap=2, ygap=2)
        fig.update_coloraxes(showscale=False)
        mostrar(fig, 480)
    with col_b:
        st.subheader('Compare duas características')
        s1, s2 = st.columns(2)
        eixo_x = s1.selectbox('Eixo X', list(ATRIBUTOS), index=0, format_func=ATRIBUTOS.get)
        eixo_y = s2.selectbox('Eixo Y', list(ATRIBUTOS), index=6, format_func=ATRIBUTOS.get)
        fig = px.scatter(
            df, x=eixo_x, y=eixo_y, color='popularidade', opacity=0.6,
            hover_data=['musica', 'artista'], labels=ATRIBUTOS
        )
        fig.update_traces(marker=dict(size=7))
        mostrar(fig, 400)

# Dados
with aba_dados:
    st.subheader('Dados tratados')
    busca = st.text_input('Buscar música ou artista')
    tabela = df[COLUNAS_TABELA]
    if busca:
        tabela = tabela[
            tabela['musica'].str.contains(busca, case=False, na=False)
            | tabela['artista'].str.contains(busca, case=False, na=False)
        ]
    st.dataframe(tabela.sort_values('popularidade', ascending=False), hide_index=True)
    st.download_button(
        'Baixar CSV filtrado', tabela.to_csv(index=False).encode('utf-8'),
        file_name='spotify_filtrado.csv', mime='text/csv'
    )

st.markdown(
    '<div class="rodape">Feito com <b>Python</b>, <b>pandas</b>, '
    '<b>Plotly</b> e <b>Streamlit</b></div>',
    unsafe_allow_html=True
)
