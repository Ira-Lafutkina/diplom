import streamlit as st
from PIL import Image
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

st.set_page_config(
    page_title="Авторизация",
    page_icon="🔑",
)

url = 'https://drive.google.com/file/d/1btfNGC8jgp8wlgcVIziuQxe9kyrdSnVD/view?usp=sharing'
file_id = url.split('/')[-2]
read_url='https://drive.google.com/uc?id=' + file_id

raw = requests.get(read_url, stream=True).raw
print(type(raw))
image = Image.open(raw)
st.image(image)

st.sidebar.info("Select a page above.")
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

# if "file" not in st.session_state:
#      st.session_state["file"] = None

# if "my_input" not in st.session_state:
#     st.session_state["my_input"] = ""

login = text_input_container_1.text_input("Логин", st.session_state["login"], placeholder="login")
st.session_state["login"] = login
password = text_input_container_2.text_input("Пароль", st.session_state["password"], placeholder="password")
st.session_state["password"] = password
# st.secrets['password']
button_sign_in = text_input_container_3.button("Войти")
personal_data = [('ira', '12345'), ('irina', '54321')]
#st.secrets[]
# true_pass = 0
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
        # file = text_input_container_1.file_uploader("Данные для анализа")
        # st.session_state["file"] = file
        # if file:
        #     text_input_container_2.write(st.session_state["file"])

# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

# #file = st.file_uploader('Yaml file')

# url_yaml = 'https://drive.google.com/file/d/1vky4sy9dpvHLwXA5EBmZQ1qyx5MC1Zye/view?usp=sharing'
# file_id = url_yaml.split('/')[-2]
# read_url_yaml='https://drive.google.com/uc?id=' + file_id

# # raw = requests.get(read_url_yaml, stream=True).raw
# # file_stream = 
# # print(raw)

# with open(read_url_yaml) as file:
#     config = yaml.load(file, Loader=SafeLoader)
    
# # config = yaml.load

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# name, authentication_status, username = authenticator.login('Login', 'main')

# # 

# if authentication_status:
#     authenticator.logout('Logout', 'main', key='unique_key')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status is False:
#     st.error('Username/password is incorrect')
# elif authentication_status is None:
#     st.warning('Please enter your username and password')

# streamlit run c:/Users/User/Desktop/SM-liiga/Multipage_apps/1_🔑_авторизация.py

# streamlit_app.py

# import streamlit as st

# def check_password():
#     """Returns `True` if the user had a correct password."""

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if (
#             st.session_state["username"] in st.secrets["passwords"]
#             and st.session_state["password"]
#             == st.secrets["passwords"][st.session_state["username"]]
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store username + password
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False

#     if "password_correct" not in st.session_state:
#         # First run, show inputs for username + password.
#         st.text_input("Логин", on_change=password_entered, key="username", placeholder="login")
#         st.text_input(
#             "Пароль", type="password", on_change=password_entered, key="password", placeholder="password"
#         )
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         st.error("😕 User not known or password incorrect")
#         return False
#     else:
#         # Password correct.
#         return True

# if check_password():
#     st.write("Here goes your normal Streamlit app...")
#     st.button("Click me")
