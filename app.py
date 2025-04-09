##import libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#loading data
data_reshaped = pd.read_csv('C:/Users/amzej/Desktop/global-suicide-dashboard/data_reshaped.csv')

st.set_page_config(
    page_title="Global Suicide Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed")

# Sidebar
with st.sidebar:
    st.title('Data info')

st.title("Global suicide data analysis")

#st.markdown("""
#    <style>
#        div.block-container {padding-top: 1.5rem; padding-bottom: 0rem; margin-top: -10px;}
#    </style>
#    """, unsafe_allow_html=True)

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

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

def make_gender_plot(input_df):
    s_by_gender = input_df.groupby('Gender')['SuicidesNo'].sum()
    s_by_gender = s_by_gender.rename(index={"female": "Female", "male": "Male"})
    fig = px.pie(s_by_gender, values=s_by_gender.values, names=s_by_gender.index,
             title="Suicides by gender",
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
             title="Suicides by generation",
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
    SuByGen_sorted.index = SuByGen_sorted.index + 1  # numeracja od 1, nie od 0
    SuByGen_sorted.index.name = 'Rank'  # nazwij indeks np. Rank

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

col = st.columns((1, 3, 1), gap='small')
col2 = st.columns((0.75, 2, 2), gap='small')

worst_year, max_suicides_year, worst_country, worst_country_no, most_at_risk_age_group, most_at_risk_suicides = calculate_suicide_metrics(data_reshaped)

with col[0]:
    SuByGen_sorted = make_low_suicide_rate_table(data_reshaped)
    st.markdown("### Countries with the lowest suicide rates")
    st.dataframe(SuByGen_sorted, use_container_width=False)

with col[1]:
    choropleth = make_choropleth(data_reshaped)
    st.plotly_chart(choropleth, use_container_width=True)

with col[2]:
    generation_plot = make_generation_plot(data_reshaped)
    st.plotly_chart(generation_plot, use_container_width=True)

with col2[0]:
    gender_plot = make_gender_plot(data_reshaped)
    st.plotly_chart(gender_plot, use_container_width=True)

with col2[1]:
    top_countries_plot = make_top_countries_plot(data_reshaped)
    st.plotly_chart(top_countries_plot, use_container_width=True)

with col2[2]:
    age_in_years_plot = make_age_in_years_plot(data_reshaped)
    st.plotly_chart(age_in_years_plot, use_container_width=True)