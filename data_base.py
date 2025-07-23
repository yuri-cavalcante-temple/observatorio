import pandas as pd
import hashlib
import geopandas as gpd
from PIL import Image
# from datetime import datetime

def load_users() -> dict[str, str]:
    return {
        "admin":  hashlib.sha256("adminpass".encode()).hexdigest(),
        "temple": hashlib.sha256("senha123".encode()).hexdigest(),
        "vale": hashlib.sha256("valereparacao".encode()).hexdigest(),
    }

def read_rc():
    """Lê o CSV de 'Registro de Relacionamento' (rc.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/rc_new.csv", encoding="UTF-8", sep=";")

def read_rc_prsa():
    """Lê o CSV de 'Registro de Relacionamento' (rc.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/rc_prsa.csv", encoding="UTF-8", sep=";")

def read_srd():
    """Lê o CSV de 'Central 0800' (srd.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/srd_new.csv", encoding="UTF-8", sep=";")

def read_srd_prsa():
    """Lê o CSV de 'Central 0800' (srd.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/srd_prsa.csv", encoding="UTF-8", sep=";")

def read_clip():
    """Lê o CSV de clipping de notícias e retorna DataFrame cru."""
    return pd.read_csv("db/clip.csv", encoding="UTF-8", sep=";")

def read_citacoes():
    """Lê o CSV de citações (citacoes.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/citacoes.csv", encoding="unicode_escape", sep=";")

def read_orsa():
    """Lê o CSV de orsa (orsa.csv) e retorna DataFrame cru."""
    return pd.read_csv("db/orsa.csv", encoding="UTF-8", sep=";")

def read_gdf():
    """Lê o GeoJSON e retorna GeoDataFrame cru."""
    return gpd.read_file("db/gdf.geojson")

def read_temple_logo():
    return Image.open("db/temple.png")

def read_temple_logo_horizontal():
    return Image.open("db/temple_logo.png")

def read_vale_logo():
    return Image.open("db/vale.png")

def read_vale_logo_pb():
    return Image.open("db/vale_logo_pb.png")

def read_bannerhead():
    return Image.open("db/header.png")


def preprocess_srd(df_srd):
    """Limpa e normaliza colunas de srd, remove colunas irrelevantes e trata datas."""
    # Colunas a remover
    cols_to_drop = [
        'Protocolo', 'Mês', 'Ano', 'Território', 'Estado',
        'LocalAtendimento', 'FatoGerador', 'StatusDemanda',
        'DescricaoDemandas', 'InformacoesDemanda-Tratativa',
        'Area_Responsavel pelo atendimento', 'DataUltimaAlteracao',
        'TipoManifestacao'
    ]
    df = df_srd.drop(columns=[cols_to_drop], errors="ignore")

    # Renomear colunas
    df = df.rename(columns={
        'BairroPessoaImpactada': 'Bairro',
        'Municipio': 'Município',
        'MicroCategoria': 'Demanda'
    })

    # Padroniza espaços e quebras de linha nos nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\n', ' ')
        .str.replace(r'\s+', ' ', regex=True)
    )

    # Trata a coluna Data (formato dayfirst=True) e cria coluna "Mês" (string 'MM/YYYY')
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
        df['Mês']  = df['Data'].dt.strftime('%m/%Y')

    return df


def preprocess_srd_prsa(df_srd_prsa):
    """Limpa e normaliza colunas de srd_prsa, remove colunas irrelevantes e trata datas."""
    # Colunas a remover
    cols_to_drop = [
        'Protocolo', 'Mês', 'Ano', 'Território', 'Estado',
        'LocalAtendimento', 'FatoGerador', 'StatusDemanda',
        'DescricaoDemandas', 'InformacoesDemanda-Tratativa',
        'Area_Responsavel pelo atendimento', 'DataUltimaAlteracao',
        'TipoManifestacao'
    ]
    df = df_srd_prsa.drop(columns=[cols_to_drop], errors="ignore")

    # Renomear colunas
    df = df.rename(columns={
        'Localidade': 'Bairro',
        'Cidade': 'Município',
        'MicroCategoria': 'Demanda',
    })

    # Padroniza espaços e quebras de linha nos nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\n', ' ')
        .str.replace(r'\s+', ' ', regex=True)
    )

    # Trata a coluna Data (formato dayfirst=True) e cria coluna "Mês" (string 'MM/YYYY')
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
        df['Mês']  = df['Data'].dt.strftime('%m/%Y')

    return df


def preprocess_rc(df_rc):
    """Limpa e normaliza colunas de rc, remove colunas, renomeia e trata datas."""
    cols_to_drop = [
        'Tipo de Ação', 'Tratativa', 'Origem', 'Público Alvo',
        'Status', 'Data do Atendimento\n(se atendida)'
    ]
    df = df_rc.drop(columns=[cols_to_drop], errors="ignore")

    # Renomear colunas
    df = df.rename(columns={
        'Cidade': 'Município',
        'Localidade': 'Bairro'
    })

    # Padroniza espaços/quebras de linha
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\n', ' ')
        .str.replace(r'\s+', ' ', regex=True)
    )

    # Se existir coluna Data, converter para datetime e criar "Mês"
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
        df['Mês']  = df['Data'].dt.strftime('%m/%Y')

    return df


def preprocess_rc_prsa(df_rc_prsa):
    """Limpa e normaliza colunas de rc_prsa, remove colunas, renomeia e trata datas."""
    cols_to_drop = [
        'Tipo de Ação', 'Tratativa', 'Origem', 'Público Alvo',
        'Status', 'Data do Atendimento\n(se atendida)'
    ]
    df = df_rc_prsa.drop(columns=[cols_to_drop], errors="ignore")

    # Renomear colunas
    df = df.rename(columns={
        'Cidade': 'Município',
        'Localidade': 'Bairro'
    })

    # Padroniza espaços/quebras de linha
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('\n', ' ')
        .str.replace(r'\s+', ' ', regex=True)
    )

    # Se existir coluna Data, converter para datetime e criar "Mês"
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=True)
        df['Mês']  = df['Data'].dt.strftime('%m/%Y')

    return df


def preprocess_clip(df_clip):
    """Remove colunas não usadas no clipping e renomeia colunas principais."""
    cols_to_drop = ['TEMA 2', 'INFORMAÇÃO DUPLICADA', 'OBS']
    df = df_clip.drop(columns=[cols_to_drop], errors="ignore")

    df.columns = df.columns \
                   .str.strip() \
                   .str.replace('\n', ' ') \
                   .str.replace(r'\s+', ' ', regex=True)

    
    print('df.columns')

    df = df.rename(columns={
        'DATA': 'Data',
        'TÍTULO': 'Título',
        'VEICULO': 'Entidade',
        'CATEGORIA DO VEÍCULO': 'Categoria do Veículo',
        'BLOCO TEMÁTICO': 'Bloco Temático',
        'TEMA PRINCIPAL': 'Tema Principal'
    })

    if 'Data' not in df.columns:
        # Se chegou aqui, quer dizer que nem “DATA” nem “Data” (após strip) existiam
        # Exibimos todas as colunas para debugging mais fácil:
        todas_as_colunas = df.columns.tolist()
        raise KeyError(
            f"A coluna 'Data' não foi encontrada após o rename em preprocess_clip().\n"
            f"As colunas presentes são: {todas_as_colunas}\n"
            f"Verifique o nome exato da coluna de data no seu CSV de clipping."
        )

    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce').dt.date
    return df


def preprocess_citacoes(df_cit):
    """Renomeia colunas do CSV de citações."""
    return df_cit.rename(columns={
        'Grupos de Documentos': 'Entidade',
        'Bloco temático':     'Tema'
    })


def preprocess_orsa(df_orsa):
    """Renomeia colunas de orsa."""
    return df_orsa.rename(columns={
        'CATEGORIA': 'Categoria',
        'CONTEUDO':  'Conteúdo'
    })


def preprocess_gdf(gdf):
    """Padroniza nome de coluna de município no GeoDataFrame."""
    # Supondo que 'municipio' já exista no GeoJSON. Se precisar, podemos renomear aqui.
    return gdf.copy()


def compute_top3_srd(df_srd, municipios_mapa):
    """
    Recebe um DataFrame de srd filtrado por município (já preprocessado)
    e retorna um DataFrame com as 3 demandas mais comuns por município.
    """
    fil = df_srd[df_srd["Município"].isin(municipios_mapa)].copy()

    top_srd = (
        fil.groupby(["Município", "Demanda"])
           .size()
           .reset_index(name="Contagem")
           .sort_values(["Município", "Contagem"], ascending=[True, False])
    )

    top3 = (
        top_srd.groupby("Município")
               .head(3)
               .groupby("Município")
               .agg({"Demanda": lambda x: ", ".join(x)})
               .reset_index()
    )
    top3.columns = ["municipio", "Top_TipoDemanda"]
    return top3


def compute_top3_rc(df_rc, municipios_mapa):
    """
    Recebe um DataFrame de rc filtrado por município (já preprocessado)
    e retorna um DataFrame com as 3 áreas temáticas mais comuns por município.
    """
    fil = df_rc[df_rc["Município"].isin(municipios_mapa)].copy()

    top_rc = (
        fil.groupby(["Município", "MicroCategoria"])
           .size()
           .reset_index(name="Contagem")
           .sort_values(["Município", "Contagem"], ascending=[True, False])
    )

    top3 = (
        top_rc.groupby("Município")
              .head(3)
              .groupby("Município")
              .agg({"MicroCategoria": lambda x: ", ".join(x)})
              .reset_index()
    )
    top3.columns = ["municipio", "Top_MicroCategoria"]
    return top3


# 5) FUNÇÃO PARA FILTRAR E MONTAR O DATAFRAME UNIFICADO

def build_unified_df(df_rc, df_srd):
    """
    Recebe dois DataFrames preprocessados (rc e srd), filtra pelos municípios
    presentes no GeoDataFrame, adiciona coluna 'Fonte' e concatena em df_unificado_geral.
    """
    # Filtra municípios por intersecção com gdf (só no main.py teremos a lista exata)
    # Aqui assumimos que o usuário vai passar a série `municipios_mapa` vindos do GeoDataFrame.
    # Mas, para compor o unificado, basta pressupor que quem chamar saiba filtrar antes.

    # Marca as fontes
    rc_fil = df_rc.copy()
    rc_fil["Fonte"] = "Registro de Relacionamento"

    srd_fil = df_srd.copy()
    srd_fil["Fonte"] = "Central 0800"

    # Mantém somente as colunas relevantes em cada um e gera colunas faltantes
    rc_final = rc_fil[['Data', 'Município', 'Bairro', 'Fonte', 'MicroCategoria']].copy()
    rc_final['Demanda'] = None

    srd_final = srd_fil[['Data', 'Município', 'Bairro', 'Demanda', 'Fonte']].copy()
    srd_final['MicroCategoria'] = None

    # Concatena
    df_unificado_geral = pd.concat([rc_final, srd_final], ignore_index=True)
    df_unificado_geral['Data'] = pd.to_datetime(df_unificado_geral['Data'], errors='coerce')

    return df_unificado_geral


def build_unified_df_prsa(df_rc_prsa, df_srd_prsa):
    """
    Recebe dois DataFrames preprocessados (rc e srd), filtra pelos municípios
    presentes no GeoDataFrame, adiciona coluna 'Fonte' e concatena em df_unificado_geral.
    """
    # Filtra municípios por intersecção com gdf (só no main.py teremos a lista exata)
    # Aqui assumimos que o usuário vai passar a série `municipios_mapa` vindos do GeoDataFrame.
    # Mas, para compor o unificado, basta pressupor que quem chamar saiba filtrar antes.

    # Marca as fontes
    rc_fil_prsa = df_rc_prsa.copy()
    rc_fil_prsa["Fonte"] = "Registro de Relacionamento"

    srd_fil_prsa = df_srd_prsa.copy()
    srd_fil_prsa["Fonte"] = "Central 0800"

    # Mantém somente as colunas relevantes em cada um e gera colunas faltantes
    rc_final_prsa = rc_fil_prsa[['Data', 'Município', 'Bairro', 'Fonte', 'MicroCategoria']].copy()
    rc_final_prsa['Demanda'] = None


    srd_final_prsa = srd_fil_prsa[['Data', 'Município', 'Bairro', 'Demanda', 'Fonte']].copy()
    srd_final_prsa['MicroCategoria'] = None

    # Concatena
    df_unificado_prsa = pd.concat([rc_final_prsa, srd_final_prsa], ignore_index=True)
    df_unificado_prsa['Data'] = pd.to_datetime(df_unificado_prsa['Data'], errors='coerce')

    return df_unificado_prsa


def load_territorial_intelligence_data():
    # 1) lê dados brutos
    df_rc  = read_rc()
    df_rc_prsa  = read_rc_prsa()
    df_srd = read_srd()
    df_srd_prsa = read_srd_prsa()
    gdf    = read_gdf()

    # 2) pré-processa
    df_rc_proc  = preprocess_rc(df_rc)
    df_rc_proc_prsa  = preprocess_rc_prsa(df_rc_prsa)
    df_srd_proc = preprocess_srd(df_srd)
    df_srd_proc_prsa = preprocess_srd_prsa(df_srd_prsa)
    gdf_proc    = preprocess_gdf(gdf)

    # 3) extrai lista de municípios do geojson
    municipios_mapa = gdf_proc["municipio"].unique()

    # 4) calcula top3 de cada base
    top3_srd = compute_top3_srd(df_srd_proc, municipios_mapa)
    top3_rc  = compute_top3_rc(df_rc_proc, municipios_mapa)

    # 5) faz merge no gdf para criar GeoDataFrame pronto para o mapa
    gdf_map = gdf_proc.merge(top3_srd, on="municipio", how="left")
    gdf_map = gdf_map.merge(top3_rc, on="municipio", how="left")

    # substitui NaN por "-" e insere <br> para tooltips
    gdf_map["Top_TipoDemanda"]   = gdf_map["Top_TipoDemanda"].fillna("-").str.replace(", ", "<br>")
    gdf_map["Top_MicroCategoria"] = gdf_map["Top_MicroCategoria"].fillna("-").str.replace(", ", "<br>")

    # 6) monta df unificado (rc + srd)
    df_unificado_geral = build_unified_df(df_rc_proc, df_srd_proc)
    df_unificado_prsa = build_unified_df_prsa(df_rc_proc_prsa, df_srd_proc_prsa)


    return {
        "rc_proc":    df_rc_proc,
        "rc_proc_prsa":    df_rc_proc_prsa,
        "srd_proc":   df_srd_proc,
        "srd_proc_prsa":   df_srd_proc_prsa,
        "gdf_map":    gdf_map,
        "df_unificado_geral": df_unificado_geral,
        "df_unificado_prsa": df_unificado_prsa
    }


def load_clipping_data():
    """
    Retorna o DataFrame de clipping de notícias (`clip`) já preprocessado.
    """
    df_clip  = read_clip()
    df_clip_proc = preprocess_clip(df_clip)
    return df_clip_proc


def load_indepedent_consultancy_data():
    """
    Retorna um dicionário contendo:
      - orsa_proc: DataFrame de ORSA preprocessado,
      - citacoes_proc: DataFrame de Citações preprocessado.
    """
    df_orsa     = read_orsa()
    df_citacoes = read_citacoes()

    orsa_proc     = preprocess_orsa(df_orsa)
    citacoes_proc = preprocess_citacoes(df_citacoes)

    return {
        "orsa_proc":     orsa_proc,
        "citacoes_proc": citacoes_proc
    }

def load_image():
    temple_logo = read_temple_logo()
    temple_logo_horizontal = read_temple_logo_horizontal()
    vale_logo = read_vale_logo()
    vale_logo_pb = read_vale_logo_pb()
    url_bannerhead = read_bannerhead()
    
    return {
        "temple_logo": temple_logo,
        "temple_logo_horizontal": temple_logo_horizontal,
        "vale_logo": vale_logo,
        "vale_logo_pb": vale_logo_pb,
        "url_bannerhead": url_bannerhead
    }
