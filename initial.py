import streamlit as st
import folium
from streamlit_folium import st_folium

import menu
from utils import load_css
from data_base import load_territorial_intelligence_data

# st.set_page_config(layout="wide")

def initial():
    load_css("home.css")

    st.markdown(f"""
                <div class="section-green-map">
                    <h2> Observatório da Reparação </h2>
                    <p> A plataforma reúne dashboards com dados estratégicos sobre<br>pautas comunitárias, atuação técnica e cobertura midiática. </p>
                    <p class="especial_box"> Mapa Interativo </p>
                </div>
                """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2]) 
    with col1:
        st.markdown(f"""
            <div class="section-white-map">
                <h3>Mapa<br> Interativo</h3>
                <p>Seguimento por município, exibe uma<br>
                síntese de informações estratégicas.<br>
                Como as principais pautas e demandas<br>
                comunitárias.</p>
                <p class="map_pointer">
                Posicione o cursor do mouse e obtenha<br>
                informações sobre o município.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        def formatar_tooltip_html(row):
            demandas = row['Top_TipoDemanda'].split("<br>") if row['Top_TipoDemanda'] != "-" else []
            microCategoria = row['Top_MicroCategoria'].split("<br>") if row['Top_MicroCategoria'] != "-" else []
            demandas_html = "<ul style='margin:0; padding-left:15px;'>" + "".join(f"<li>{d}</li>" for d in demandas) + "</ul>" if demandas else "-"
            microCategoria_html = "<ul style='margin:0; padding-left:15px;'>" + "".join(f"<li>{p}</li>" for p in microCategoria) + "</ul>" if microCategoria else "-"

            html = f"""
            <b>Município:</b> {row['municipio']}<br>
            <b>Região:</b> {row['Regiao']}<br>
            <b>Principais demandas 0800:</b> {demandas_html}
            <br><b>Principais demandas RCs:</b> {microCategoria_html}
            """
            return html

        data = load_territorial_intelligence_data()
        gdf = data['gdf_map']
        gdf['tooltip_html'] = gdf.apply(formatar_tooltip_html, axis=1)

        m = folium.Map(location=[-19.1, -44.2], zoom_start=8, tiles=None, control_scale=True)
        folium.TileLayer("CartoDB positron", name="Positron", control=False).add_to(m)

        color_map = {
            "Região 1": "#00867D",
            "Região 2": "#00A19A",
            "Região 3": "#EDB111",
            "Região 4": "#F5C542",
            "Região 5": "#919191"
        }

        tooltip = folium.GeoJsonTooltip(
            fields=['tooltip_html'],
            labels=False,
            sticky=True,
            style=(
                "background-color: white;"
                "border: 1px solid gray; "
                "border-radius: 8px; "
                "box-shadow: 3px 3px 8px rgba(0,0,0,0.15); "
                "padding: 10px; "
                "min-width: 350px; "
                "max-width: 500px; "
                "white-space: normal; "
                "word-break: break-word; "
                "overflow-wrap: break-word;"
            ),
            max_width=500,
        )

        folium.GeoJson(
            gdf,
            tooltip=tooltip,
            style_function=lambda x: {
                "fillColor": color_map.get(x["properties"]["Regiao"], "#CCC"),
                "color": "black",
                "weight": 0.5,
                "fillOpacity": 0.8,
            }
        ).add_to(m)

        bounds = gdf.total_bounds
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

        st_folium(m, width=800, height=500)

    menu.footer()
