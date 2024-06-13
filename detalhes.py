from pathlib import Path 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd 
import time 
import os
import pages as pg
import datetime as dt


def app():

    st.title("Dashboard Ômega Invest")

    caminho_vendas = r"C:\Users\WelberOliveira\CursoRPA\Dashboard\Geral.csv"

    # Quando a aplicação é muito pesada o código renderiza a ultima aplicação fazendo assim que a página apresente o ultimo visual.

    @st.cache_data
    def load_data():
        df = pd.read_csv(caminho_vendas)
        time.sleep(5)
        # Operação Pesada
        return df

    df = load_data()



    #######################################
    # STREAMLIT LAYOUT
    #######################################

    # FILTRO TEMPO

    # Ordenar o DataFrame pelo índice
    df_sorted = df.sort_index(ascending=False)

    coldata,  colcoanta, colcentro, colfundo =  st.columns(4)


    with coldata:
        # Extrair as datas únicas do DataFrame ordenado pelo índice
        datas = ['Todas'] + list(df_sorted["Mês/Ano"].unique())
        data = st.selectbox("Data", datas)
        df_filter = df[df['Mês/Ano']== data]


    # Filtrar o DataFrame pela conta selecionada
    if data == 'Todos':
        df_filter = df_sorted
    else:
        df_filter = df_sorted[df_sorted['Mês/Ano'] == data]
    

    
    with colcoanta:
        clients = ['Todos'] + list(df_filter["Conta"].value_counts().index)
        client = st.selectbox("Conta", clients)
        df_filtered = df_filter[df_filter['Conta']== client]

    # FILTRO CONTA

    

    # Filtrar o DataFrame pela conta selecionada
    if client == 'Todos':
        df_filtered = df_filter
    else:
        df_filtered = df_filter[df_filter['Conta'] == client]


          

    tabela = df_filtered[['Mês/Ano','Conta','Nome','Auc','CAPTAÇÃO','Receita_Bruta_Total','Comissao_Bruta_Fundos','Receita_Bruta_Corban', 'Comissao_Bruta_prev']]

    def formatar_numero(valor):
        try:
            # Converter para float e formatar como moeda brasileira
            valor_formatado = f"{float(valor):,.2f}"  # Usar duas casas decimais
            valor_formatado = valor_formatado.replace(",", "@").replace(".", ",").replace("@", ".")
            return "R$ " + valor_formatado
        except ValueError:
            # Retorna o valor original se a conversão falhar
            return valor

    # Converter as colunas a partir do índice 2 para string
    for col in tabela.columns[3:]:
        tabela[col] = tabela[col].astype(str)

    # Aplicar a função formatar_numero
    for col in tabela.columns[3:]:
        tabela[col] = tabela[col].apply(formatar_numero)


    tabela['Conta'] = tabela['Conta'].astype(str)

    tabela['Conta'] = tabela['Conta'].str.replace('.','')

    # st.line_chart(df_sorted, x="Mês/Ano", y="Receita_bruta_total")
        
    
    tabela_reset_index = tabela.reset_index(drop=True)
      

    display = st.checkbox('Detalhes')

    if display:
        tabela_reset_index.set_index("Mês/Ano", inplace=True)
        # Criar o gráfico de barras usando Plotly Express
        st.dataframe(tabela_reset_index,  use_container_width=True)
        # # Exibir o gráfico no Streamlit
        # st.plotly_chart(fig)


    # st.dataframe(df_filtered2,
    #              column_config={
                
    #              }
    #             )


