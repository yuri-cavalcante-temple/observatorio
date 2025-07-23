import streamlit as st
import pandas as pd
from pathlib import Path
import os


def load_css(file_path: str):
    """
    Lê o arquivo CSS indicado e injeta no Streamlit via <style>.
    """
    css_file = Path(file_path)
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def navigation_menu(paginas: list[str], key_prefix: str = ""):
    """
    Cria botões de navegação em colunas para cada item de `paginas`.
    Se o usuário clicar em um botão, atualiza st.session_state['current_page'].
    - paginas: lista de strings, ex: ["Início", "Inteligência Territorial", ...]
    - key_prefix: prefixo para gerar chaves únicas dos botões (útil se houver múltiplos menus).
    """
    weights = [0.2] + [1] * len(paginas) + [0.2]
    cols = st.columns(weights)

    for idx, pagina in enumerate(paginas, start=1):
        btn_key = f"{key_prefix}btn_{pagina}"
        if cols[idx].button(pagina, key=btn_key):
            st.session_state.current_page = pagina


def render_header_banner(url_banner):
    """
    Se você tiver um banner ou logo no topo de todas as páginas, chame esta função.
    'url_banner' pode ser o caminho string (por ex. "db/header.png") ou um PIL.Image.
    """
    st.image(url_banner, use_container_width=True)


def change_page(pagina):
    st.session_state.pagina = pagina


def aplicar_filtros(
    df: pd.DataFrame,
    filtros: list[dict],
    date_column: str | None = None,
    key_prefix: str = "filtros",
    include_reset: bool = True
) -> pd.DataFrame:
    import streamlit as st
    import pandas as pd
    import datetime

    df = df.copy().fillna("Não Informado")
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .replace("", "Não Informado")
            .str.title()
        )

    for idx, cfg in enumerate(filtros):
        has_simple = 'column' in cfg
        has_composed = 'columns' in cfg and 'new_column' in cfg
        if not has_simple and not has_composed:
            raise KeyError(
                f"Filtro inválido na posição {idx}: é necessário 'column' ou ('columns' e 'new_column')"
            )

    reset_flag_key   = f"{key_prefix}_reset_flag"
    reset_button_key = f"{key_prefix}_reset_btn"

    if reset_flag_key not in st.session_state:
        st.session_state[reset_flag_key] = False

    def do_reset():
        st.session_state[reset_flag_key] = True

    for cfg in filtros:
        if 'columns' in cfg and 'new_column' in cfg:
            src = cfg['columns']
            df[cfg['new_column']] = df[src[0]].fillna(df[src[1]])

    valores = {}
    for cfg in filtros:
        colname = cfg.get('new_column', cfg.get('column'))
        widget_key = f"{key_prefix}_{colname}"
        if st.session_state[reset_flag_key]:
            valores[colname] = cfg.get('default', 'Total')
        else:
            valores[colname] = st.session_state.get(widget_key, cfg.get('default', 'Total'))

    if date_column:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        min_d = df[date_column].min().date()
        max_d = df[date_column].max().date()
        date_key = f"{key_prefix}_{date_column}"
        if st.session_state.get(reset_flag_key, False):
            valores[date_column] = (min_d, max_d)
        else:
            valores[date_column] = st.session_state.get(date_key, (min_d, max_d))

    col1, col2 = st.columns(2)
    filtros_col1 = filtros[:3]
    filtros_col2 = filtros[3:]

    with col1:
        for cfg in filtros_col1:
            colname = cfg.get('new_column', cfg.get('column'))
            options = ['Total'] + sorted(df[colname].dropna().unique().tolist())
            st.selectbox(
                cfg['label'],
                options,
                index=options.index(valores[colname]) if valores[colname] in options else 0,
                key=f"{key_prefix}_{colname}",
                help=cfg.get('help', '')
            )

    with col2:
        for cfg in filtros_col2:
            colname = cfg.get('new_column', cfg.get('column'))
            options = ['Total'] + sorted(df[colname].dropna().unique().tolist())
            st.selectbox(
                cfg['label'],
                options,
                index=options.index(valores[colname]) if valores[colname] in options else 0,
                key=f"{key_prefix}_{colname}",
                help=cfg.get('help', '')
            )

        if date_column:
            key_date_input = f"{key_prefix}_date_key"
            valores[date_column] = st.date_input(
                "Período",
                value=valores[date_column],
                min_value=min_d,
                max_value=max_d,
                key=key_date_input,
                help="Escolha um período"
            )

        if include_reset:
            st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
            st.button(
                "Resetar filtros",
                on_click=do_reset,
                key=reset_button_key
            )
            st.markdown("</div>", unsafe_allow_html=True)

    df_filtrado = df.copy()

    for cfg in filtros:
        colname = cfg.get('new_column', cfg.get('column'))
        val = st.session_state.get(f"{key_prefix}_{colname}", "Total")
        if val != 'Total':
            df_filtrado = df_filtrado[df_filtrado[colname] == val]

    if date_column:
        filtro_data = st.session_state.get(f"{key_prefix}_{date_column}")
        if isinstance(filtro_data, tuple):
            if len(filtro_data) == 2:
                dt0, dt1 = filtro_data
            elif len(filtro_data) == 1:
                dt0 = dt1 = filtro_data[0]
            else:
                dt0, dt1 = min_d, max_d
        elif isinstance(filtro_data, datetime.date):
            dt0 = dt1 = filtro_data
        else:
            dt0, dt1 = min_d, max_d

        df_filtrado = df_filtrado[
            (df_filtrado[date_column].dt.date >= dt0) &
            (df_filtrado[date_column].dt.date <= dt1)
        ]

    st.session_state[reset_flag_key] = False

    return df_filtrado
