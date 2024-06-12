from pathlib import Path 
import streamlit as st
from streamlit_navigation_bar import st_navbar
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd 
import time 
import os
import openpyxl
import datetime as dt



caminho_vendas = r"C:\Users\WelberOliveira\OneDrive - OMEGA INVEST AGENTE AUTONOMO DE INVESTIMENTOS LTDA\MIS - Interno\Projetos Power Bi\Relatórios\Fechamento.xlsx"

df = pd.read_excel(caminho_vendas, sheet_name='Comissões')


df['Data Receita'] = pd.to_datetime(df['Data Receita'])
df['Mês/Ano'] = df['Data Receita'].dt.to_period('M')
df.dropna(subset=['Receita Bruta'])

df['Receita Bruta'] = pd.to_numeric(df['Receita Bruta'], errors='coerce')
df['Comissão'] = pd.to_numeric(df['Comissão'], errors='coerce')
df['Receita Líquida'] = pd.to_numeric(df['Receita Líquida'], errors='coerce')

df = df.dropna(subset=['Receita Bruta'])

relatorio = df.groupby(['Mês/Ano', 'Assessor Principal', 'Conta', 'Cliente', 'Categoria']).agg({'Receita Bruta':'sum','Receita Líquida':'sum','Comissão':'sum'}).reset_index()
 

#######################################
# TEMPO
#######################################

from datetime import datetime
 
mes_atual = datetime.now().strftime('%Y-%m')

#######################################
# DF_DONO
#######################################

df_dono = relatorio[relatorio['Mês/Ano'] == "2024-05"]

#######################################
# BASE
#######################################

Basecaminho = r"C:\Users\WelberOliveira\OneDrive - OMEGA INVEST AGENTE AUTONOMO DE INVESTIMENTOS LTDA\MIS - Interno\Base Atendimentos\Base_OmegaInvest_Ofc.xlsx"

base = pd.read_excel(Basecaminho)

# Remover duplicatas na coluna 'Conta'
base = base.drop_duplicates(subset=['Conta'])

baseRV = base[['Conta', 'Assessor_RV']]

baseRF = base[['Conta', 'Assessor_RF']]

# Retirando os Não Consta
 
baseRV = baseRV[~baseRV['Assessor_RV'].str.contains("Não Consta", na=False)]
baseRV = baseRV[~baseRV['Assessor_RV'].str.contains("SAULO DE SOUZA FREITAS", na=False)]
baseRV = baseRV[~baseRV['Assessor_RV'].str.contains("JONAS VICENTE DA SILVA", na=False)]
baseRV = baseRV[~baseRV['Assessor_RV'].str.contains("WILLIAN MATTOS SATURNINI DE OLIVEIRA", na=False)]
baseRV = baseRV[~baseRV['Assessor_RV'].str.contains("WELBER MATTOS SATURNINI DE OLIVEIRA", na=False)]

# Retirando os Informar
 
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("Informar", na=False)]
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("SAULO DE SOUZA FREITAS", na=False)]
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("JONAS VICENTE DA SILVA", na=False)]
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("WILLIAN MATTOS SATURNINI DE OLIVEIRA", na=False)]
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("WELBER MATTOS SATURNINI DE OLIVEIRA", na=False)]
baseRF = baseRF[~baseRF['Assessor_RF'].str.contains("WELLINGTON DA SILVA COELHO", na=False)]


df_ger = df_dono.copy()

df_ger_rf = df_dono.copy()

#######################################
# FILTRO CATEGORIA RV
#######################################
categorias_filtradas_rv = ['RENDA VARIAVEL','OPERACOES ESTRUTURADAS']
 
df_filtradorv = df_ger[df_ger['Categoria'].isin(categorias_filtradas_rv)]


#######################################
# FILTRO CATEGORIA RF
#######################################
categorias_filtradas_rf = ['RENDA FIXA']
 
df_filtradorf = df_ger_rf[df_ger_rf['Categoria'].isin(categorias_filtradas_rf)]


#######################################
# AGRUPANDO OS DFS
#######################################

df_filtradorv = df_filtradorv.merge(baseRV[['Conta', 'Assessor_RV']], on='Conta', how='left')

df_filtradorf = df_filtradorf.merge(baseRF[['Conta', 'Assessor_RF']], on='Conta', how='left')

df_filtradorv['Assessor_RV'].fillna(df_filtradorv['Assessor Principal'], inplace=True)

df_filtradorf['Assessor_RF'].fillna(df_filtradorf['Assessor Principal'], inplace=True)


condicao = df_filtradorv["Assessor Principal"] != df_filtradorv["Assessor_RV"]
df_diferentes = df_filtradorv[condicao]

condicao2 = df_filtradorv["Assessor Principal"] == df_filtradorv["Assessor_RV"]
df_igual_rv = df_filtradorv[condicao2]


