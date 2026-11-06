# Dashboard Spotify

Dashboard feito em Python para explorar dados de músicas populares do Spotify. O projeto prepara os dados com um processo ETL e apresenta os resultados em gráficos e tabelas interativas.

## Tecnologias

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

## Sobre o dashboard

O dashboard está dividido em seis abas:

- **Panorama:** mostra a quantidade de músicas e artistas, a popularidade média, a duração média e a distribuição das músicas por gênero e popularidade.
- **Gêneros:** compara a popularidade média e as características sonoras de cada gênero.
- **Artistas:** relaciona a quantidade de músicas de cada artista com sua popularidade média.
- **Evolução:** apresenta a quantidade de lançamentos por ano, a duração média e mudanças em algumas características das músicas.
- **Perfil sonoro:** mostra a correlação entre as características musicais e permite comparar duas delas em um gráfico.
- **Dados:** exibe uma tabela com busca por música ou artista e permite baixar os dados filtrados em CSV.

Na barra lateral, é possível filtrar as músicas por popularidade mínima, ano de lançamento e gênero.

## Tratamento dos dados (ETL)

Antes de montar o dashboard, o programa prepara o arquivo CSV original:

1. **Extração:** lê o arquivo `high_popularity_spotify_data.csv` usando pandas.
2. **Transformação:** renomeia as colunas, remove linhas duplicadas, mantém um registro por faixa, remove registros sem informações necessárias, extrai o ano de lançamento e converte a duração de milissegundos para minutos.
3. **Carregamento:** salva os dados tratados no arquivo `spotify_tratado.csv`.

## Estrutura dos arquivos

```text
projeto_spotify/
├── app.py
├── style.css
├── high_popularity_spotify_data.csv
├── spotify_tratado.csv
├── requirements.txt
└── .streamlit/
    └── config.toml
```

- `app.py`: código do dashboard e do tratamento dos dados.
- `style.css`: estilos da página.
- `high_popularity_spotify_data.csv`: arquivo original.
- `spotify_tratado.csv`: arquivo gerado com os dados tratados.
- `requirements.txt`: bibliotecas necessárias para executar o projeto.
- `.streamlit/config.toml`: configurações do tema do Streamlit.

## Como executar

É necessário ter o Python instalado. Abra o terminal na pasta do projeto e instale as bibliotecas:

```bash
pip install -r requirements.txt
```

Depois, inicie o dashboard com o comando:

```bash
streamlit run app.py
```

O Streamlit vai mostrar um endereço local no terminal. Abra esse endereço no navegador para acessar o dashboard.
