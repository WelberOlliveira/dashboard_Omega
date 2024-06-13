
import streamlit as st
import streamlit_authenticator as stauth
from dependencies import add_registro, consulta, consulta_geral, cria_tabela
from time import sleep
import home

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #ffffff;
opacity:30;
background: rgb(224,238,241);
background: linear-gradient(180deg, rgba(224,238,241,1) 95%, #2A3054 95%);
margin-top: -70px; /* Ajuste este valor conforme necessário */
}

[data-testid="stHeader"] {
background-color: #ffffff;
opacity:30;
background: rgb(224,238,241);
}

.custom-title {
    color: red; /* Altere para a cor desejada */
    font-size: 25px; /* Ajuste o tamanho da fonte se necessário */
    font-weight: bold;
}
</style>

"""

st.markdown(page_bg_img, unsafe_allow_html=True)



def main():
    st.title("Dashboard Ômega Invest")

    try:
        consulta_geral()
    except:
        cria_tabela()

    db_query = consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name' : data[0], 'password' : data[2]}

    COOKIE_EXPIRY_DAYS = 30
    authenticator = stauth.Authenticate(
        registros,
        'random_cookie_name',
        'random_signature_key',
        COOKIE_EXPIRY_DAYS,

    )
    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
        usuario_form()


def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        col1, col2 = st.columns([1, 11])
        with col2:
            authenticator.logout('Logout', 'main')
        with col1:
            st.write(f'*{name} está logado!*')
        home.app(username)
    elif authentication_status == False:
        st.error('Usuário ou senha incorretos')
    elif authentication_status == None:
        st.warning('Insira um nome de usuário e uma senha')
        clicou_em_registrar = st.button("Registrar")
        if clicou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.experimental_rerun()


def confirmation_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senhas não conferem')
        sleep(3)
    elif consulta(st.session_state.user):
        st.warning('Nome de usuário já existe.')
        sleep(3)
    else:
        add_registro(st.session_state.nome,st.session_state.user, hashed_password[0])
        st.success('Registro efetuado!')
        sleep(3)

def usuario_form():
    with st.form(key="test", clear_on_submit=True):
        nome = st.text_input("Nome", key="nome")
        username = st.text_input("Usuário", key="user")
        password = st.text_input("Password", key="pswrd", type="password")
        confirm_password = st.text_input("Confirm Password", key="confirm_pswrd", type="password")
        submit = st.form_submit_button(
            "Salvar", on_click=confirmation_msg,
        )
    clicou_em_fazer_login = st.button("Fazer Login")
    if clicou_em_fazer_login:
        st.session_state['clicou_registrar'] = False
        st.experimental_rerun()
        

if __name__ == "__main__":
    main()