#Filtrar o DataFrame:
 
condicaoRF = df_filtradorf["Assessor Principal"] != df_filtradorf["Assessor_RF"]
df_diferentesRF = df_filtradorf[condicaoRF]


#Filtrar o DataFrame:
 
condicaoRF2 = df_filtradorf["Assessor Principal"] == df_filtradorf["Assessor_RF"]
df_igual_rf = df_filtradorf[condicaoRF2]


df_diferentes_ger = df_diferentes.copy()


df_diferentes_gerRF = df_diferentesRF.copy()



# Substitua 'df_diferentes_ger' pelo nome do seu DataFrame, se necessário

# Lista de nomes para verificar na coluna 'Assessor Principal'
nomes = [
    "DIOGO GOMES RAMOS",
    "GABRIEL PEREIRA LIMA CESAR DE OLIVEIRA",
    "JOAO PAULO ALVES SOARES",
    "KAUE DEL DUQUE DE GODOY",
    "LUCIANA FERREIRA GONCALVES ABADE",
    "ALINE DE OLIVEIRA",
    "RODRIGO MOSSIN PANSICA"
]

# Cria a condição verificando se o valor na coluna 'Assessor Principal' está na lista de nomes
condicao = df_diferentes_ger['Assessor Principal'].isin(nomes)

# Aplica a condição usando np.where e calcula os valores com base na condição
df_diferentes_ger['Nova Receita Bruta'] = np.where(condicao, df_diferentes_ger['Receita Bruta'] * 0.50, df_diferentes_ger['Receita Bruta'] * 0.628571)

df_diferentes_ger['Nova Comissão'] = np.where(condicao, df_diferentes_ger['Comissão'] * 0.50, df_diferentes_ger['Comissão'] * 0.628571)

df_diferentes_ger['Nova Receita Líquida'] = np.where(condicao, df_diferentes_ger['Receita Líquida'] * 0.50, df_diferentes_ger['Receita Líquida'] * 0.628571)


df_diferentes_ger['Receita Bruta'] = df_diferentes_ger['Nova Receita Bruta']

df_diferentes_ger['Comissão'] = df_diferentes_ger['Nova Comissão']

df_diferentes_ger['Receita Líquida'] = df_diferentes_ger['Nova Receita Líquida']



# Substitua 'df_diferentes_ger' pelo nome do seu DataFrame, se necessário

# Lista de nomes para verificar na coluna 'Assessor Principal'
nomes = [
    "DIOGO GOMES RAMOS",
    "GABRIEL PEREIRA LIMA CESAR DE OLIVEIRA",
    "JOAO PAULO ALVES SOARES",
    "KAUE DEL DUQUE DE GODOY",
    "LUCIANA FERREIRA GONCALVES ABADE",
    "ALINE DE OLIVEIRA",
    "RODRIGO MOSSIN PANSICA"
]

# Cria a condição verificando se o valor na coluna 'Assessor Principal' está na lista de nomes
condicao = df_diferentes_gerRF['Assessor Principal'].isin(nomes)

# Aplica a condição usando np.where e calcula os valores com base na condição
df_diferentes_gerRF['Nova Receita Bruta'] = np.where(condicao, df_diferentes_gerRF['Receita Bruta'] * 0.50, df_diferentes_gerRF['Receita Bruta'] * 0.6667)

df_diferentes_gerRF['Nova Receita Líquida'] = np.where(condicao, df_diferentes_gerRF['Receita Líquida'] * 0.50, df_diferentes_gerRF['Receita Líquida'] * 0.6667)

df_diferentes_gerRF['Nova Comissão'] = np.where(condicao, df_diferentes_gerRF['Comissão'] * 0.50, df_diferentes_gerRF['Comissão'] * 0.6667)

df_diferentes_gerRF['Receita Bruta'] = df_diferentes_gerRF['Nova Receita Bruta']

df_diferentes_gerRF['Receita Líquida'] = df_diferentes_gerRF['Nova Receita Líquida']

df_diferentes_gerRF['Comissão'] = df_diferentes_gerRF['Nova Comissão']


df_diferentes31 = df_diferentes.copy()
df_diferentes31RF = df_diferentesRF.copy()



# Lista de nomes para verificar na coluna 'Assessor Principal'
nomes = [
    "DIOGO GOMES RAMOS",
    "GABRIEL PEREIRA LIMA CESAR DE OLIVEIRA",
    "JOAO PAULO ALVES SOARES",
    "KAUE DEL DUQUE DE GODOY",
    "LUCIANA FERREIRA GONCALVES ABADE",
    "ALINE DE OLIVEIRA",
    "RODRIGO MOSSIN PANSICA"
]

# Cria a condição verificando se o valor na coluna 'Assessor Principal' está na lista de nomes
condicao = df_diferentes31['Assessor Principal'].isin(nomes)

