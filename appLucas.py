#!/usr/bin/env python
# coding: utf-8

# # MBA Ciência de Dados Unifor Turma 5
# 
# Disciplina: Dashboards em R/Python
# 
# Aluno: Lucas de Castro Pereira
# 
# Matrícula: 2319807

# ## Exercício 2
# 
# Utilize os arquivos do **RECLAME AQUI** e crie um dashboard com algumas caracteristicas. 
# 
# Empresas: 
# - Hapvida
# - Nagem
# - Ibyte
# 
# O painel deve conter tais informações: 
# 
# 1. Série temporal do número de reclamações. 
# 
# 2. Frequência de reclamações por estado. 
# 
# 3. Frequência de cada tipo de **STATUS**
# 
# 4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**) 
# 
# 
# Alguns botões devem ser implementados no painel para operar filtros dinâmicos. Alguns exemplos:: 
# 
# 1. Seletor da empresa para ser analisada. 
# 
# 2. Seletor do estado. 
# 
# 3. Seletor por **STATUS**
# 
# 4. Seletor de tamanho do texto 
# 
# Faça o deploy da aplicação. Dicas: 
# 
# https://www.youtube.com/watch?v=vw0I8i7QJRk&list=PLRFQn2r6xhgcDMhp9NCWMqDYGfeeYsn5m&index=16&t=252s
# 
# https://www.youtube.com/watch?v=HKoOBiAaHGg&t=515s
# 
# Exemplo do github
# https://github.com/jlb-gmail/streamlit_teste
# 
# 
# **OBSERVAÇÃO**
# 
# A resposta do exercicio é o link do github e o link da aplicação. Coloque-os abaixo.  
# 
# 
# 
# 

# ### 0. Upload e Tratamento dos dados 

# In[65]:


# Importar bibliotecas e os datasets

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


#get_ipython().system('pip install pipreqs')
#get_ipython().system('pip install --upgrade pip --user')
#get_ipython().system('pip install --upgrade pip')
#get_ipython().system('pip install aiohttp --user')
#get_ipython().system('pip install aiohttp')


# In[66]:


#Carregar os datasets

df_ibyte=pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_hapvida=pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_nagem=pd.read_csv('RECLAMEAQUI_NAGEM.csv')


# In[67]:


#Exibir informações gerais sobre os datasets

print(df_ibyte.info())
print(df_hapvida.info())
print(df_nagem.info())


# In[68]:


# Concatenar os datasets, depois de verificar que possuem as mesmas colunas

df_ibyte['EMPRESA'] = "Ibyte"
df_hapvida['EMPRESA'] = "Hapvida"
df_nagem['EMPRESA'] = "Nagem"

df = pd.concat([df_ibyte, df_hapvida, df_nagem], ignore_index=True)
df.head()


# In[69]:


#Verificar informações gerais sobre o dataset concatenado

df.info()


# In[70]:


#Contar os valores únicos das colunas do dataset concatenado

df.nunique()


# ### 1. Utilização do Streamlit

# In[71]:


# Carregar a biblioteca streamlit

# pip install streamlit matplotli


# In[72]:


# Adicione a coluna N_CARACTERES
df['N_CARACTERES'] = df['DESCRICAO'].apply(len)

# Título do Dashboard
st.title("Dashboard de Reclamações de Clientes")

# Filtros dinâmicos
empresa_selecionada = st.selectbox("Seletor da Empresa", df['EMPRESA'].unique())
estado_selecionado = st.selectbox("Seletor do Estado", df['LOCAL'].unique())
status_selecionado = st.selectbox("Seletor de STATUS", df['STATUS'].unique())
tamanho_minimo = st.slider("Seletor de Tamanho Mínimo do Texto", min_value=0, max_value=df['N_CARACTERES'].max(), value=0)

# Aplica os filtros dinâmicos
df_filtrado = df[(df['EMPRESA'] == empresa_selecionada) &
                 (df['LOCAL'] == estado_selecionado) &
                 (df['STATUS'] == status_selecionado) &
                 (df['N_CARACTERES'] >= tamanho_minimo)]

# Série temporal do número de reclamações
st.subheader("Série Temporal do Número de Reclamações")
df_temporal = df_filtrado.groupby(['ANO', 'MES']).size().reset_index(name='Número de Reclamações')
fig_temporal, ax_temporal = plt.subplots()
sns.lineplot(data=df_temporal, x='ANO', y='Número de Reclamações', hue='MES', ax=ax_temporal)
st.pyplot(fig_temporal)

# Frequência de reclamações por estado
st.subheader("Frequência de Reclamações por Estado")
df_estado = df_filtrado['LOCAL'].value_counts().reset_index()
df_estado.columns = ['Estado', 'Número de Reclamações']
fig_estado, ax_estado = plt.subplots()
sns.barplot(x='Número de Reclamações', y='Estado', data=df_estado, ax=ax_estado)
st.pyplot(fig_estado)

# Frequência de cada tipo de STATUS
st.subheader("Frequência de Cada Tipo de STATUS")
df_status = df_filtrado['STATUS'].value_counts().reset_index()
df_status.columns = ['Status', 'Número de Reclamações']
fig_status, ax_status = plt.subplots()
sns.barplot(x='Número de Reclamações', y='Status', data=df_status, ax=ax_status)
st.pyplot(fig_status)

# Distribuição do tamanho do texto (coluna DESCRIÇÃO)
st.subheader("Distribuição do Tamanho do Texto (Descrição)")
fig_tamanho_descricao, ax_tamanho_descricao = plt.subplots()
sns.histplot(df_filtrado['N_CARACTERES'], bins=30, kde=True, color='purple', ax=ax_tamanho_descricao)
st.pyplot(fig_tamanho_descricao)


# In[73]:


#pipreqs . --force


# In[ ]:




