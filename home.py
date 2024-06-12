from pathlib import Path 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd 
import time 
import os
import pages as pg
import openpyxl
from datetime import datetime
 





st.set_page_config(
        layout = "wide",
        page_title="Dashboard"
    )


def app(username):


    mes_atual = datetime.now().strftime('%Y-%m')

    caminho_vendas = r"C:\Users\WelberOliveira\CursoRPA\Dashboard\Geral.csv"

    # Quando a aplicação é muito pesada o código renderiza a ultima aplicação fazendo assim que a página apresente o ultimo visual.

    @st.cache_data
    def load_data():
        df = pd.read_csv(caminho_vendas)
        time.sleep(5)
        # Operação Pesada
        return df

    df = load_data()


    # Filtrar o DataFrame para exibir apenas os dados do usuário logado
    df = df[df['Email'] == username]



    #######################################
    # VISUALIZATION METHODS
    #######################################

    def plot_metric(label, value, prefix="", suffix="", width=200, height=280):
        fig = go.Figure()

         # Adicionar o indicador
        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font": {"size": 48,
                            "color": "#000000"},
                },
                title={
                    "text": label,
                    "font": {"size": 34,
                            "color": "#2A3054"},
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            )
        )

        fig.update_layout(
            paper_bgcolor = "#F9F9F9",
            width=width,
            height=height
            )
        

        st.plotly_chart(fig, use_container_width=True)

    




    # Função para criar o card com características específicas
    def plot_metric2(label, value,fundos_date,fundos_values,valor_rotulo, prefix="", suffix="", width=200, height=280):
        # Dados de exemplo para a linha de tendência
        trend_data = {
            'dates': fundos_date,
            'values': fundos_values
        }
        df_trend = pd.DataFrame(trend_data)
        
        fig = make_subplots(
                rows=2, cols=1,
                row_heights=[0.8, 0.2],  # Ajustar a proporção de altura entre o indicador e a linha de tendência
                specs=[[{"type": "indicator"}],
                    [{"type": "scatter"}]]
        )   

        # Adicionar o indicador
        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font": {"size": 48,
                            "color": "#000000"},
                },
                title={
                    "text": label,
                    "font": {"size": 34,
                            "color": "#2A3054"},
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=1
        )

        # Adicionar a linha de tendência
        fig.add_trace(
            go.Scatter(
                x=df_trend['dates'],
                y=df_trend['values'],
                mode='lines',
                line=dict(color='rgba(42,48,84,0.2)', width=3),
                fill='tozeroy',
                fillcolor='rgba(42,48,84,0.2)',
                name='Fundos',
                text = valor_rotulo
            ),
            row =2, col=1
        )

        # Atualizar layout
        fig.update_layout(
            paper_bgcolor="#F9F9F9",
            plot_bgcolor="#F9F9F9",
            width=width,
            height=height,
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(color="#FFFFFF"),
            showlegend=False  # Ocultar a legenda
        )

        # Ajustar eixos
        fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=1, col=1)
        fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=1, col=1)
        fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=2, col=1)
        fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)


    


    # Função para criar o gráfico de gauge com subplots
    def plot_gauge(title, subtitle, value, value_percent , meta, current_value, width=300, height=280):
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.2, 0.6],  # Ajustar a proporção de altura entre o título, o valor e o gráfico de gauge
            specs=[[{"type": "indicator"}],
                [{"type": "indicator"}]]
        )

        # Adicionar o valor atual
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=current_value,
                number={'prefix': "R$ ", 'suffix': " M", 'font': {'size': 24}},
                title={'text': f"<span style='font-size:12px;'>Meta: {meta}</span>", 'font': {'size': 12}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=1, col=1
        )

        # Adicionar o gráfico de gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=value,
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "rgba(0,0,0,0)"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, value_percent], 'color': '#C5DFFA'},
                        {'range': [value_percent, 100], 'color': '#4F94F3'}
                    ],
                    'threshold': {
                        'line': {'color': "blue", 'width': 5},
                        'thickness': value_percent/100,
                        'value': 82}
                },
                number={'suffix': "%", 'font': {'size': 24}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=1
        )

        # Atualizar layout
        fig.update_layout(
            margin={'t': 10, 'b': 10, 'l': 10, 'r': 10},
            width=width,
            height=height,
            paper_bgcolor="white",
            font={'color': "blue", 'family': "Arial"}
        )

        st.plotly_chart(fig, use_container_width=True)


    


    #######################################
    # STREAMLIT LAYOUT
    #######################################

    # FILTRO TEMPO

    # Ordenar o DataFrame pelo índice
    df_sorted = df.sort_index(ascending=False)

    Receitageral = df_sorted.groupby(['Mês/Ano'])['Receita_Bruta_Total'].sum().reset_index()

    Fundos = df_sorted.groupby(['Mês/Ano'])['Comissao_Bruta_Fundos'].sum().reset_index()

    coldata,  colcoanta, colcentro, colfundo =  st.columns(4)


    

    with coldata:
        # Extrair as datas únicas do DataFrame ordenado pelo índice
        datas = ['Todas'] + list(df_sorted["Mês/Ano"].unique())

        # Verificar se o mês/ano atual está na lista de datas
        if mes_atual in datas:
            default_index = datas.index(mes_atual)
        else:
            default_index = 0  # 'Todas' será o valor padrão se o mês/ano atual não estiver na lista

        data = st.selectbox("Data", datas, index=default_index)
        
        # Filtrar o DataFrame pela data selecionada
        if data == 'Todas':
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




    #######################################
    #AUC
    #######################################

    # Encontrar o valor máximo de 'Mês/Ano'
    max_mes_ano = df_filtered['Mês/Ano'].max()

    # Filtrar o DataFrame para incluir apenas as linhas onde 'Mês/Ano' é igual ao valor máximo
    df_max_mes_ano = df_filtered[df_filtered['Mês/Ano'] == max_mes_ano]

    # Calcular o total de 'Valor Bruto' para o valor máximo de 'Mês/Ano'
    total_auc = df_max_mes_ano['Auc'].sum().round(2)

   

    #######################################
    #CAPTAÇÃO
    #######################################

    total_mes_cap = df_filtered['CAPTAÇÃO'].sum().round(2)


    #######################################
    #RECEITA TOTAL
    #######################################


    receitabrutaTOTAL = df_filtered['Receita_Bruta_Total'].sum().round(2)


    receitaliqTotal = df_filtered['Receita_Líquida_Total'].sum().round(2)


    ComissaoTotal = df_filtered['Comissão_Total'].sum().round(2)


    #######################################
    #Fundos TOTAL
    #######################################

    # Calcular o total de 'Fundos' '
    Fundostotal = df_filtered['Comissao_Bruta_Fundos'].sum().round(2)

    Fundostotal_df = df_sorted[df_sorted['Mês/Ano'] >= '2023-01']


    #######################################
    #Previdência TOTAL
    #######################################

    # Calcular o total de 'Fundos' '
    Previdenciatotal = df_filtered['Comissao_Bruta_prev'].sum().round(2)


    #######################################
    #Câmbio TOTAL
    #######################################

    # Calcular o total de 'Fundos' '
    PCambiototal = df_filtered['Receita_Bruta_Corban'].sum().round(2)


    column_1, column_2, column_3= st.columns(3)

    with column_1:
        plot_metric(
            "AUC",
            total_auc,
            prefix="R$ ",
            suffix="",
            
        )
        

    with column_2:
        plot_metric(
            "Captação Mensal",
            total_mes_cap,
            prefix="R$ ",
            suffix="",
            
        )
        

    with column_3:
        plot_metric(
            "Receita Bruta Mensal",
            receitabrutaTOTAL,
            prefix="R$ ",
            suffix=""
            
        )


    Receitageral.set_index("Mês/Ano", inplace= True)
   
    # st.line_chart(Receitageral)
  

    column_11, column_22, column_33= st.columns(3)


    # column_11.line_chart(Receitageral)
    
    
    with column_11:
        plot_metric(
            "Fundos",
            Fundostotal,
            prefix="R$ ",
            suffix=""
            )

    
    with column_22:
        plot_gauge(
            title="AuC",
            subtitle="Meta: R$ 868,59 M",
            value=82,
            meta="R$ 643,80 M",
            current_value=643.80,
            value_percent = 82
        )

    

    with column_33:
        plot_metric(
            "Câmbio",
            PCambiototal,
            prefix="R$ ",
            suffix="",
            
        )
        