# Aplica a condição usando np.where e calcula os valores com base na condição
df_diferentes31['Nova Receita Bruta'] = np.where(condicao, df_diferentes31['Receita Bruta'] * 0.50, df_diferentes31['Receita Bruta'] * 0.371429)

df_diferentes31['Nova Receita Líquida'] = np.where(condicao, df_diferentes31['Receita Líquida'] * 0.50, df_diferentes31['Receita Líquida'] * 0.371429)

df_diferentes31['Nova Comissão'] = np.where(condicao, df_diferentes31['Comissão'] * 0.50, df_diferentes31['Comissão'] * 0.371429)


df_diferentes31['Receita Bruta'] = df_diferentes31['Nova Receita Bruta']

df_diferentes31['Receita Líquida'] = df_diferentes31['Nova Receita Líquida']

df_diferentes31['Comissão'] = df_diferentes31['Nova Comissão']


# Lista de nomes para verificar na coluna 'Assessor Principal'
nomes = [
    "DIOGO GOMES RAMOS",
    "GABRIEL PEREIRA LIMA CESAR DE OLIVEIRA",
    "JOAO PAULO ALVES SOARES",
    "KAUE DEL DUQUE DE GODOY",
    "LUCIANA FERREIRA GONCALVES ABADE",
    "ALINE DE OLIVEIRA",
    "RODRIGO MOSSIN PANSICA"
]

# Cria a condição verificando se o valor na coluna 'Assessor Principal' está na lista de nomes
condicao = df_diferentes31RF['Assessor Principal'].isin(nomes)

# Aplica a condição usando np.where e calcula os valores com base na condição
df_diferentes31RF['Nova Receita Bruta'] = np.where(condicao, df_diferentes31RF['Receita Bruta'] * 0.50, df_diferentes31RF['Receita Bruta'] * 0.3333)

df_diferentes31RF['Nova Receita Líquida'] = np.where(condicao, df_diferentes31RF['Receita Líquida'] * 0.50, df_diferentes31RF['Receita Líquida'] * 0.3333)

df_diferentes31RF['Nova Comissão'] = np.where(condicao, df_diferentes31RF['Comissão'] * 0.50, df_diferentes31RF['Comissão'] * 0.3333)


df_diferentes31RF['Receita Bruta'] = df_diferentes31RF['Nova Receita Bruta']

df_diferentes31RF['Receita Líquida'] = df_diferentes31RF['Nova Receita Líquida']

df_diferentes31RF['Comissão'] = df_diferentes31RF['Nova Comissão']


df_diferentes_ger["Assessor_Oficial"] = df_diferentes_ger["Assessor_RV"]


df_diferentes_gerRF["Assessor_Oficial"] = df_diferentes_gerRF["Assessor_RF"]

df_diferentes31["Assessor_Oficial"] = df_diferentes31["Assessor Principal"]


df_diferentes31RF["Assessor_Oficial"] = df_diferentes31RF["Assessor Principal"]

df_diferentes_final_rv = pd.concat([df_diferentes31, df_diferentes_ger], ignore_index=True)


df_diferentes_final_rF = pd.concat([df_diferentes31RF, df_diferentes_gerRF], ignore_index=True)

df_diferentes_final_rv_ofi = df_diferentes_final_rv.drop(['Assessor_RV'], axis=1)

df_diferentes_final_rf_ofi = df_diferentes_final_rF.drop(['Assessor_RF'], axis=1)

df_igual_rv = df_igual_rv.rename(columns={'Assessor_RV': 'Assessor_Oficial'})

df_igual_rf = df_igual_rf.rename(columns={'Assessor_RF': 'Assessor_Oficial'})


df_dono["Assessor_Oficial"] = df_dono["Assessor Principal"]


# Condição para a duplicação
condicao = (df_dono['Categoria'] == 'RENDA VARIAVEL') | (df_dono['Categoria'] == 'RENDA FIXA') | (df_dono['Categoria'] == 'OPERACOES ESTRUTURADAS')
  
# Filtrar linhas que satisfazem a condição
linhas_condicao = df_dono[condicao]


# Remover linhas originais que satisfazem a condição do DataFrame original
df_dono = df_dono.drop(linhas_condicao.index)

df_final_Oficial = pd.concat([df_dono, df_diferentes_final_rf_ofi,df_diferentes_final_rv_ofi,df_igual_rf,df_igual_rv])

df_final_Oficial = df_final_Oficial.drop(columns=['Nova Receita Bruta', 'Nova Receita Líquida', 'Nova Comissão'])


df_final_Oficial["Receita Bruta"] = df_final_Oficial["Receita Bruta"].round(2)

df_final_Oficial['Categoria'] = df_final_Oficial['Categoria'].dropna()