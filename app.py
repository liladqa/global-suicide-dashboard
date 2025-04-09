##import libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#loading data
data_reshaped = pd.read_csv('C:/Users/amzej/Desktop/global-suicide-dashboard/data_reshaped.csv')

#page configuration

st.set_page_config(
    page_title="Global Suicide Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
    <style>
        div.block-container {padding-top: 1.5rem; padding-bottom: 0rem; margin-top: -10px;}
    </style>
    """, unsafe_allow_html=True)

#graphs 

def make_choropleth(input_df):
    s_100k_country = data_reshaped.groupby(['CountryToISO', 'Country'])['SuicidesPer100k'].mean().reset_index()

    choropleth = go.Figure(data=go.Choropleth(
    locations = s_100k_country['CountryToISO'],
    z = s_100k_country['SuicidesPer100k'],
    text = s_100k_country['Country'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Suicides per 100k',
    ))

    choropleth.update_layout(
    title_text='Global suicides per 100k (1985 - 2020)',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
    )

    return choropleth

def make_age_in_years_plot(input_df):
    s_by_age = input_df.groupby(['Year', 'Age'])['SuicidesNo'].sum()
    s_by_age = s_by_age.reset_index()
    age_in_years_plot = px.line(s_by_age, x='Year', y="SuicidesNo", color="Age",
    title="No. of suicides by year and age group",
    markers=True, line_shape="spline")

    age_in_years_plot.update_layout(
    template="plotly_white",
    xaxis_title="Year",
    yaxis_title="No. of suicides",
    hovermode="x unified"
    )
    age_in_years_plot.update_layout(height=300)
    return age_in_years_plot
    
def make_top_countries_plot(input_df):
    top_countries = input_df.groupby("Country")["SuicidesPer100k"].mean().nlargest(10)
    top_countries_plot = px.bar(top_countries, x=top_countries.index, y=top_countries.values, 
             title="Top 10 countries with highest suicide rates",
             labels={"x": "Country", "y": "Suicides per 100k"},
             color=top_countries.values, color_continuous_scale="reds")
    top_countries_plot.update_layout(height=300)
    return top_countries_plot


#dashboard main panel

col = st.columns((1.5, 3, 2), gap='small')

with col[1]:
    choropleth = make_choropleth(data_reshaped)
    st.plotly_chart(choropleth, use_container_width=True)

    top_countries_plot = make_top_countries_plot(data_reshaped)
    st.plotly_chart(top_countries_plot, use_container_width=True)

    age_in_years_plot = make_age_in_years_plot(data_reshaped)
    st.plotly_chart(age_in_years_plot, use_container_width=True)

