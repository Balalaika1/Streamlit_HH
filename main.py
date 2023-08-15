import datetime
import streamlit as st
import pandas as pd
from plotly import express as pl






sheet_id = '1--tKdV1vyLsbdHYRL-D4SXFfM-fGvvIs'
df_main = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

df_main['(salary)_from_in_RUR'] = df_main['(salary)_from_in_RUR'].str.replace(',','.')
df_main['(salary)_from_in_RUR'] = df_main['(salary)_from_in_RUR'].astype('float64')
def replace_comma_and_convert(value):
    try:
        return float(value.replace(',', '.'))
    except (ValueError, AttributeError):
        return value
df_main['(salary)_to_in_RUR'] = df_main['(salary)_to_in_RUR'].apply(replace_comma_and_convert)
df_main['(salary)_to_in_RUR'] = df_main['(salary)_to_in_RUR'].astype('float64')

df_main['(address)_lat'] = df_main['(address)_lat'].str.replace(',','.')
df_main['(address)_lat'] = df_main['(address)_lat'].astype('float64')

df_main['(address)_lng'] = df_main['(address)_lng'].str.replace(',','.')
df_main['(address)_lng'] = df_main['(address)_lng'].astype('float64')

df_main['created_at'] = pd.to_datetime(df_main['created_at'])
df_main['date_only'] = df_main['created_at'].dt.date


max_salary_from_in_RUR = int(max(df_main['(salary)_from_in_RUR']))
min_salary_from_in_RUR = int(min(df_main['(salary)_from_in_RUR']))

def funck(min, max, request_name, create_date):
    df = df_main[(df_main['(salary)_from_in_RUR'] >= min) & (df_main['(salary)_from_in_RUR'] <= max)]
    if len(create_date) == 2:
        df = df[(df['date_only'] >= create_date[0]) & (df['date_only'] <= create_date[1])]
    if request_name != []:
        df = df[df['download_name'].isin(request_name)]
    return df


def fig_horiz(df_main):
    df = df_main
    agg_func_count = {'(salary)_from_in_RUR': ['mean']}

    grouped_data = df.groupby('(employer)_name', as_index=False).agg(agg_func_count).round(2)
    grouped_data.head()
    grouped_data.columns = ['_'.join(col).rstrip('_') for col in grouped_data.columns.values]
    grouped_data = grouped_data.sort_values(by='(salary)_from_in_RUR_mean', ascending=False)
    grouped_data = grouped_data.head(30)
    grouped_data = grouped_data.sort_values(by='(salary)_from_in_RUR_mean', ascending=True)

    fig = pl.bar(grouped_data, y='(employer)_name', x='(salary)_from_in_RUR_mean', orientation = 'h')

    return fig

def map_f(df_main):
    df = df_main
    df_filtered = df.dropna(subset=['(address)_lat', '(address)_lng'])
    fig = pl.scatter_mapbox(df_filtered, lat='(address)_lat', lon='(address)_lng', color='(salary)_from_in_RUR',
                            size='(salary)_from_in_RUR', size_max=10, zoom=0, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def average_value(df_main):
    df = df_main
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month'] = df['created_at'].dt.to_period('W').astype(str)

    agg_func_count = {'(salary)_from_in_RUR': ['mean'], '(salary)_to_in_RUR': ['mean']}
    average_salary_by_month = df.groupby(['month'], as_index=False).agg(agg_func_count).round(2)
    average_salary_by_month.head()
    average_salary_by_month.columns = ['_'.join(col).rstrip('_') for col in average_salary_by_month.columns.values]

    fig = pl.line()
    fig.add_scatter(x=average_salary_by_month['month'], y=average_salary_by_month['(salary)_from_in_RUR_mean'], mode='lines', name='Зарплата От')
    fig.add_scatter(x=average_salary_by_month['month'], y=average_salary_by_month['(salary)_to_in_RUR_mean'], mode='lines', name='Зарплата До')
    return fig























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
