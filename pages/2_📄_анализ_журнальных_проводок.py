import streamlit as st
from PIL import Image
import requests
import pandas as pd

st.set_page_config(
    page_title="Анализ журнальных проводок",
    page_icon="📄",
)

url = 'https://drive.google.com/file/d/1btfNGC8jgp8wlgcVIziuQxe9kyrdSnVD/view?usp=sharing'
file_id = url.split('/')[-2]
read_url='https://drive.google.com/uc?id=' + file_id

raw = requests.get(read_url, stream=True).raw
image = Image.open(raw)
st.image(image)

st.title("Анализ журнальных проводок")

if 'sign in' not in st.session_state:
    st.session_state['sign in'] = False

if 'file_upload' not in st.session_state:
    st.session_state['file_upload'] = False

if 'data' not in st.session_state:
    st.session_state['data'] = None

if 'data_time_1' not in st.session_state:
    st.session_state['data_time_1'] = None

if 'data_time_2' not in st.session_state:
    st.session_state['data_time_2'] = None

if 'true_data_times' not in st.session_state:
    st.session_state['true_data_times'] = False

if st.session_state["sign in"] == False:
    st.error("Для работы этой вкладки выполните вход в систему на вкладке 'авторизация'")
else:
    st.info(f'Вход в систему выполнен под логином - {st.session_state["login"]}')
    file = st.file_uploader('Данные для анализа', type=['csv', 'xls', 'xlsx'])
    if file:
        data = pd.read_excel(file)
        data = pd.DataFrame(data)
        data.columns = data.columns.str.replace(' ', '_')
        st.session_state['file_upload'] = True
        st.session_state['data'] = data
        data_time_1 = st.date_input('Начальная дата для анализа')
        data_time_2 = st.date_input('Конечная дата для анализа')
        st.session_state['data_time_1'] = data_time_1
        st.session_state['data_time_2'] = data_time_2
        if data_time_1 > data_time_2:
            st.error("Анализ проводится с даты_1 по дату_2, а не наоборот")
        else:
            data_time_1 = pd.Timestamp(data_time_1)
            data_time_2 = pd.Timestamp(data_time_2)
            st.session_state['data'] = data.query('Дата >= @data_time_1 & Дата <= @data_time_2')
            st.session_state['true_data_times'] = True
            st.info("Для получения анализа перейдите на вкладку 'результаты'")
        
