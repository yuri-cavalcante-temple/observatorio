import streamlit as st
import pandas as pd
import plotly.express as px

from data_base import load_territorial_intelligence_data
from utils import aplicar_filtros, load_css, navigation_menu
import menu
from data_base import load_image

def territorial_intelligence():
    
    data = load_territorial_intelligence_data()
    df_unificado_geral     = data["df_unificado_geral"]
    df_unificado_prsa     = data["df_unificado_prsa"]

    load_css("territorial_intelligence.css")
    st.markdown(f"""
                <div class="section-green-map">
                """, unsafe_allow_html=True)
    with st.container(height=870, border=False, ):
        col1, col2 = st.columns(2)
        with col1: 
           st.header("Inteligência Territorial")
           st.write("Reúne informações da Central de Atendimento e da base de registros dos Analistas de Relacionamento com a Comunidade, permitindo visualizar as principais pautas e demandas da população, entre outras informações.")
           st.subheader("Filtros")
           on = st.toggle("**Dados do PRSA**", help='Exibe somente dados do PRSA')
           if on:
            df_unificado = df_unificado_prsa
           else:
            df_unificado = df_unificado_geral


           df_temp = df_unificado.copy()
           df_temp['Tipo'] = df_temp['Demanda'].fillna(df_temp['MicroCategoria'])

           config = [
            {"column": "Fonte", "label": "Fonte", "default": "Total", "help": "Escolha a Fonte de Dados"},
            {"column": "Município", "label": "Município", "default": "Total", "help": "Escolha um Município"},
            {"column": "Bairro", "label": "Bairro", "default": "Total", "help": "Escolha um Bairro"},
            {"column": "Tipo", "label": "Categoria Temática", "default": "Total", "help": "Escolha uma Categoria Temática"},
            ]
           
           df_territorial = aplicar_filtros(
                df_temp,
                filtros=config,
                date_column="Data",
                key_prefix="clipping"
            )

        with col2:
             contagens = (
             df_territorial['Tipo']
                .value_counts(normalize=True)    # fração somando 1.0
                .mul(100)                        # converte pra %
                .round(1)                        # arredonda
                .rename_axis('Tipo')            # põe o nome do índice
                .reset_index(name='Porcentagem') # transforma em DF e nomeia a coluna de valores
            )

            # 2. Cria o treemap usando path ao invés de names
             fig = px.treemap(
                contagens,
                path=['Tipo'],    # usa a coluna ‘Tipo’ como hierarquia
                values='Porcentagem',   # usa exatamente o nome da coluna de valores,
                custom_data=['Porcentagem']
            )

            # 3. Ajustes de layout para forçar exibição
             fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
            title=None, width=800, height=700 )
             fig.update_traces(
                texttemplate='<b>%{label}</b><br>%{value}%',  # ou use '%{percentEntry:.1%}' se quiser proporção
                textinfo='none',    # usar texttemplate em vez de textinfo
                textfont=dict(size=14),
                hovertemplate='<b>%{label}</b><br>Representa <b>%{customdata[0]}%</b> do total<extra></extra>'
            )
             st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""
                </div>
                """, unsafe_allow_html=True)

    st.subheader("📊 Registros Mensais", help='Distribuição ao longo do tempo dos registros')
    if not df_territorial.empty:
        df_diario = (
            df_territorial
            .groupby(['Data', 'Fonte'])
            .size()
            .reset_index(name='Contagem')
        )

        color_map = {
            'Central 0800': '#007E7A',
            'Registro De Relacionamento': '#EDB111',
        }

        fig = px.line(
            df_diario, x="Data", y="Contagem", color="Fonte", markers=True,
        color_discrete_map=color_map,
            title=""
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(legend_title_text='Fonte')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.line(title="")
        st.plotly_chart(fig, use_container_width=True)

    
    with st.expander( "**Saiba mais:** Pico de demandas em agosto e setembro de 2024"):
        st.write('''
                No período de 10/08/2024 a 01/10/2024, o SRD (Central 0800) registrou um total de 1.300 chamados.
                Esse volume, considerado atípico para o período, foi influenciado principalmente pela atuação de um stakeholder específico — um escritório de advocacia — responsável por 455 solicitações.
                As demandas desse stakeholder foram distribuídas da seguinte forma: 392 relacionadas à "Qualidade da água do rio Paraopeba e seus usos", 38 sobre "Serviço de saúde mental e perícia" e 25 referentes ao "Levantamento de desvalorização imobiliária".
        ''')

    st.subheader("🔢 Contagem por categoria", help='Selecione o filtro')
    colunas_disponiveis = ['Município', 'Bairro', 'Demanda', 'MicroCategoria', 'Fonte']
    coluna = st.selectbox(
        "Coluna para agrupar",
        [c for c in colunas_disponiveis if c in df_territorial.columns]
    )

    if not df_unificado.empty and coluna in df_unificado.columns:
        agrupado = df_unificado[coluna].value_counts().reset_index()
        agrupado.columns = [coluna, 'Contagem']
        st.dataframe(agrupado.style.set_properties(subset=['Contagem'], **{'text-align': 'right'}), hide_index=True)
    else:
        agrupado_vazio = pd.DataFrame(columns=[coluna, 'Contagem'])
        st.dataframe(agrupado_vazio)
    
    menu.footer()
