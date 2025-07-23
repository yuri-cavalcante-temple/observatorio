import hashlib
import streamlit as st
from data_base import load_users

# faixa amarela

# st.markdown(
#     """
#     <div style='
#         position: relative;
#         left: -1.5rem;
#         width: calc(100% + 3rem);
#         background-color: #EDB111;
#         color: #007E7A;
#         padding: 2px 0;
#         text-align: center;
#         font-weight: bold;
#         font-size: 18px;
#         border-radius: 0;
#         margin-top: 10px;
#         margin-bottom: 33px;
#     '>
#         Observatório da Reparação
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# ─── Recupera o usuário atual (se já estiver logado) ─────────────────────────────────
def get_current_user():
    """
    Retorna um dict com {'username': <nome>} se o usuário já estiver autenticado,
    ou None caso contrário.
    """
    if st.session_state.get("login", False):
        return {"username": st.session_state.username}
    return None


# ─── Validação de credenciais ─────────────────────────────────────────────────────────
def check_credentials(username: str, password: str) -> bool:
    """
    Recebe username e senha em texto claro, gera hash SHA-256 da senha fornecida
    e compara com o dicionário retornado por load_users() (onde as senhas já vêm em hash).
    """
    users_dict = load_users()  # ex: {"admin": "<hash_sha256>", "temple": "<hash_sha256>"}
    if username in users_dict:
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        return users_dict[username] == hashed_input
    return False


# ─── Exibe o formulário de login e bloqueia o resto do app caso não autentique ─────────
def login():
    """
    Mostra um título “Login”, dois campos (usuário e senha) e um botão “Entrar”.
    Se as credenciais estiverem corretas, define st.session_state.login = True e st.session_state.username.
    Senão, exibe erro. Sempre chama st.stop() no final para impedir o restante do script.
    """

    st.markdown(
    """
    <style>
    /* Para versões recentes do Streamlit: */
    .stApp {
        background-color: #007E7A;
    }
    /* Se precisar afetar também a área interna (algumas versões antigas): */
    .reportview-container, .main {
        background-color: #00FF00;
    }
    
    /* ─ Botão (st.button) ──────────────────────────────────────────────── */
    .stButton {
        display: flex;
        justify-content: flex-end;
    }

    /* Seleciona o <button> dentro de stButton */
    /* Hover do botão: amarelo um pouco mais escuro */
    .stButton > button:hover {
        background-color: #EDB111 !important; 
        color: 007E7A !important;
        }

    /* ─ Rótulos (labels) e títulos ─────────────────────────────────────── */
    /* Força todos os textos (h1, h2, <label> de input, etc) em branco */
        h1, h2, h3, h4, h5, h6,
        label, .stTextInput label, .stTextInput div {
        color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    st.title("🔒 Login")
    username_input = st.text_input("Usuário")
    password_input = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if check_credentials(username_input, password_input):
            st.session_state.login = True
            st.session_state.username = username_input
        else:
            st.error("Usuário ou senha incorretos")

    st.stop()
