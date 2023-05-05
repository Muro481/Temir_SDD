import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='SDD Təmir normativləri')
st.header('Təmir materialları 2022-2023')
st.subheader('Təmir materialların dövriyyəsi')

excel_file = 'C:/Users/User/Desktop/data/SDD/Material.xlsx'
sheet_name = 'Summary'


        # Şəkil əlavə etmək
# image = Image.open('C:/Users/User/Desktop/data/SDD/Train.jpg')
# st.image(image,
#          caption = "Azərbaycan Dəmir Yolları",
#         width = 500)

# Normativlər sütunu
excel_file_1 = 'C:/Users/User/Desktop/data/SDD/Material.xlsx'
sheet_name_Norms = 'Normativ'
df_Normativ = pd.read_excel(excel_file_1,
                   sheet_name = sheet_name_Norms,
                   usecols = 'B:K',
                   header = 0)

# Normativ sutununda unique adlari chixarir
Norms = df_Normativ['Təmir Növü'].unique().tolist()
per_loco = df_Normativ['per loco'].unique().tolist()

# 1-39 geder say uzre secim verirem
count_per_loco = st.slider('Bir lokomotivə təmir növündən asılı olaraq lazım olan material sayı: ',
                        min_value = min(per_loco),
                        max_value = max(per_loco),
                        value = (min(per_loco), max(per_loco)))


Normativs_selection = st.multiselect("Təmir növü:",
                                     Norms,
                                     default= Norms)

#  --- Group DATAFRAME based on selection
mask = (df_Normativ['Təmir Növü'].isin(Normativs_selection)) & (df_Normativ['per loco'].between(*count_per_loco))
# isin(Norms))
number_of_result = df_Normativ[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')    

# --- Group DATAFRAME  after selection
df_grouped = df_Normativ[mask].groupby(by=['Malın Adı ']).sum()[['per loco']]
df_grouped = df_grouped.rename(columns={'per loco': 'Miqdar'})
df_grouped = df_grouped.reset_index()

bar_chart = px.bar(df_grouped,
                   x = 'Malın Adı ',
                   y = 'Miqdar',
                   text = 'Miqdar',
                   color_discrete_sequence= ['#F63366']*len(df_grouped), 
template = "plotly_white")
st.plotly_chart(bar_chart)

# --- Vüsal analiz 
df_vusal = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols = 'B:L',
                                header=1)


# --- table vüsal cağırır
st.dataframe(df_vusal)


# --- Planlı təmir
excel_file = 'C:/Users/User/Desktop/data/SDD/Material.xlsx'
sheet_name_1 = 'Summary'
df = pd.read_excel(excel_file,
                   sheet_name = sheet_name_1,
                   usecols = 'O:P',
                   header = 2)

# --- Piechart formasına salmaq (planlı)
pie_chart = px.pie(df,
                   title = 'Planlı təmir',
                   values = 'Tezlik',
                   names= 'Material')


# --- piechart cağırır (planlı)
st.plotly_chart(pie_chart)


#  --- Plandan kənar təmir
df_plandan_kənar = pd.read_excel(excel_file,
                                sheet_name=sheet_name_1,
                                usecols = 'R:S',
                                header=2)

# --- Piechart formasına salmaq (plandan kənar)
pie_chart_1 = px.pie(df_plandan_kənar,
                   title = 'Plandan kənar təmir',
                   values = 'Tezlik ',
                   names= 'Material ')
# --- piechart cağırır (plandan kənar)
st.plotly_chart(pie_chart_1)


st.dataframe(df_Normativ)