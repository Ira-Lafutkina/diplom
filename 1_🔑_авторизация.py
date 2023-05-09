import streamlit as st
from PIL import Image
import requests

st.set_page_config(
    page_title="Авторизация",
    page_icon="🔑",
)

# url = 'https://drive.google.com/file/d/1btfNGC8jgp8wlgcVIziuQxe9kyrdSnVD/view?usp=sharing'
# file_id = url.split('/')[-2]
# read_url='https://drive.google.com/uc?id=' + file_id

# raw = requests.get(read_url, stream=True).raw
# print(type(raw))
# image = Image.open(raw)
# st.image(image)

text_input_container_0 = st.empty()
text_input_container_1 = st.empty()
text_input_container_2 = st.empty()
text_input_container_3 = st.empty()

text_input_container_0.title("Авторизация")
# st.sidebar.success("Select a page above.")

if "login" not in st.session_state:
    st.session_state["login"] = ""

if "password" not in st.session_state:
    st.session_state["password"] = ""

st.session_state["sign in"] = False

login = text_input_container_1.text_input("Логин", st.session_state["login"], placeholder="login")
st.session_state["login"] = login
password = text_input_container_2.text_input("Пароль", st.session_state["password"], placeholder="password")
st.session_state["password"] = password

button_sign_in = text_input_container_3.button("Войти")
personal_data = [('ira', '12345'), ('irina', '54321')]

if button_sign_in:
    true_pass = 0
    for log, pas in personal_data:
        if (login == log) & (password == pas):
            text_input_container_0.empty()            
            text_input_container_1.empty()
            text_input_container_2.empty()
            text_input_container_3.empty()
            st.info(f'Вход в систему под логином выполнен - {login}')
            st.session_state["sign in"] = True
            break;
    if st.session_state["sign in"] == False:
        st.write('Неверный логин/пароль')
