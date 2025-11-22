from dataset import df
import pandas as pd
import streamlit as st
import time


def format_number(value, prefix=''):
    for unit in ['', 'mil']:
        if value < 1_000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1_000
    return f'{prefix} {value:.2f} {unit} milhões'


# -------------------------------
# Receita por Estado
# -------------------------------

df_receita_estado = df.groupby('Local da compra')[['Preço']].sum()
df_receita_estado = (
    df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']]
      .merge(df_receita_estado, left_on='Local da compra', right_index=True)
      .sort_values('Preço', ascending=False)
)


# -------------------------------
# Receita Mensal
# -------------------------------

# 1. Converter coluna de data
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], dayfirst=True, errors='coerce')

# Verificar conversão
# print("\n--- Verificando datas convertidas ---")
# print(df['Data da Compra'].head())
# print("Tipo:", df['Data da Compra'].dtype)

# Mostrar linhas inválidas, se houver
# linhas_invalidas = df[df['Data da Compra'].isna()]
# if not linhas_invalidas.empty:
#     print("\n⚠ Linhas com data inválida:")
#     print(linhas_invalidas)


# 2. Agrupar por mês (fim do mês usando freq='ME')
df_receita_mensal = (
    df.groupby(pd.Grouper(key='Data da Compra', freq='ME'))['Preço']
      .sum()
      .reset_index()
)

# 3. Criar colunas Ano e Mês
df_receita_mensal['Ano'] = df_receita_mensal['Data da Compra'].dt.year
df_receita_mensal['Mes'] = df_receita_mensal['Data da Compra'].dt.month_name('pt_BR')

# print("\n--- Receita Mensal Gerada ---")
# print(df_receita_mensal.head())
# print(df_receita_mensal.dtypes)


# # 4. Mostrar colunas do df original
# print("\n--- Colunas do DataFrame Original ---")
# print(df.columns)

# 5. Criar DatAFrame de Receita por Categoria
df_receita_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)
# print(df_receita_categoria.head())

# 6. DataFrame Vendedores
df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))
# print(df_vendedores)

# Funcao para converter arquivo .csv
@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# mensagem de sucesso
def msg_sucesso():
    sucesso = st.success(
        'Arquivo baixado com sucesso!',
        icon='✅'
    )
    time.sleep(3)
    sucesso.empty()