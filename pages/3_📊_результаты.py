import streamlit as st
from PIL import Image
import requests
import pandas as pd
import base64
import math

st.set_page_config(
    page_title="Результаты",
    page_icon="📊",
)

# url = 'https://drive.google.com/file/d/1btfNGC8jgp8wlgcVIziuQxe9kyrdSnVD/view?usp=sharing'
# file_id = url.split('/')[-2]
# read_url='https://drive.google.com/uc?id=' + file_id

# raw = requests.get(read_url, stream=True).raw
# image = Image.open(raw)
# st.image(image)

timestr = ''

class FileDownloader(object):
	
	def __init__(self, data,filename='Полученные_данные_за',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext

	def download(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
		# st.markdown("#### Download File ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Скачать данные</a>'
		st.markdown(href,unsafe_allow_html=True)

def benford_1():
    ben_1_list = []
    for i in range(1,10):
        ben_1 = math.log10(1+1/i)
        ben_1_list.append(ben_1)
    ben_1_df = pd.DataFrame(pd.Series(ben_1_list, index=list(range(1,10))), columns=['Ожидаемая частота (EP)'])
    return ben_1_df

def benford_2():
    ben_2_list = [0,0,0,0,0,0,0,0,0,0]
    for i in range(10,100):
        ben_2_list[i % 10] += math.log10(1+1/i)
    ben_2_df = pd.DataFrame(pd.Series(ben_2_list, index=list(range(0,10))), columns=['Ожидаемая частота (EP)'])
    return ben_2_df

def benford_12():
    ben_12_list = []
    for i in range(10,100):
        ben_12 = math.log10(1+1/i)
        ben_12_list.append(ben_12)
    ben_12_df = pd.DataFrame(pd.Series(ben_12_list, index=list(range(10,100))), columns=['Ожидаемая частота (EP)'])
    return ben_12_df

def z_calc(row, n):
    AP = row['Фактическая частота (AP)']
    EP = row['Ожидаемая частота (EP)']
    z = (abs(AP-EP) - (1/(2*n)))/(EP*(1-AP)/n)**(1/2)
    return float(z)

def x_square(data, list_ts_n):
    # AP = data['Фактическая частота (AP)']
    EP = data['Ожидаемая частота (EP)']
    series_ts_n = pd.Series(list_ts_n).groupby(list_ts_n).count()
    df_ts_n = pd.DataFrame(series_ts_n, columns=['Фактическое кол-во чисел (AC)'])    
    df_ts_n['Ожидаемое кол-во чисел (EC)'] = series_ts_n.sum()*EP
    EC = df_ts_n['Ожидаемое кол-во чисел (EC)']
    AC = df_ts_n['Фактическое кол-во чисел (AC)']
    x_s = (((AC-EC)**2)/EC).sum()
    return f'хи-квадрат: {x_s}'

def MAD_1(data):
    AP = data['Фактическая частота (AP)']
    EP = data['Ожидаемая частота (EP)']
    k = data.shape[0]
    mad = abs(AP-EP).sum()/k
    if (mad >= 0) & (mad < 0.006):
        st.write('mad - Близкое соответствие')
    elif (mad >= 0.006) & (mad < 0.012):
        st.write('mad - Приемлемое соответствие')
    elif (mad >= 0.012) & (mad < 0.015):
        st.write('mad - Предельно допустимое соответствие')
    elif (mad >= 0.015):
        st.write('mad - Несоответствие')
    return f'Значение mad: {mad}'

def MAD_2(data):
    AP = data['Фактическая частота (AP)']
    EP = data['Ожидаемая частота (EP)']
    k = data.shape[0]
    mad = abs(AP-EP).sum()/k
    if (mad >= 0) & (mad < 0.008):
        st.write('mad - Близкое соответствие')
    elif (mad >= 0.008) & (mad < 0.010):
        st.write('mad - Приемлемое соответствие')
    elif (mad >= 0.010) & (mad < 0.012):
        st.write('mad - Предельно допустимое соответствие')
    elif (mad >= 0.012):
        st.write('mad - Несоответствие')
    return f'Значение mad: {mad}'

def MAD_12(data):
    AP = data['Фактическая частота (AP)']
    EP = data['Ожидаемая частота (EP)']
    k = data.shape[0]
    mad = abs(AP-EP).sum()/k
    if (mad >= 0) & (mad < 0.0012):
        st.write('mad - Близкое соответствие')
    elif (mad >= 0.0012) & (mad < 0.0018):
        st.write('mad - Приемлемое соответствие')
    elif (mad >= 0.0018) & (mad < 0.0022):
        st.write('mad - Предельно допустимое соответствие')
    elif (mad >= 0.0022):
        st.write('mad - Несоответствие')
    return f'Значение mad: {mad}'




def benford(df):
    st.header('Основные тесты')
    list_ts_1 = []
    list_ts_2 = []
    list_ts_12 = []
    for summa in df['Сумма']:
        summa = int(summa)
        while summa >= 100:
             summa //=10
        ts_1 = summa // 10
        list_ts_1.append(ts_1)
        ts_2 = summa % 10
        list_ts_2.append(ts_2)
        ts_12 = summa
        list_ts_12.append(ts_12) 
        
    st.subheader('Тест первой цифры')
    df_ts_1 = pd.DataFrame(pd.Series(list_ts_1).groupby(list_ts_1).count() / len(list_ts_1), columns=['Фактическая частота (AP)'])
    df_ts_1.style.set_table_attributes("style='display:inline'").set_caption('Таблица распределения первой цифры')
    df_ts_1 = df_ts_1.join(benford_1())
    st.bar_chart(df_ts_1)
    df_ts_1['Z-статистика'] = df_ts_1.apply(lambda x: z_calc(x, n=df_ts_1.shape[0]), axis=1)
    st.write('Таблица распределения первой цифры')
    st.table(df_ts_1)
    st.write(MAD_1(df_ts_1))
    st.write(x_square(df_ts_1, list_ts_1))

    st.subheader('Тест второй цифры')
    df_ts_2 = pd.DataFrame(pd.Series(list_ts_2).groupby(list_ts_2).count() / len(list_ts_2), columns=['Фактическая частота (AP)'])
    df_ts_2.style.set_table_attributes("style='display:inline'").set_caption('Таблица распределения второй цифры')
    df_ts_2 = df_ts_2.join(benford_2())
    st.bar_chart(df_ts_2)
    df_ts_2['Z-статистика'] = df_ts_2.apply(lambda x: z_calc(x, n=df_ts_2.shape[0]), axis=1)
    st.write('Таблица распределения второй цифры')
    st.table(df_ts_2)
    st.write(MAD_2(df_ts_2))
    st.write(x_square(df_ts_2, list_ts_2))

    st.subheader('Тест первых двух цифр')
    df_ts_12 = pd.DataFrame(pd.Series(list_ts_12).groupby(list_ts_12).count() / len(list_ts_12), columns=['Фактическая частота (AP)'])
    df_ts_12.style.set_table_attributes("style='display:inline'").set_caption('Таблица распределения первой пары цифр')
    df_ts_12 = df_ts_12.join(benford_12())
    st.bar_chart(df_ts_12)
    df_ts_12['Z-статистика'] = df_ts_12.apply(lambda x: z_calc(x, n=df_ts_12.shape[0]), axis=1)
    st.write('Таблица распределения первых двух цифр')
    st.table(df_ts_12)
    st.write(MAD_12(df_ts_12))
    st.write(x_square(df_ts_12, list_ts_12))     

def filter_sus(row):
    filter1 = 'даренн' in row['Содержание']
    filter2 = 'дарени' in row['Содержание']
    filter3 = 'подар' in row['Содержание']
    filter4 = 'спонсор' in row['Содержание']
    filter5 = 'жертв' in row['Содержание']
    filter6 = 'проч' in row['Содержание']
    filter7 = 'допол' in row['Содержание']
    if filter1 | filter2 | filter3 | filter4 | filter5 | filter6 | filter7:
         return True
    else:
         return False
    
def spec(row):
    summa = int(row['Сумма'])
    filter1 = summa % (10**6) == 0
    filter2 = summa % (10**3) == 999
    if filter1 | filter2:
        return True
    else:
        return False

st.title("Результаты")

if 'sign in' not in st.session_state:
    st.session_state['sign in'] = False

if 'file_upload' not in st.session_state:
    st.session_state['file_upload'] = False

if 'data' not in st.session_state:
    st.session_state['data'] = False

if 'true_data_times' not in st.session_state:
    st.session_state['true_data_times'] = False

if st.session_state["sign in"] == False:
    st.error("Для работы этой вкладки выполните вход в систему на вкладке 'авторизация'")
else:
    st.info(f'Вход в систему выполнен под логином - {st.session_state["login"]}')

    button_ben = st.button("Основные тесты")
    button_add = st.button("Дополнительные тесты")

    if st.session_state['file_upload']:
        if st.session_state['true_data_times']:
            data = st.session_state['data']
            data = pd.DataFrame(data)

            if button_ben:
                benford(data)
            if button_add:
                st.subheader('Редкие')
                st.write('Проверка на наличие несвязанных, необычных или редких проводок')
                st.write('Счет Дт')
                data_seldom_dt = data.groupby('Счет_Дт')['Счет_Дт'].count().fillna(0)
                data_seldom_dt = pd.DataFrame(data_seldom_dt)
                data_seldom_dt = data_seldom_dt.dropna(subset=['Счет_Дт'])
                data_seldom_dt = data_seldom_dt[data_seldom_dt>0]
                data_seldom_dt = data_seldom_dt[data_seldom_dt<3]

                st.table(data_seldom_dt)
                if data_seldom_dt.shape[0] > 0:
                    download = FileDownloader(data_seldom_dt.to_csv(),file_ext='csv').download()
                st.write('Счет Кт')
                data_seldom_kt = data.groupby('Счет_Кт')['Счет_Кт'].count().fillna(0)
                data_seldom_kt = pd.DataFrame(data_seldom_kt)
                data_seldom_kt = data_seldom_kt.dropna(subset=['Счет_Кт'])
                data_seldom_kt = data_seldom_kt[data_seldom_kt>0]
                data_seldom_kt = data_seldom_kt[data_seldom_kt<3].reset_index(drop=True)
                st.table(data_seldom_kt)
                if data_seldom_kt.shape[0] > 0:
                    download = FileDownloader(data_seldom_kt.to_csv(),file_ext='csv').download()

                st.subheader('Подозрительное описание')
                st.write('Выявление проводок  с подозрительным описанием или его отсутствием')
                filter_sus_series = data.apply(filter_sus, axis=1)
                filter_nan = data['Содержание'].isna()
                data_sus = data[filter_sus_series | filter_nan].reset_index(drop=True)
                st.table(data_sus)
                if data_sus.shape[0] > 0:
                    download = FileDownloader(data.to_csv(),file_ext='csv').download()
                st.subheader('Выше порога')
                st.write('Выявление проводок выше указанного порога')
                data_anomal = data.query("Сумма > 1017518000").reset_index(drop=True)  
                st.table(data_anomal)
                if data_anomal.shape[0] > 0:
                    download = FileDownloader(data.to_csv(),file_ext='csv').download()               
                st.subheader('Специфические суммы')
                st.write('Поиск проводок со специфическими суммами')
                filter_spec = pd.Series(data.apply(spec, axis=1))
                data_spec = data[filter_spec]
                st.table(data_spec)
                if data_spec.shape[0] > 0:
                    download = FileDownloader(data.to_csv(),file_ext='csv').download()                 
    else:
        st.error("Для проведений теста необходимо загрузить файл во вкладке 'анализ журнальных проводок'")   
