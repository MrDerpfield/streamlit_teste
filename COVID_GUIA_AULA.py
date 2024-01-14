import streamlit as st
import pandas as pd 
import plotly.express as px

##### DADOS  ####
casos=pd.read_csv('SERIES_CASOS_BAIRRO.csv',sep=';')
casos['DATA']=pd.to_datetime(casos['DATA'])
casos['FORTALEZA']=casos.drop('DATA',axis=1).sum(axis=1)

mortes=pd.read_csv('SERIES_OBITOS_BAIRRO.csv',sep=';')
mortes['DATA']=pd.to_datetime(mortes['DATA'])
mortes['FORTALEZA']=mortes.drop('DATA',axis=1).sum(axis=1)


ibge=pd.read_csv('IBGE_BAIRRO.csv',sep=';')

lista_localidade=list(ibge['NM_BAIRRO'].unique())
lista_localidade=['FORTALEZA']+lista_localidade

st.title('COVID DASHBOARD')
localidade = st.selectbox(
    'SELECIONE A LOCALIDADE',
    lista_localidade)

col1, col2=st.columns(2)

with col1:
        st.metric(label='CASOS', value=casos[localidade].sum())
with col2:       
        st.metric(label='MORTES',value=mortes[localidade].sum())
        
st.markdown('---')

if localidade !='FORTALEZA':
    POP=ibge[ibge['NM_BAIRRO']==localidade]['POP'].values[0]
    INC=ibge[ibge['NM_BAIRRO']==localidade]['INC'].values[0]
    ARE=ibge[ibge['NM_BAIRRO']==localidade]['ARE'].values[0]
    
if localidade =='FORTALEZA':
    POP=ibge['POP'].sum()
    INC=ibge['INC'].sum()
    ARE=ibge['ARE'].sum()

col1, col2,col3=st.columns(3)
with col1:
        st.metric(label='POPULAÇÃO', value=POP)
with col2:
        st.metric(label='RENDA', value=INC)
with col3:
        st.metric(label='AREA', value=ARE)

st.title('CASOS DIÁRIOS')
figcasos=px.bar(casos, x="DATA", y=localidade)
figcasos.update_traces(marker_color = 'blue')
st.plotly_chart(figcasos)

st.title('MORTES DIÁRIAS')
figmortes=px.bar(mortes, x="DATA", y=localidade)
figmortes.update_traces(marker_color = 'red')
st.plotly_chart(figmortes)





