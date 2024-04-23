import base64
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob 

st.set_page_config(layout='wide')

parties_df=pd.read_csv('Partis_Data_.xlsx - Sheet1.csv')

column_name = "PARTIES"
options = parties_df[column_name].unique()  # Get unique values from the column
selected_option = st.selectbox(
    'Choose an option',
    options
)
st.write("You selected", selected_option)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Apply sentiment analysis to the event data
parties_df['IMPACT'] = parties_df['EVENTS_NAMES'].apply(analyze_sentiment)

# Aggregate sentiments for each party
party_sentiments = parties_df.groupby(['PARTIES', 'IMPACT']).size().reset_index(name='Count')

# Create bar graph using Plotly
fig = px.bar(party_sentiments, x='PARTIES', y='Count', color='IMPACT', barmode='group',
             labels={'PARTIES': 'Party', 'Count': 'Count'}, title='Sentiment Analysis by Party')
st.plotly_chart(fig)




fig = go.Figure()
fig.add_trace(go.Bar(x=parties_df["EVENTS_NAMES"], y=[80,60,90,60,50,60,80,95,85,60],
                base=0,
                marker_color='crimson',
                name='Positive'))
fig.add_trace(go.Bar(x=parties_df['EVENTS_NAMES'], y=[55,90,90,60,80,55,45,65,65],
                base=[-55,-90,-90,-60,-80,-55,-45,-65,-65],
                marker_color='lightslategrey',
                name='Negative'
                ))

st.plotly_chart(fig)