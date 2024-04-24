import base64
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob 

st.set_page_config(layout='wide')

file_ = open(r"C:\Users\PRITI\OneDrive\Desktop\New folder (3)\voting (1).gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8-sig")
file_.close()

st.header("Election")
st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="voting gif" width="120" height="100">', 
    unsafe_allow_html=True
)


parties_df=pd.read_csv('Partis_Data_.xlsx - Sheet1.csv')

column_name = "PARTIES"
options = parties_df[column_name].unique()  # Get unique values from the column
selected_option = st.selectbox(
    'Select Political Party',
    options
)
st.write(selected_option)


filtered_data = parties_df[parties_df['PARTIES'] == selected_option]


column_name2 = "EFFECTED_CONTITUENCY"
options2 = parties_df[column_name2].unique()  # Get unique values from the column
selected_option2 = st.selectbox(
    'Select an Constituency',
    options2
)
st.write(selected_option2)


filtered_data2 = parties_df[parties_df['EFFECTED_CONTITUENCY'] == selected_option2]


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

# Aggregate sentiments for each party
party_sentiments = filtered_data.groupby(['PARTIES', 'IMPACT']).size().reset_index(name='Count')

# # Create bar graph using Plotly
fig = px.bar(party_sentiments, x='PARTIES', y='Count',color='IMPACT',color_discrete_map={'Positive':'green','Negative':'red','Neutral':'skyblue'}, barmode='group',
             labels={'PARTIES': 'Party', 'Count': 'Count'}, title='Sentiment Analysis by Party')
st.plotly_chart(fig)



# grouped_data2 = filtered_data2.groupby(['PREVIOUS_POLL%', 'EFFECTED_POLL%'])['VARIATION'].sum().unstack(fill_value=0)
grouped_data2 = filtered_data2.groupby(['EVENTS_NAMES', 'IMPACT'])['VARIATION'].sum().unstack(fill_value=0)

# Create a horizontal bar chart for positive and negative impacts
fig = go.Figure()

for column in grouped_data2.columns:
    variation_in_poll_values = filtered_data2['VARIATION_IN_POLL'].values
    if any(variation_in_poll_values > 0) and column == 'Positive':
        fig.add_trace(go.Bar(y=grouped_data2.index, x=grouped_data2[column], orientation='h', name='Positive', marker_color='green'))
    elif any(variation_in_poll_values < 0) and column == 'Negative':
        fig.add_trace(go.Bar(y=grouped_data2.index, x=grouped_data2[column], orientation='h', name='Negative', marker_color='red'))

fig.update_layout(barmode='relative', title=f'Positive and Negative Impacts for {selected_option2} constituency')
st.plotly_chart(fig)