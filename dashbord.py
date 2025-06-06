import streamlit as st
import pandas as pd
import plotly.express as px

#--------------------------
# Funções
#--------------------------

def formatNumero(valor):
    if valor >= 1_000_000_000:
        return f'{valor / 1_000_000_000:.2f} G'
    if valor >= 1_000_000:
        return f'{valor / 1_000_000:.2f} M'
    if valor >= 1_000:
        return f'{valor / 1_000:.2f} k'
    return str(valor)

def tratarDados(df, parameter, max=True):
    if max:
        idx = df.index[df['Emissão'] == df['Emissão'].max()]
    else:
        idx = df.index[df['Emissão'] == df['Emissão'].min()]
    key = df.iloc[idx[0]][parameter]
    value = df.iloc[idx[0]]['Emissão']
    return key, value

#--------------------------
# Dados
#--------------------------

dados = pd.read_csv('emissoes.csv')

#--------------------------
# Tabelas
#--------------------------

#Estados
emissoes_estados = dados.groupby('Estado')[["Emissão"]].sum().reset_index()
emissoes_estados = dados.drop_duplicates(subset='Estado')[['Estado', 'lat', 'long']].merge(emissoes_estados, on='Estado').reset_index()
emissoes_estados.drop('index', axis=1, inplace=True)

#Setores
emissoes_setores = dados.groupby('Setor de emissão')[['Emissão']].sum().reset_index()

#Anos

emissoes_anos = dados.groupby('Ano')[["Emissão"]].sum().sort_values(by='Ano').reset_index()

#Gás

emissoes_gas = dados.groupby('Gás')[['Emissão']].sum().sort_values(by='Emissão').reset_index()

#--------------------------
# Grafico
#--------------------------

#Estados

fig_mapa_emissoes = px.scatter_geo(emissoes_estados, 
                                   lat='lat', 
                                   lon='long', 
                                   scope='south america', 
                                   size='Emissão', 
                                   hover_name='Estado', 
                                   hover_data={'lat':False, 'long':False},
                                   color='Estado',
                                   text='Estado',
                                   title='Total de Emissões por Estado')

#Setores

fig_emissoes_setores = px.bar(emissoes_setores, 
                              x='Emissão', 
                              y='Setor de emissão', 
                              color='Setor de emissão', 
                              text_auto=True, 
                              title="Total de Emissões por Setores")
fig_emissoes_setores.update_layout(yaxis_title='', showlegend=False)

#Anos

fig_emissoes_anos = px.line(emissoes_anos, 
                            x='Ano', 
                            y='Emissão', 
                            title="Total de Emissões por Ano")

#--------------------------
# Dashboard
#--------------------------

st.set_page_config(layout="wide")

st.title("Emissões de Gases de Efeito Estufa")

tab_home, tab_gas = st.tabs(["Home", "Gás"])

with tab_home:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de emissões", formatNumero(dados['Emissão'].sum()) + 'Ton')
        st.plotly_chart(fig_mapa_emissoes)

    with col2:
        #idx_maior_emissao = emissoes_anos.index[emissoes_anos['Emissão'] == emissoes_anos['Emissão'].max()]
        #ano_mais_poluente = emissoes_anos.iloc[idx_maior_emissao[0]]['Ano']
        #emissao_mais_poluente = emissoes_anos.iloc[idx_maior_emissao[0]]['Emissão']
        ano_mais_poluente, emissao_mais_poluente = tratarDados(emissoes_anos, 'Ano')
        st.metric(f"Ano Mais Poluente: {ano_mais_poluente}", formatNumero(emissao_mais_poluente) + 'Ton')
        st.plotly_chart(fig_emissoes_setores)

    st.plotly_chart(fig_emissoes_anos)

with tab_gas:
    col1, col2 = st.columns(2)

    with col1:
        #Gás com mais emissões
        #idx_gas_mais_emissoes = emissoes_gas.index[emissoes_gas['Emissão'] == emissoes_gas['Emissão'].max()]
        #gas_mais_emissoes = emissoes_gas.iloc[idx_gas_mais_emissoes[0]]['Gás']
        #emissao_gas_max = emissoes_gas.iloc[idx_gas_mais_emissoes[0]]['Emissão']
        gas_mais_emissoes, emissao_gas_max = tratarDados(emissoes_gas, 'Gás')
        st.metric(f"Gás com mais emissões: {gas_mais_emissoes}", formatNumero(emissao_gas_max) + 'Ton')

    with col2:
        #Gás com menos emissões
        #idx_gas_menos_emissoes = emissoes_gas.index[emissoes_gas['Emissão'] == emissoes_gas['Emissão'].min()]
        #gas_menos_emissoes = emissoes_gas.iloc[idx_gas_menos_emissoes[0]]['Gás']
        #emissao_gas_min = emissoes_gas.iloc[idx_gas_menos_emissoes[0]]['Emissão']
        gas_menos_emissoes, emissao_gas_min = tratarDados(emissoes_gas, 'Gás', False)
        st.metric(f"Gás com menos emissões: {gas_menos_emissoes}", formatNumero(emissao_gas_min))
