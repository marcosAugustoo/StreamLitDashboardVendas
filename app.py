import streamlit as st
from dataset import df
from graficos import grafico_map_estado, grafico_receita_mensal, grafico_receita_estado, grafico_receita_categoria, grafico_receita_vendedores, grafico_vendas_dos_vendedores
from utils import format_number

st.title('Dashboard de Vendas 🛒')
st.set_page_config(layout='wide')
st.sidebar.title('Filtro Vendedores')
filtro_vendedor = st.sidebar.multiselect(
    'Vendedores',
    df['Vendedor'].unique(),
)

if filtro_vendedor:
    df = df[df['Vendedor'].isin(filtro_vendedor)]

aba1, aba2, aba3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])

with aba1:
    st.dataframe(df)
with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita Total', format_number(df['Preço'].sum(), 'R$'))
        st.plotly_chart(grafico_map_estado, width='stretch')
        st.plotly_chart(grafico_receita_estado, width='stretch')
    with coluna2:
        st.metric('Quantidade de Vendas', format_number(df.shape[0]))
        st.plotly_chart(grafico_receita_mensal, width='stretch')
        st.plotly_chart(grafico_receita_categoria, width='stretch')
with aba3:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(grafico_receita_vendedores) # width='stretch'
    with coluna2:
        st.plotly_chart(grafico_vendas_dos_vendedores)

