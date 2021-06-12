import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk   #opensource library for 3d mapping
# import plotly.express as px #like matplotlib
st.title('Motor vehicle collision in NYC')

st.markdown('### This app is a streamlit dashboard that can be used '
            "to analyze collision in NYC")
Data_url=(r"C:\Users\parth\Downloads/Motor_Vehicle_Collisions_-_Crashes(2)")
@st.cache(persist=True)  # only compute one time like Jupyter notebook
def load_data(nrows):
    data=pd.read_csv(r"C:\Users\parth\Downloads/Motor_Vehicle_Collisions_-_Crashes(2).csv",nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']]) # read data, parse_dates convert to date_time  
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
    lowercase=lambda x:str(x).lower()  # convert it to lower case
    data.rename(lowercase,axis='columns',inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data
data=load_data(100000)
m=data['injured_persons'].max()
m=int(m)
# Visualize data 
st.header('Where are the most people injured in NYC?') #new question
injured_people=st.slider('Number of people injured in vehicle collision',0,m) # work as slider 0 to 19->m
st.map(data.query('injured_persons>=@injured_people')[['latitude','longitude']].dropna(how='any'))# build map
#                   here injured_persons column, and @injured_people from slider
st.header("How many collisions occur during given time of a day?")
hour= st.sidebar.slider('Hour to look at',0,24)
data=data[data['date/time'].dt.hour==hour]

# st.markdown('Vehicle collisions between %i:00 and %i:00' % (hour,(hour+1)%24)
midpoint=(np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude':midpoint[0],
        'longitude':midpoint[1],
        'zoom':11,
        'pitch':50,
    },
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=data[['date/time','latitude','longitude']],
            get_position=['longitude','latitude'],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0,1000]
        ),
    ]
))

st.subheader('breakdown by minute between %i:00 and %i:00' %(hour,(hour+1)%24))
filtered=data[
    (data['date/time'].dt.hour>=hour) & (data['date/time'].dt.hour<(hour+1))  #dtaframe with date/time between hour and hour+1
]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0]# x-axis data of histogram
chart_data=pd.DataFrame({'minute':range(60),'crashes':hist})
# fig=px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
# st.write(fig)




if st.checkbox('Show Raw Data',False):  # Work as a checkbox
    st.subheader('Raw Data')
    st.write(data)