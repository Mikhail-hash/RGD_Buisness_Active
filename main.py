import pandas as pd
import numpy as np
import csv
import os
import re
import datetime as dt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from calendar import month_name
import plotly.express as px







def graphic_show():
    global df
    global df_containers
    global df_direction
    file_path = Entry.get(E1)
    df = pd.read_excel(file_path)
    last_row = len(df) - 1
    df = df.drop(df.index[last_row])
    df.sort_values('Дата операции')

    df_containers = pd.DataFrame()
    l = df["Контейнер"].unique()
    df_containers = df_containers.assign(containers_index=l)

    time_delay = []
    for i in df_containers['containers_index']:
        time_delay.append(container_time(i))

    months = []
    for i in df_containers['containers_index']:
        months.append(container_month(i))

    df_direction = pd.DataFrame(df['Контейнер'])
    df_direction = df_direction.assign(direction=df['Станция назначения'])
    df_containers = df_containers.assign(time_delay=time_delay)
    df_containers = df_containers.assign(month=months)
    df_containers = df_containers.assign(direction=df_direction['direction'])

    monthi = list(month_name)[1:]
    for_graph = []
    for i in monthi:
        for_graph.append(time_delay_of_month(i))
    #print(for_graph)
    data = {'month': monthi, 'delay': for_graph}
    df3 = pd.DataFrame(data)
    df3['delay'] = pd.to_timedelta(df3['delay'])

    directions = df_direction['direction'].unique()
    for_graph2 = []
    for i in directions:
        for_graph2.append(time_delay_of_direction(i))
    data1 = {'direction': directions, 'delay': for_graph2}
    df4 = pd.DataFrame(data1)
    df4['delay'] = pd.to_timedelta(df4['delay'])

    fig1 = px.bar(x=df3['month'], y=df3['delay'].dt.days, title = "Средняя задержка по месяцам", labels = {'x':"Месяц", 'y':'Задержка (дни)'})
    fig2 = px.bar(x=df4['direction'], y=df4['delay'].dt.days, title = "Средняя задержка по направлениям", labels = {'x':"Направление", 'y':'Задержка (дни)'})

    fig1.show()
    fig2.show()
    return True

def container_history(container_index: str): 
    global df 
    df_container = df.loc[df['Контейнер'] == container_index]
    df_container = df_container.sort_values('Дата операции')
    return(df_container[['Контейнер', 'Дата операции','Опер (расш)']])

def container_time(container_index: str): 
    global df 
    df_containeri = df.loc[df['Контейнер'] == container_index] 
    return np.ptp(df_containeri['Дата операции'])

def container_month(container_index: str): 
    global df 
    df_container = df.loc[df['Контейнер'] == container_index] 
    df_container = df_container.sort_values('Дата операции')
    return (min(df_container['Дата операции']).strftime("%B"))




def time_delay_of_direction(direction: str):
    global df_containers
    mean_time_delay = df_containers[(df_containers['direction'] == direction)]['time_delay'].mean()
    return mean_time_delay

def time_delay_of_month(month: str):
    global df_containers
    mean_time_delay = df_containers[(df_containers['month'] == month)]['time_delay'].mean()
    return mean_time_delay
#=========================================================================================================================================================================================================================================================================================================
top = tk.Tk()
Label(top, text="", ).grid(row=0, column=1)
Label(top, text="Файл с контейнерами", ).grid(row=1, column=0)

E1 = Entry(top, bd=5)
E1.grid(row=1, column=1)

Button(top, text="Submit", command=graphic_show).grid(row=5, column=1)

print(E1)
top.mainloop()