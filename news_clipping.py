import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

from data_base import load_clipping_data
from utils import aplicar_filtros, load_css, navigation_menu
# from menu import show_header, show_sidebar, header_menu
from data_base import load_image, load_clipping_data

def news_clipping():
    # show_sidebar()
    imagens = load_image()
    url_bannerhead = imagens["url_bannerhead"]
    # show_header(url_bannerhead)

    load_css("style.css")

    st.header("Monitoramento de Notícias")
    st.write("""
    <div style="text-align: justify">
        Aqui você encontra o <strong>monitoramento das matérias publicadas na web</strong> sobre a reparação, além de outras notícias que possam impactar a comunicação do PRSA (Plano de Reparação Socioambiental), desde janeiro de 2024.
        Dois <strong>gráficos de frequência</strong> permitem visualizar a quantidade de notícias ao longo do tempo. O gráfico inferior detalha as informações do período selecionado ao mover o cursor sobre o gráfico superior, permitindo também a visualização do total acumulado por tema ou por entidade. É possível aplicar <strong>filtros por tema</strong> ou por <strong>entidade responsável pela publicação</strong>, facilitando a análise do volume e do foco das notícias monitoradas.
        A tabela <strong>“Notícias Monitoradas”</strong> exibe os títulos das matérias, a entidade responsável, os veículos de comunicação utilizados para a divulgação e os respectivos links de acesso. É possível filtrar as informações por entidade, data e tema. Por fim, a <strong>nuvem de palavras</strong> oferece um acesso mais visual às informações reunidas nesta seção.
        <br><br>
    </div>
      """, unsafe_allow_html=True)

    paginas_disponiveis = [
        "Início",
        "Inteligência Territorial",
        "Monitoramento de Notícias",
        "Assessorias Técnicas"
    ]
    navigation_menu(paginas_disponiveis, key_prefix="main_menu_")

    clip = load_clipping_data()
    clip_filtrado = clip.copy()
    clip_card = clip_filtrado.copy()

    clip_card["Data"] = pd.to_datetime(clip_card["Data"], errors='coerce')

    clip_card["Ano"] = clip_card["Data"].dt.year
    clip_card["Trimestre"] = clip_card["Data"].dt.quarter
    clip_card["Trimestre_Label"] = clip_card["Ano"].astype(str) + " - " + clip_card["Trimestre"].astype(str) + "º Trimestre"

    clip_card["Trimestre_Ord"] = clip_card["Ano"] * 10 + clip_card["Trimestre"]

    trimestres_unicos = clip_card[["Trimestre_Label", "Trimestre_Ord"]].drop_duplicates()
    trimestres_ordenados = trimestres_unicos.sort_values("Trimestre_Ord", ascending=False)["Trimestre_Label"].tolist()
    trimestres_ordenados_com_total = ["Total"] + trimestres_ordenados


    entidades = sorted(clip_card["Entidade"].unique().tolist())

    st.subheader('Principais Categoria Menciondas pelas Entidades Trimestralmente')
    entidade_escolhida = st.radio(
        "Selecione a fonte 👇",
        options=entidades,
        key="fonte_radio",
        horizontal=True,
        help='Escolha uma Entidade',
    )

    trimestre_escolhido = st.selectbox("Selecione o trimestre:", trimestres_ordenados_com_total)

    if trimestre_escolhido == "Total":
        df_filtrado_final = clip_card[clip_card["Entidade"] == entidade_escolhida]
    else:
        df_filtrado_final = clip_card[
            (clip_card["Entidade"] == entidade_escolhida) &
            (clip_card["Trimestre_Label"] == trimestre_escolhido)
        ]




    categorias_relacionadas = sorted(df_filtrado_final["Tema Principal"].unique(), reverse=True)

    # st.write(f"Categorias associadas à entidade **{entidade_escolhida}** em **{trimestre_escolhido}**:")
    # if categorias_relacionadas:
    #     col_esq, col_centro, col_dir = st.columns([1, 2, 1])    
    #     with col_centro:
    #         st.markdown(
    #             f"""
    #             <div style='
    #                 background-color: #EDB111;
    #                 color: #007E7A;
    #                 padding: 10px;
    #                 border-radius: 10px;
    #                 box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    #                 text-align: center;
    #                 font-size: 20px;
    #                 font-weight: 500;
    #             '>
    #                 <span style="font-size: 25px;">📋 <strong>Categorias</strong> da entidade <em>{entidade_escolhida}</em><br>
    #                 no trimestre <em>{trimestre_escolhido}</em>:</span><br><br>
    #                 {"<br>".join(f"◦ {cat}" for cat in categorias_relacionadas) if categorias_relacionadas else "<i>Nenhuma categoria encontrada.</i>"}
    #             </div>
    #             """,
    #             unsafe_allow_html=True
    #         )
    # else:
    #     st.warning("Nenhuma categoria encontrada para os filtros selecionados.")


    st.write('')
    st.subheader("📊 Frequência das Publicações")
    config = [
        {"column": "Tema Principal", "label": "Tema Principal", "default": "Total", "help": "Escolha um Tema Principal"},
        {"column": "Entidade", "label": "Entidade", "default": "Total", "help": "Escolha uma Entidade"},
    ]

    df_filtrado = aplicar_filtros(
        clip_filtrado,
        filtros=config,
        date_column="Data",
        key_prefix="clipping"
    )

    df_filtrado["Categoria"] = (
        df_filtrado["Tema Principal"]
        .fillna(df_filtrado["Entidade"])
    )
    categoria = "Categoria"

    df_diario = (
        df_filtrado
        .groupby(['Data', categoria])
        .size()
        .reset_index(name='Contagem')
    )

    # df_diario['Data'] = pd.to_datetime(df_diario['Data'])
    # # df_diario = df_diario.drop_duplicates(subset=['Data', categoria])
    vale_colors = ["#007E7A", "#EDB111", "#919191", "#66C2A5", "#F6EEC7", "#B3B3B3"] #TODO:trabalhar com a paleta de cores
    unique_cats = df_diario[categoria].unique().tolist()
    color_scale = alt.Scale(
        domain=unique_cats,
        range=(vale_colors * (len(unique_cats) // len(vale_colors) + 1))[:len(unique_cats)]
    )

    color = alt.Color(f'{categoria}:N', scale=color_scale, legend=alt.Legend(title=categoria))

    brush = alt.selection_interval(encodings=['x', 'y'])
    click = alt.selection_point(
        fields=[categoria],
        bind="legend",
        empty="all"
    )

    # 1) Pega domínio bruto de contagens únicas
    counts = sorted(df_diario['Contagem'].unique())

    # 2) Seleciona até 5 valores equidistantes (ou todos, se <5)
    if len(counts) > 5:
        # índices igualmente espaçados entre 0 e len(counts)-1
        idxs = np.linspace(0, len(counts)-1, 5).round().astype(int)
        tick_vals = [counts[i] for i in idxs]
    else:
        tick_vals = counts

    # 3) Usa legend.values em vez de só tickCount
    size = alt.Size(
        'Contagem:Q',
        scale=alt.Scale(range=[10, 200]),
        legend=alt.Legend(
            title='Contagem',
            values=tick_vals,    # pega só esses
            format='.0f'
        )
    )

    points = (
        alt.Chart(df_diario)
        .mark_circle()
        .encode(
            x=alt.X('Data:T', title='Data', axis=alt.Axis(format='%m/%y', labelAngle=0)),
            y=alt.Y('Contagem:Q', title='Contagem Mensal', axis=alt.Axis(format='d')),
            color=alt.condition(brush, color, alt.value('lightgray')),
            size=size,
            tooltip=[
                alt.Tooltip('Data:T'),
                # alt.Tooltip('Contagem:Q', title='Contagem', format='.0f'),
                alt.Tooltip('Contagem:Q', title='Contagem'),
                alt.Tooltip(f'{categoria}:N')
            ]
        )
        .add_params(brush, click)
        .transform_filter(click)
        .properties(width=700, height=300)
    )

    n_categorias = len(df_diario[categoria].unique())
    altura_barras = max(150, n_categorias * 16)

    bars = (
        alt.Chart(df_diario)
        .mark_bar()
        .encode(
            y=alt.Y(
                f'{categoria}:N',
                title=categoria,
                axis=alt.Axis(labelLimit=200, tickMinStep=1, labelFlush=False)
            ),
            x=alt.X('sum(Contagem):Q',
                    title='Total de Registros',
                    axis=alt.Axis(format='d')),
            color=alt.condition(click, color, alt.value('lightgray')),
            tooltip=[
                alt.Tooltip(f'{categoria}:N'),
                alt.Tooltip('sum(Contagem):Q', title='Total')
            ]
        )
        .transform_filter(brush)
        .add_params(click)
        .properties(width=700, height=altura_barras)
    )

    chart = alt.vconcat(points, bars)

    col1, col2, col3 = st.columns([1,50,1])
    with col2:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        # st.altair_chart(points, use_container_width=True)

    temas_contagem = (
        clip_filtrado
        .dropna(subset=["Tema Principal"])
        # .drop_duplicates(subset=["Data", "Tema Principal"])
        .groupby("Tema Principal")
        .size()
        .reset_index(name="Contagem")
    )
    entidades_contagem = (
        clip_filtrado
        .dropna(subset=["Entidade"])
        # .drop_duplicates(subset=["Data", "Entidade"])
        .groupby("Entidade")
        .size()
        .reset_index(name="Contagem")
    )

    chart_tema = (
        alt.Chart(temas_contagem)
        .mark_bar(color='#007E7A')
        .encode(
            x=alt.X('Tema Principal:N', title='Tema Principal', sort='-y', axis=alt.Axis(labelAngle=25)),
            y=alt.Y('Contagem:Q', title='Quantidade'),
            tooltip=['Tema Principal:N', 'Contagem:Q']
        )
        .properties(
            title="Distribuição por Tema Principal",
            width=700,
            height=400
        )
    )

    chart_entidade = (
        alt.Chart(entidades_contagem)
        .mark_bar(color='#EDB111')
        .encode(
            x=alt.X('Entidade:N', title='Entidade', sort='-y', axis=alt.Axis(labelAngle=25)),
            y=alt.Y('Contagem:Q', title='Quantidade'),
            tooltip=['Entidade:N', 'Contagem:Q']
        )
        .properties(
            title="Distribuição por Entidades",
            width=700,
            height=400
        )
    )

    with st.expander( "**Saiba mais:** Gráficos de Frequência das Publicações"):
        st.write('''
                O **gráfico de pontos** acima mostra a concentração de publicações, por tema, durante cada dia ao longo do tempo.
                O **gráfico de barras** acompanha o gráfico de pontos tanto com a seleção manual, ou com a aplicação dos filtros.
                Neste, se vê de forma mais detalhada a distribuição das categorias para o período selecionado.
        ''')

    tab1, tab2 = st.tabs(["📊 Por Tema", "📊 Por Entidade"])
    with tab1:
        st.altair_chart(chart_tema, theme=None, use_container_width=True)
    with tab2:
        st.altair_chart(chart_entidade, theme=None, use_container_width=True)


    st.header("🧾 Notícias Monitoradas")
    config = [
        {"column": 'Entidade', "label": 'Entidade', "default": 'Total', "help": "Escola uma Entidade"},
        {"column": 'Categoria do Veículo', "label": 'Categoria do Veículo', "default": 'Total', "help": "Escola uma Categoria de Veículo"},
        {"column": 'Bloco Temático', "label": 'Bloco Temático', "default": 'Total', "help": "Escola um Bloco Temático"},
        {"column": 'Tema Principal', "label": 'Tema Principal', "default": 'Total', "help": "Escola um Tema Principal"},
    ]
    df_monitoramento = aplicar_filtros(
        clip_filtrado,
        filtros=config,
        date_column="Data",
        key_prefix="clipping_monitoring"
        )

    cols = [f["column"] for f in config]

    df_monitoramento["Monitoramento"] = (
        df_monitoramento[cols]
        .bfill(axis=1)
        .iloc[:, 0]
    )


    st.data_editor(
        df_monitoramento[['Data', 'Título', 'Entidade', 'Categoria do Veículo', 'Bloco Temático', 'Tema Principal', 'URL']].drop_duplicates(),
        column_config={
            "Data": st.column_config.DateColumn("Data"),
            "Título": st.column_config.TextColumn("Título", width="large"),
            "Entidade": st.column_config.TextColumn("Entidade"),
            "Categoria do Veículo": st.column_config.TextColumn("Categoria do Veículo"),
            "Bloco Temático": st.column_config.TextColumn("Bloco Temático"),
            "Tema Principal": st.column_config.TextColumn("Tema Principal"),
            "URL": st.column_config.LinkColumn("Link", display_text="Acessar")
            },
        hide_index=True,
        use_container_width=True
        )

    st.title('📊 Nuvem de Palavras')

    def criar_colormap():
        colors = ['#007E7A', '#EDB111', '#919191']
        return LinearSegmentedColormap.from_list("paleta_personalizada", colors)

    stopwords = set([
        'a', 'as', 'na', 'das', 'à', 'às', 'além', 'e', 'é', 'em', 'o', 'os', 'no',
        'dos', 'de', 'da', 'do', 'por', 'para', 'pelo', 'para', 'que', 'se', 'são',
        'um', 'uma', 'uns', 'umas', 'com', 'sem', 'sob', 'sobre', 'entre', 'até'
    ])

    coluna_selecionada = st.selectbox(
    'Selecione a coluna para análise:',
    ['Título', 'Tema Principal']
    )

    df_clound = clip.copy()

    def limpar_texto(texto):
      texto = texto.lower()
      texto = re.sub(r'[^\w\s]', '', texto)
      palavras = texto.split()
      return [p for p in palavras if p not in stopwords and len(p) > 2]

    def processar_texto(textos):
        textos = textos.dropna().astype(str)
        texto = ' '.join(textos)
        return limpar_texto(texto)

    palavras_lista = processar_texto(df_clound[coluna_selecionada])
    palavras_unicas = list(set(palavras_lista))
    texto_para_nuvem = ' '.join(palavras_unicas)

    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='#ffffff',
            max_words=100,
            colormap=criar_colormap(),
            stopwords=stopwords,
            prefer_horizontal=0.9,
            contour_width=1,
            contour_color='#007E7A'
        ).generate(texto_para_nuvem)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background-color:{'#007E7A'}; color:white; padding:6px; border-radius:5px;'>
            <h5 style='margin:0;'>Total de palavras analisadas</h5>
            <h3 style='margin:0;'>{len(palavras_lista)}</h3>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background-color:{'#EDB111'}; color:{"#000000"}; padding:6px; border-radius:5px;'>
            <h5 style='margin:0;'>Palavras únicas</h5>
            <h3 style='margin:0;'>{len(palavras_unicas)}</h3>
            </div>
            """, unsafe_allow_html=True)


        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        for spine in ax.spines.values():
            spine.set_edgecolor('#007E7A')
            spine.set_linewidth(2)
        st.pyplot(fig)

    except ValueError as e:
        st.error("Não há dados suficientes para gerar a nuvem de palavras.")
        st.error(str(e))
        
        st.markdown(f"""
            <div style='margin-bottom: 50px'>
            </div>
            """, unsafe_allow_html=True)
