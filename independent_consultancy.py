import streamlit as st

from data_base import load_indepedent_consultancy_data
from utils import  aplicar_filtros, load_css, navigation_menu
# from menu import show_header, show_sidebar
from data_base import load_image

def indepedent_consultancy():
    # show_sidebar()
    imagens = load_image()
    url_bannerhead = imagens["url_bannerhead"]
    # show_header(url_bannerhead)

    load_css("style.css")

    st.header("Assessorias Técnicas")

    data = load_indepedent_consultancy_data()

    orsa = data['orsa_proc']
    citacoes = data['citacoes_proc']


    st.write("""
    <div style="text-align: justify">
        Aqui você encontra  publicações realizadas por essas entidades no ambiente virtual, organizadas por temas. Também é possível acessar um <strong>resumo das publicações por bloco temático</strong>, com suas respectivas citações. Esse painel permite, ainda, a <strong>visualização gráfica das coocorrências entre temáticas</strong>. O carregamento inicial desta seção contempla publicações a partir de janeiro de 2025.
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

    st.subheader("🔍 Resumo do Conteúdo Publicado, por Tema")
    for categoria, grupo in orsa.groupby('Categoria'):
        with st.expander(f"{categoria}"):
            st.markdown(f"<div style='font-size:20px; font-weight:700; margin-bottom:6px'>{categoria}</div>",
                        unsafe_allow_html=True)
            for item in grupo['Conteúdo']:
                st.markdown(f"{item}")

    st.subheader("🎲 Dados gerais")

    citacoes_filtradas = citacoes.copy()


    config = [
        {"column": 'Entidade', "label": 'Entidade', "default": 'Total', "help": "Escolha uma Entidade"},
        {"column": 'Tema', "label": 'Tema', "default": 'Total', "help": "Escolha um Tema"},
    ]
    df_quotes = aplicar_filtros(
        citacoes_filtradas,
        filtros=config,
        # date_column="Data",
        key_prefix="quotes"
        )

    df_quotes["quotes"] = (
        df_quotes["Tema"]
        .fillna(df_quotes["Entidade"])
    )


    st.markdown(
        """
        <style>
        .centered-container {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    st.dataframe(
        df_quotes[
            ['Documento', 'Entidade', 'Conteúdo de Citação', 'Tema', 'Tema principal']
        ],
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
