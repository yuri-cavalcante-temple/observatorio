import streamlit as st

import menu


from initial import initial
from territorial_intelligence import territorial_intelligence
from news_clipping import news_clipping
from independent_consultancy import indepedent_consultancy
from login import get_current_user, login
from utils import load_css, navigation_menu
from data_base import (
    load_users,
    load_territorial_intelligence_data,
    load_clipping_data,
    load_indepedent_consultancy_data,
    load_image
)


def main():
    st.set_page_config(
        page_title="Observatório da Reparação",
        page_icon="db/favicon_vale.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_css("style.css")
    menu.menu()
    
    pagina = st.query_params.get("page", "home")

    if pagina == "home":
        initial()
    elif pagina == "territorial_intelligence":
        territorial_intelligence()
    elif pagina == "news_clipping":
        news_clipping()
    elif pagina == "indepedent_consultancy":
        indepedent_consultancy()
    else:
        st.error(f"Página '{pagina}' não encontrada.")

if __name__ == "__main__":
    main()
