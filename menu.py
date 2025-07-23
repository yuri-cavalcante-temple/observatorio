import streamlit as st
import pandas as pd

import base64


from PIL import Image
import base64
from io import BytesIO

def pil_to_base64(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

logo_vale_path = "db/vale_logo.png"
logo_vale_pb_path = "db/vale_pb_amarela.png"
logo_temple_path = "db/temple.png"
logo_vale_img = Image.open(logo_vale_path)
logo_vale_pb_img = Image.open(logo_vale_pb_path)
logo_temple_img = Image.open(logo_temple_path)

logo_vale_base64 = pil_to_base64(logo_vale_img)
logo_vale_pb_base64 = pil_to_base64(logo_vale_pb_img)
logo_temple_base64 = pil_to_base64(logo_temple_img)


def menu():
    """
    Renderiza o cabeçalho (banner + título) que aparecerá no topo de todas as páginas
    uma vez que o usuário esteja logado.
    """
    st.markdown(f"""
        <style>
            /* Remove margens do layout padrão do Streamlit */
            .block-container {{
                padding: 0 !important;
            }}

            /* Remove espaço superior */
            .css-18ni7ap.e8zbici2 {{
                padding-top: 0rem !important;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 30px;
                background-color: #fff;
                border-bottom: 1px solid #dde1e6;
                box-sizing: border-box;
                position: fixed;
                top: 0;
                left: 0;
                margin-bottom: 0;
                box-sizing: border-box;
                width: 100vw;
                z-index: 1000;
            }}

            /* Espaçamento inferior para não sobrepor conteúdo da página */
            .stApp {{
                margin-top: 100px !important;  /* ajustável à altura real do seu header */
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .right-container {{
                display: flex;
                align-items: center;
                gap: 32px;
                color: #21272A;
                font-family: "Vale Sans";
                font-size: 18px;
                font-style: normal;
                font-weight: 500;
                line-height: 100%; /* 16px */
            }}

            .right-container a {{
                text-decoration: none;
                color: #333;
                border-radius: 4px;
            }}

            .right-container a:hover,
            .right-container a:active {{
                color: #007E7A;
                transition: background-color 0.2s ease;
            }}

            .header img {{
                width: 96px;
                height: 100px;
                padding: -1;
                margin: -10px 80px;
                display: block;
            }}
        </style>

        <div class="header">
            <div class="left-container">
                <img src="data:image/png;base64,{logo_vale_base64}" alt="Logo Vale" />
            </div>
            <div class="right-container">
                <a href="/?page=home" target="_self">Home</a>
                <a href="/?page=territorial_intelligence" target="_self">Inteligência Territorial</a>
                <a href="/?page=news_clipping" target="_self">Monitoramento de Notícias</a>
                <a href="/?page=indepedent_consultancy" target="_self">Assessorias Técnicas</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.query_params.get("page", "home")


def footer():
    st.markdown(f"""
        <style>
            .footer-top {{
                padding-top: 1rem;
                box-sizing: border-box;
            }}

            .footer-bottom {{
                border-top: none !important;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .footer-top img {{
                width: 106px;
                height: 40.539px;
                aspect-ratio: 106.00/40.54;
                margin: 20px 80px;
                margin-bottom: 1.8rem;
                display: block;
            }}

            .footer-bottom img {{
                width: 162.872px;
                height: 29.461px;
                aspect-ratio: 106.00/40.54;
                margin: 20px 80px;
                margin-top: 1.8rem;
                margin-bottom: -1rem;
                display: block;
            }}

            .obs {{
                color: #fff;
                font-family: "Vale Sans";
                font-size: 14px;
                font-style: normal;
                margin: 20px 80px;
                margin-top: 1.8rem;
                margin-bottom: -1rem;
                display: block;
            }}

            .footer-columns {{
                border-top: none !important;
                border-bottom: none !important;
                display: flex;
                flex-wrap: wrap;
                column-gap: 20px; /* menor espaço horizontal */
                row-gap: 16px;
            }}

            .footer-column {{
                flex: 0 0 220px;
                word-wrap: break-word;
                padding: 0px 80px 0px 0px;
                margin-bottom: 1.8rem;
            }}

            .footer-column h4{{
                display: flex;
                align-items: center;
                font-size: 15px;
                font-weight: 700;
                line-height: 110%; /* 19.8px */
                margin-bottom: -15px;
                letter-spacing: 0.6px;
            }}

            .footer-column a{{
                display: flex;
                align-items: center;
                padding: 5px 0px;
                color: #fff;
                font-size: 12px;
                font-weight: 500;
                line-height: 1.5;
                letter-spacing: 0.6px;
            }}
        </style>
        <div class="footer-top">
            <div class="vale-logo">
                <img src="data:image/png;base64,{logo_vale_pb_base64}" alt="Logo Vale PB" />
            </div>
            <div style="border-top: 1px solid #ccc; width: 100%; margin: 0 auto 2rem auto;"></div>
            <div class="footer-columns">
                <div class="footer-column">
                    <h4>Home</h4>
                    <a href="#">Mapa Interativo</a>
                </div>
                <div class="footer-column">
                    <h4>Inteligência Territorial</h4>
                    <a href="#">Proporção de Demanda por<br>tema em relação ao total</a>
                    <a href="#">Registros Mensais</a>
                    <a href="#">Categoria por categoria</a>
                </div>
                <div class="footer-column">
                    <h4>Monitoramento de Notícias</h4>
                    <a href="#">Principais Categoria Menciondas<br>pelas entidades trimestralmente</a>
                    <a href="#">Frequência das Publicações</a>
                    <a href="#">Notícias Monitoradas</a>
                    <a href="#">Nuvem de Palavras</a>
                </div>
                <div class="footer-column">
                    <h4>Assessorias Técnicas</h4>
                    <a href="#">Resumo do Conteúdo Publicado</a>
                    <a href="#">Dados Gerais</a>
                </div>
        </div>

        <div style="border-bottom: 1px solid #ccc; width: 100%; margin: 2rem auto 0 auto;"></div>
        <div class="footer-bottom">
            <div class="temple-logo">
                <img src="data:image/png;base64,{logo_temple_base64}" alt="Logo Temple" />
            </div>
            <div>
                <span class = "obs">© 2025 - Observatório da Reparação</span>
            </div>
        </div>
        """, unsafe_allow_html=True)



# def show_sidebar():
#     """
#     Constrói o menu lateral com links para as páginas internas.
#     Você pode usar st.sidebar.radio, st.sidebar.selectbox etc.
#     """
    
#     st.sidebar.markdown(
#         """
#         <div style='
#             position: relative;
#             left: -1.5rem;
#             width: calc(100% + 3rem);
#             background-color: #EDB111;
#             color: #007E7A;
#             padding: 2px 0;
#             text-align: center;
#             font-weight: bold;
#             font-size: 18px;
#             border-radius: 0;
#             margin-top: 10px;
#             margin-bottom: 33px;
#         '>
#             Observatório da Reparação
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     def font_to_base64(path):
#         with open(path, "rb") as f:
#             return base64.b64encode(f.read()).decode()


#     def image_to_base64(path):
#         with open(path, "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode()


#     img1 = image_to_base64("db/temple_logo.png")
#     img2 = image_to_base64("db/vale_logo_pb.png")

#     st.sidebar.markdown(
#         f"""
#         <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1rem;">
#             <img src="data:image/png;base64,{img1}" style="width: 100px; margin-right: 10px;">
#             <div style="padding: 5px; border-radius: 5px;">
#                 <img src="data:image/png;base64,{img2}" style="width: 90px; margin-left: 10px;">
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.sidebar.markdown("<hr style='margin-top: 2rem; margin-bottom: 2rem; border: none; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)

#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "Início"

#     def mudar_pagina(pagina):
#         st.session_state.current_page = pagina

#     st.sidebar.markdown("<div style='margin-top: 0.5rem; margin-bottom: -2rem; color: white;'> 📁 Escolha sua sessão</div>", unsafe_allow_html=True)

#     opcao_menu = st.sidebar.selectbox(
#         label="",
#         options=["Início", "Inteligência Territorial", "Monitoramento de Notícias", "Assessorias Técnicas"],
#         index=["Início", "Inteligência Territorial", "Monitoramento de Notícias", "Assessorias Técnicas"].index(st.session_state.current_page)
#     )



#     df = pd.read_csv('db/glossario.csv', sep=';')  # ou sep=',' se for vírgula

#     termos = df['Termo'].tolist()
#     options = ["Selecione um termo…"] + termos

#     st.sidebar.markdown(
#         "<div style='margin-top: 1rem; margin-bottom: -2rem; color: white;'>📚 Glossário</div>",
#         unsafe_allow_html=True
#     )

#     termo_selecionado = st.sidebar.selectbox(
#         label="",
#         options=options,
#         index=0,
#         key="glossario_select"
#     )

#     if termo_selecionado != "Selecione um termo…":
#         significado = df.loc[df['Termo'] == termo_selecionado, 'Significado'].iloc[0]
#         st.sidebar.markdown(
#             f"<div style='margin-top: 0.1rem; color: white; text-align: justify;'>"
#             f"{significado}"
#             "</div>",
#             unsafe_allow_html=True
#         )


# def header_menu():
#     """
#     Renderiza as colunas com botões de navegação:
#     [Inteligência Territorial] [Monitoramento de Notícias] [Assessorias Técnicas]
#     Se o usuário clicar em algum botão, atualiza st.session_state['current_page'].
#     """
#     col4, col1, col2, col3, col5 = st.columns(5)
#     if col4.button("Home"):
#         st.session_state.current_page = "Home"
#     if col1.button("Inteligência Territorial"):
#         st.session_state.current_page = "Inteligência Territorial"
#     if col2.button("Monitoramento de Notícias"):
#         st.session_state.current_page = "Monitoramento de Notícias"
#     if col3.button("Assessorias Técnicas"):
#         st.session_state.current_page = "Assessorias Técnicas"

