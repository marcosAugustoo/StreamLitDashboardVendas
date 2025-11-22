import streamlit as st
import pandas as pd
from dataset import df
from utils import converte_csv, msg_sucesso

st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as colunas',
        list(df.columns),
        list(df.columns)
    )

st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()
    )

with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o preço do produto',
        0, 5000,
        (0, 5000)
    )

with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a data da compra',
        (
            df['Data da Compra'].min(),
            df['Data da Compra'].max()
        )
    )

# garantir tupla
if not isinstance(data_compra, (list, tuple)):
    data_compra = (data_compra, data_compra)

data_inicio = pd.to_datetime(data_compra[0])
data_fim = pd.to_datetime(data_compra[1])

query = '''
    `Categoria do Produto` in @categorias and \
    @preco[0] <= Preço <= @preco[1] and \
    @data_inicio <= `Data da Compra` <= @data_fim
'''

filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]
st.dataframe(filtro_dados)

nome_arquivo = st.text_input(
    'Nome do arquivo (sem .csv)',
    placeholder='ex: vendas_filtradas'
)

file_name = f"{nome_arquivo.strip()}.csv" if nome_arquivo.strip() else "arquivo.csv"

st.download_button(
    label='Baixar CSV',
    data=converte_csv(filtro_dados),
    file_name=file_name,
    mime='text/csv',
    on_click=msg_sucesso
)