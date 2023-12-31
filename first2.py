import datetime
import streamlit as st
import pandas as pd
from plotly import express as pl
#from Data_DF import fig_horiz, map_f, average_value, max_salary_from_in_RUR, min_salary_from_in_RUR, df_main
from Data_DF2 import funck, fig_horiz, map_f, average_value, max_salary_from_in_RUR, min_salary_from_in_RUR, df_main
path = 'combined_data.xlsx'

st.set_page_config(layout="wide")


#st.title("h1 exs")
#st.subheader('first')
#st.header('sec')
#
#st.text('3')
#st.markdown('---')
with st.sidebar:
    st.markdown('##Sidebar')
    st.markdown('Конфигурации')
    request_name = st.multiselect('Выбрать имя запроса',df_main['download_name'].unique())

    today = datetime.datetime.now()
    next_year = today.year + 1
    jan_1 = datetime.date(today.year, today.month-2, today.day)
    dec_31 = datetime.date(today.year, 12, 31)

    d = st.date_input(
        "Выбрать дату создания",
        (jan_1, datetime.date(today.year, today.month, today.day)),
        jan_1,
        dec_31,
        format="DD.MM.YYYY",
    )

    selected_range = st.slider("Уровень заработной платы", min_value=min_salary_from_in_RUR, max_value=max_salary_from_in_RUR, value=(0, 100000), step=10000, format=None, key=None, help=None,on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    min_selected = selected_range[0]
    max_selected = selected_range[1]
    st.write(f"Минимальное значение: {min_selected}")
    st.write(f"Максимальное значение: {max_selected}")

col1, col2 = st.columns([3, 1])

df_main = funck(min_selected, max_selected, request_name, d)
with col1:
    fig = map_f(df_main)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = fig_horiz(df_main)
    st.plotly_chart(fig, use_container_width=True)

fig = average_value(df_main)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_main)