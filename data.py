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



filtered_data = parties_df[parties_df['PARTIES'] == selected_option]
# Group by event and impact, and aggregate impact scores
grouped_data = filtered_data.groupby(['EVENTS_NAMES', 'IMPACT'])['MOD_VALUE'].sum().unstack(fill_value=0)

# Create a horizontal bar chart for positive and negative impacts
fig = go.Figure()

if 'Positive' in grouped_data.columns:
    fig.add_trace(go.Bar(y=grouped_data.index, x=grouped_data['Positive'], orientation='h', name='Positive', marker_color='green'))

if 'Negative' in grouped_data.columns:
    fig.add_trace(go.Bar(y=grouped_data.index, x=grouped_data['Negative'], orientation='h', name='Negative', marker_color='red'))

fig.update_layout(barmode='relative', title=f'Positive and Negative Impacts for {selected_option} Events')
st.plotly_chart(fig)

# Apply sentiment analysis to the event data
filtered_data['IMPACT'] = filtered_data['EVENTS_NAMES'].apply(analyze_sentiment)

# # Aggregate sentiments for each party
party_sentiments = filtered_data.groupby(['PARTIES', 'IMPACT']).size().reset_index(name='Count')

# # Create bar graph using Plotly
fig = px.bar(party_sentiments, x='PARTIES', y='Count', color='IMPACT', barmode='group',
             labels={'PARTIES': 'Party', 'Count': 'Count'}, title='Sentiment Analysis by Party')
st.plotly_chart(fig)