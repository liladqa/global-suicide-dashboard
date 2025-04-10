##import libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#loading data
data_reshaped = pd.read_csv('data_reshaped.csv')

st.set_page_config(
    page_title="Global Suicide Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed")

css_file = 'style.css'  

with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Exploratory Analysis of Suicide Data (1985–2020)")

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
    #title_text='Global suicides per 100k (1985 - 2020)',
    margin=dict(l=0, r=0, t=30, b=0),
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
    markers=True, line_shape="spline")

    age_in_years_plot.update_layout(
    template="plotly_white",
    xaxis_title="Year",
    yaxis_title="No. of suicides",
    hovermode="x unified"
    )
    return age_in_years_plot
    
def make_top_countries_plot(input_df):
    top_countries = input_df.groupby("Country")["SuicidesPer100k"].mean().nlargest(10)
    top_countries_plot = px.bar(top_countries, x=top_countries.index, y=top_countries.values,
             labels={"x": "Country", "y": "Suicides per 100k"},
             color=top_countries.values, color_continuous_scale="reds")
    return top_countries_plot

def make_gender_plot(input_df):
    s_by_gender = input_df.groupby('Gender')['SuicidesNo'].sum()
    s_by_gender = s_by_gender.rename(index={"female": "Female", "male": "Male"})
    fig = px.pie(s_by_gender, values=s_by_gender.values, names=s_by_gender.index,
             color_discrete_sequence=px.colors.qualitative.Plotly)

    fig.update_traces(
    textinfo='percent+label+value',
    )

    fig.update_layout(
    template="plotly_white",  
    font=dict(size=12),  
    showlegend=True 
    )

    return fig

def make_generation_plot(input_df):
    s_by_generation = input_df.groupby('Generation')['SuicidesNo'].sum()
    fig = px.pie(s_by_generation, values=s_by_generation.values, names=s_by_generation.index,
             color_discrete_sequence=px.colors.qualitative.Plotly)

    fig.update_traces(
    textinfo='percent+label+value',
    )

    fig.update_layout(
    template="plotly_white",  
    font=dict(size=12),
    showlegend=True
    )
    return fig

def make_low_suicide_rate_table(input_df):
    s_100k_country = input_df.groupby('Country')['SuicidesPer100k'].mean().round(2)

    if isinstance(s_100k_country, pd.Series):
        s_100k_country = s_100k_country.reset_index()

    s_100k_country_filtered = s_100k_country[s_100k_country['SuicidesPer100k'] < 1]

    SuByGen_sorted = s_100k_country_filtered.sort_values(by="SuicidesPer100k", ascending=True).reset_index(drop=True)
    SuByGen_sorted.index = SuByGen_sorted.index + 1 
    SuByGen_sorted.index.name = 'Rank' 

    return SuByGen_sorted

def calculate_suicide_metrics(data):
    yearly_suicides = data.groupby("Year")["SuicidesNo"].sum()
    country_suicides = data.groupby("CountryToISO")["SuicidesPer100k"].mean()
    age_group_suicides = data.groupby("Age")["SuicidesNo"].mean()

    # worst year
    worst_year = yearly_suicides.idxmax()
    max_suicides_year = yearly_suicides.max()

    # worst country
    worst_country = country_suicides.idxmax()
    worst_country_no = country_suicides.max()

    # most at risk generation
    most_at_risk_age_group = age_group_suicides.idxmax()
    most_at_risk_suicides = age_group_suicides.max()

    return worst_year, max_suicides_year, worst_country, worst_country_no, most_at_risk_age_group, most_at_risk_suicides

#dashboard main panel

plh = st.container()

with plh:
    col = st.columns((0.25, 1, 3, 1, 0.25), gap='small')
    col2 = st.columns((0.25, 0.75, 2, 2, 0.25), gap='small')

    worst_year, max_suicides_year, worst_country, worst_country_no, most_at_risk_age_group, most_at_risk_suicides = calculate_suicide_metrics(data_reshaped)

    with col[1]:
        SuByGen_sorted = make_low_suicide_rate_table(data_reshaped)
        st.markdown("#### Countries with the lowest suicide rates")
        st.dataframe(SuByGen_sorted, use_container_width=False)

    with col[2]:
        choropleth = make_choropleth(data_reshaped)
        st.markdown("#### Global suicides per 100k (1985 - 2020)")
        st.plotly_chart(choropleth, use_container_width=True)

    with col[3]:
        generation_plot = make_generation_plot(data_reshaped)
        st.markdown("#### Suicides by generation")
        st.plotly_chart(generation_plot, use_container_width=False)

    with col2[1]:
        gender_plot = make_gender_plot(data_reshaped)
        st.markdown("#### Suicides by gender")
        st.plotly_chart(gender_plot, use_container_width=False)

    with col2[2]:
        top_countries_plot = make_top_countries_plot(data_reshaped)
        st.markdown("#### Top 10 countries with highest suicide rates")
        st.plotly_chart(top_countries_plot, use_container_width=False)

    with col2[3]:
        age_in_years_plot = make_age_in_years_plot(data_reshaped)
        st.markdown("#### No. of suicides by year and age group")
        st.plotly_chart(age_in_years_plot, use_container_width=False)